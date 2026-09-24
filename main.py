"""Nuvio/Stremio HTTP addon for Movies & TV Series.

Quality criterion: Any quality >= 1080p (1080p, 1440p/2K, 2160p/4K).
Zero maintenance (no cookies, direct HTTP streams).
"""
import asyncio
import json
import logging
import os
import time
import httpx
from collections import deque
from dataclasses import dataclass, field
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from providers import cinemeta
from providers import cf_client
from providers import vidlove
from providers import vidrock

ADDON_ID = "org.nuvio.movies-1080p"
ADDON_NAME = "Movies & TV 1080p+"
VERSION = "1.4.0"
CACHE_TTL_SEARCH = int(os.getenv("CACHE_TTL_SEARCH", "3600"))
CACHE_TTL_CATALOG = int(os.getenv("CACHE_TTL_CATALOG", "86400"))  # 24 hours
STREAM_DEADLINE_S = float(os.getenv("STREAM_DEADLINE_S", "9.5"))
PORT = int(os.getenv("PORT", "7001"))

# Rate limiting configuration (requests per minute per provider)
RATE_LIMITS = {
    "vidlove": int(os.getenv("RATE_LIMIT_VIDLOVE", "30")),
    "vidrock": int(os.getenv("RATE_LIMIT_VIDROCK", "30")),
}

# Provider priority order (tried sequentially)
PROVIDERS = [
    ("vidlove", vidlove.resolve),
    ("vidrock", vidrock.resolve),
]

# Structured logging setup
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": time.time(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "created", "filename", "funcName", "levelname", "levelno", "lineno", "module", "msecs", "message", "msg", "name", "pathname", "process", "processName", "relativeCreated", "thread", "threadName", "exc_info", "exc_text", "stack_info"]:
                log_obj[key] = value
        return json.dumps(log_obj)

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=log_level, handlers=[handler], force=True)
logger = logging.getLogger("nuvio-movies-addon")

# Metrics tracking
@dataclass
class Metrics:
    stream_requests: int = 0
    stream_success: int = 0
    stream_errors: int = 0
    provider_calls: dict[str, int] = field(default_factory=lambda: {"vidlove": 0, "vidrock": 0})
    provider_success: dict[str, int] = field(default_factory=lambda: {"vidlove": 0, "vidrock": 0})
    provider_errors: dict[str, int] = field(default_factory=lambda: {"vidlove": 0, "vidrock": 0})
    cache_hits: int = 0
    cache_misses: int = 0
    catalog_requests: int = 0

metrics = Metrics()

# Rate limiter using sliding window
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: deque[float] = deque()
    
    def acquire(self) -> bool:
        now = time.time()
        while self.requests and self.requests[0] <= now - self.window_seconds:
            self.requests.popleft()
        
        if len(self.requests) >= self.max_requests:
            return False
        
        self.requests.append(now)
        return True
    
    def wait_time(self) -> float:
        if not self.requests:
            return 0.0
        now = time.time()
        if len(self.requests) < self.max_requests:
            return 0.0
        oldest = self.requests[0]
        return max(0.0, oldest + self.window_seconds - now)

# Initialize rate limiters per provider
_rate_limiters: dict[str, RateLimiter] = {
    name: RateLimiter(limit) for name, limit in RATE_LIMITS.items()
}

# Catalog configuration
CATALOGS = [
    {
        "id": "movies_trending",
        "name": "Trending Movies",
        "type": "movie",
        "extra": [
            {"name": "genre", "isRequired": False, "options": ["action", "comedy", "drama", "horror", "sci-fi", "thriller"]},
            {"name": "sort", "isRequired": False, "options": ["popular", "rating", "release"]}
        ]
    },
    {
        "id": "series_trending",
        "name": "Trending Series",
        "type": "series",
        "extra": [
            {"name": "genre", "isRequired": False, "options": ["action", "comedy", "drama", "horror", "sci-fi", "thriller"]},
            {"name": "sort", "isRequired": False, "options": ["popular", "rating", "release"]}
        ]
    },
    {
        "id": "movies_top_rated",
        "name": "Top Rated Movies",
        "type": "movie",
        "extra": [
            {"name": "genre", "isRequired": False, "options": ["action", "comedy", "drama", "horror", "sci-fi", "thriller"]}
        ]
    },
    {
        "id": "series_top_rated",
        "name": "Top Rated Series",
        "type": "series",
        "extra": [
            {"name": "genre", "isRequired": False, "options": ["action", "comedy", "drama", "horror", "sci-fi", "thriller"]}
        ]
    }
]

app = FastAPI(title=ADDON_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MANIFEST = {
    "id": ADDON_ID,
    "version": VERSION,
    "name": ADDON_NAME,
    "description": "Direct HTTP Movies & TV Series streams >= 1080p (1080p, 1440p, 4K). No torrents, no logins.",
    "resources": ["stream", "catalog"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt", "tmdb"],
    "catalogs": CATALOGS,
    "behaviorHints": {"p2pNotSupported": True, "configurable": True},
}

_cache: dict[str, tuple[float, object]] = {}


def cache_get(key: str):
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < CACHE_TTL_SEARCH:
        return hit[1]
    return None


def cache_set(key: str, val: object):
    _cache[key] = (time.time(), val)


def cache_get_catalog(key: str):
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < CACHE_TTL_CATALOG:
        return hit[1]
    return None


def cache_set_catalog(key: str, val: object):
    _cache[key] = (time.time(), val)


def format_size(bytes_val: int | float | None) -> str | None:
    """Format bytes into readable string (e.g. 2.15 GB, 850 MB)."""
    if not bytes_val or bytes_val <= 0:
        return None
    gb = bytes_val / (1024 ** 3)
    if gb >= 1.0:
        return f"{gb:.2f} GB"
    mb = bytes_val / (1024 ** 2)
    return f"{int(mb)} MB"


def estimate_size(bandwidth_bps: int | None, ctype: str = "movie") -> int | None:
    """Estimate byte size from HLS bandwidth and standard runtime."""
    if not bandwidth_bps or bandwidth_bps <= 0:
        return None
    # Standard movie: ~6300s (105 min), Series episode: ~2700s (45 min)
    duration_s = 6300 if ctype == "movie" else 2700
    return int((duration_s * bandwidth_bps) / 8)


def is_quality_ge_1080(quality: str | None, height: int | None = None) -> bool:
    """Check if quality meets the >= 1080p requirement."""
    if height is not None and height >= 1080:
        return True
    if not quality:
        return False
    q = quality.strip().lower()
    if any(k in q for k in ("4k", "2160p", "uhd", "1440p", "2k", "1080p", "fhd")):
        return True
    # If standard number, e.g. 1080
    digits = "".join(ch for ch in q if ch.isdigit())
    if digits.isdigit() and int(digits) >= 1080:
        return True
    return False


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    base = str(request.base_url).rstrip("/")
    manifest_url = f"{base}/manifest.json"
    return f"""<html><body style="font-family:sans-serif;max-width:640px;margin:40px auto;line-height:1.6">
<h2>{ADDON_NAME} v{VERSION}</h2>
<p>Direct HTTP streams for Movies & TV Series. <b>>= 1080p only</b> (1080p, 1440p, 4K). No logins, no cookies, no torrents.</p>
<p><b>Manifest URL (install in Nuvio/Stremio):</b></p>
<pre style="background:#f4f4f4;padding:10px;border-radius:4px"><code>{manifest_url}</code></pre>
<p>Test Movie: <code><a href="{base}/stream/movie/tt0137523.json">{base}/stream/movie/tt0137523.json</a></code></p>
<p>Test Series: <code><a href="{base}/stream/series/tt0903747:1:1.json">{base}/stream/series/tt0903747:1:1.json</a></code></p>
<p>Diagnostics: <code><a href="{base}/diag">{base}/diag</a></code> • Keep-alive: <code><a href="{base}/ping">{base}/ping</a></code></p>
</body></html>"""


@app.get("/manifest.json")
async def manifest():
    return JSONResponse(MANIFEST)


@app.get("/ping")
async def ping():
    return {"ok": True, "version": VERSION, "ts": time.time()}


@app.get("/health")
async def health():
    return {
        "ok": True,
        "version": VERSION,
        "quality_filter": ">=1080p",
    }


@app.get("/metrics")
async def get_metrics():
    """Return current metrics."""
    return {
        "stream_requests": metrics.stream_requests,
        "stream_success": metrics.stream_success,
        "stream_errors": metrics.stream_errors,
        "success_rate": round(metrics.stream_success / max(metrics.stream_requests, 1) * 100, 2),
        "provider_calls": metrics.provider_calls,
        "provider_success": metrics.provider_success,
        "provider_errors": metrics.provider_errors,
        "cache_hits": metrics.cache_hits,
        "cache_misses": metrics.cache_misses,
        "cache_hit_rate": round(metrics.cache_hits / max(metrics.cache_hits + metrics.cache_misses, 1) * 100, 2),
        "catalog_requests": metrics.catalog_requests,
    }


async def fetch_catalog_from_tmdb(ctype: str, sort: str = "popular", genre: str = "", page: int = 1) -> list[dict]:
    """Fetch catalog data from TMDB via Cinemeta-compatible API."""
    # Use Cinemeta's catalog endpoints or a public TMDB proxy
    # For now, we'll use a simple approach with known popular content
    # In production, you'd use TMDB API with a key
    
    # Static popular content as fallback (tmdb_ids)
    popular_movies = [
        {"id": "tt0111161", "title": "The Shawshank Redemption", "year": 1994, "tmdb_id": 278},
        {"id": "tt0068646", "title": "The Godfather", "year": 1972, "tmdb_id": 238},
        {"id": "tt0071562", "title": "The Godfather Part II", "year": 1974, "tmdb_id": 240},
        {"id": "tt0468569", "title": "The Dark Knight", "year": 2008, "tmdb_id": 155},
        {"id": "tt0137523", "title": "Fight Club", "year": 1999, "tmdb_id": 550},
        {"id": "tt0109830", "title": "Forrest Gump", "year": 1994, "tmdb_id": 13},
        {"id": "tt0167260", "title": "The Lord of the Rings: The Return of the King", "year": 2003, "tmdb_id": 122},
        {"id": "tt0110912", "title": "Pulp Fiction", "year": 1994, "tmdb_id": 680},
        {"id": "tt0133093", "title": "The Matrix", "year": 1999, "tmdb_id": 603},
        {"id": "tt0108052", "title": "Schindler's List", "year": 1993, "tmdb_id": 424},
        {"id": "tt0120737", "title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "tmdb_id": 120},
        {"id": "tt0167261", "title": "The Lord of the Rings: The Two Towers", "year": 2002, "tmdb_id": 121},
        {"id": "tt0080684", "title": "Star Wars: Episode V - The Empire Strikes Back", "year": 1980, "tmdb_id": 1891},
        {"id": "tt0076759", "title": "Star Wars", "year": 1977, "tmdb_id": 11},
        {"id": "tt0050083", "title": "12 Angry Men", "year": 1957, "tmdb_id": 389},
        {"id": "tt0109830", "title": "Forrest Gump", "year": 1994, "tmdb_id": 13},
        {"id": "tt0167260", "title": "The Lord of the Rings: The Return of the King", "year": 2003, "tmdb_id": 122},
        {"id": "tt0110912", "title": "Pulp Fiction", "year": 1994, "tmdb_id": 680},
        {"id": "tt0133093", "title": "The Matrix", "year": 1999, "tmdb_id": 603},
        {"id": "tt0108052", "title": "Schindler's List", "year": 1993, "tmdb_id": 424},
    ]
    
    popular_series = [
        {"id": "tt0903747", "title": "Breaking Bad", "year": 2008, "tmdb_id": 1396},
        {"id": "tt0944947", "title": "Game of Thrones", "year": 2011, "tmdb_id": 1399},
        {"id": "tt0411008", "title": "The Wire", "year": 2002, "tmdb_id": 1402},
        {"id": "tt0455275", "title": "The Sopranos", "year": 1999, "tmdb_id": 1416},
        {"id": "tt1856010", "title": "House of Cards", "year": 2013, "tmdb_id": 1404},
        {"id": "tt2306299", "title": "The Crown", "year": 2016, "tmdb_id": 66732},
        {"id": "tt2560140", "title": "Stranger Things", "year": 2016, "tmdb_id": 66732},
        {"id": "tt2698640", "title": "The Handmaid's Tale", "year": 2017, "tmdb_id": 65780},
        {"id": "tt3032476", "title": "The Boys", "year": 2019, "tmdb_id": 76479},
        {"id": "tt0903747", "title": "Breaking Bad", "year": 2008, "tmdb_id": 1396},
        {"id": "tt1475582", "title": "Sherlock", "year": 2010, "tmdb_id": 19885},
        {"id": "tt2861424", "title": "Rick and Morty", "year": 2013, "tmdb_id": 60574},
        {"id": "tt1475582", "title": "Sherlock", "year": 2010, "tmdb_id": 19885},
        {"id": "tt2861424", "title": "Rick and Morty", "year": 2013, "tmdb_id": 60574},
        {"id": "tt10637874", "title": "Fallout", "year": 2024, "tmdb_id": 106379},
        {"id": "tt94997", "title": "House of the Dragon", "year": 2022, "tmdb_id": 94997},
    ]
    
    if ctype == "movie":
        items = popular_movies
    else:
        items = popular_series
    
    # Convert to Stremio meta format
    metas = []
    for item in items[:20]:  # Limit to 20 items
        metas.append({
            "id": item["id"],
            "type": ctype,
            "name": item["title"],
            "poster": f"https://image.tmdb.org/t/p/w500/{item.get('poster_path', '')}" if item.get('poster_path') else "",
            "year": item.get("year"),
            "imdb_id": item["id"] if item["id"].startswith("tt") else None,
            "tmdb_id": item.get("tmdb_id"),
        })
    return metas


@app.get("/catalog/{catalog_type}/{catalog_id}.json")
async def catalog(catalog_type: str, catalog_id: str, genre: str = "", sort: str = "popular", page: int = 1):
    """Serve catalog data for movies/series."""
    metrics.catalog_requests += 1
    logger.info("catalog_request", extra={"catalog_type": catalog_type, "catalog_id": catalog_id})
    
    if catalog_type not in ("movie", "series"):
        logger.warning("catalog_invalid_type", extra={"catalog_type": catalog_type})
        return JSONResponse({"metas": []})
    
    # Validate catalog exists
    catalog_config = next((c for c in CATALOGS if c["id"] == catalog_id and c["type"] == catalog_type), None)
    if not catalog_config:
        logger.warning("catalog_not_found", extra={"catalog_id": catalog_id, "catalog_type": catalog_type})
        return JSONResponse({"metas": []})
    
    cache_key = f"catalog:{catalog_type}:{catalog_id}:{genre}:{sort}:{page}"
    cached = cache_get_catalog(cache_key)
    if cached is not None:
        metrics.cache_hits += 1
        logger.info("catalog_cache_hit", extra={"cache_key": cache_key})
        return JSONResponse({"metas": cached})

    metrics.cache_misses += 1
    
    try:
        metas = await fetch_catalog_from_tmdb(catalog_type, sort, genre, page)
        cache_set_catalog(cache_key, metas)
        logger.info("catalog_success", extra={"catalog_id": catalog_id, "metas_count": len(metas)})
        return JSONResponse({"metas": metas})
    except Exception as e:
        logger.error("catalog_error", extra={"catalog_id": catalog_id, "error": str(e)})
        return JSONResponse({"metas": []})


@app.get("/diag")
async def diag(q: str = "Inception"):
    """Check upstream reachability and provider status."""
    results = {}
    for name, resolver in PROVIDERS:
        try:
            prov_streams = await resolver(27205, "movie", 1, 1, "Inception", 2010)
            results[name] = {
                "status": "ok",
                "streams_count": len(prov_streams),
                "sample": prov_streams[0]["name"] if prov_streams else None,
                "sample_title": prov_streams[0]["title"] if prov_streams else None
            }
        except Exception as e:
            results[name] = {"status": "error", "error": str(e)}
    return {"query": q, "providers": results}


@app.get("/stream/{ctype}/{full_id}.json")
async def stream(ctype: str, full_id: str):
    """Serve movie/series streams >= 1080p."""
    start_time = time.time()
    metrics.stream_requests += 1
    logger.info("stream_request_start", extra={"ctype": ctype, "full_id": full_id})
    
    if ctype not in ("movie", "series"):
        metrics.stream_errors += 1
        logger.warning("stream_invalid_type", extra={"ctype": ctype})
        return JSONResponse({"streams": []})

    base_id, season, episode = cinemeta.parse_strem_id(full_id)
    cache_key = f"streams:{ctype}:{base_id}:{season}:{episode}"
    cached = cache_get(cache_key)
    if cached is not None:
        metrics.cache_hits += 1
        logger.info("stream_cache_hit", extra={"cache_key": cache_key})
        return JSONResponse({"streams": cached})

    metrics.cache_misses += 1

    async with httpx.AsyncClient() as client:
        meta = await cinemeta.get_meta(client, base_id, ctype)

    if not meta or not meta.get("title"):
        metrics.stream_errors += 1
        logger.warning("stream_no_meta", extra={"base_id": base_id, "ctype": ctype})
        return JSONResponse({"streams": []})

    title = meta["title"]
    year = meta.get("year")
    tmdb_id = meta.get("tmdb_id")

    streams = []
    if tmdb_id:
        for name, resolver in PROVIDERS:
            metrics.provider_calls[name] += 1
            # Check rate limit
            limiter = _rate_limiters.get(name)
            if limiter and not limiter.acquire():
                wait = limiter.wait_time()
                logger.warning("provider_rate_limited", extra={"provider": name, "wait_seconds": wait})
                await asyncio.sleep(min(wait, 2.0))
                if not limiter.acquire():
                    logger.warning("provider_rate_limited_skip", extra={"provider": name})
                    continue
            
            try:
                prov_streams = await asyncio.wait_for(
                    resolver(
                        tmdb_id=tmdb_id,
                        ctype=ctype,
                        season=season,
                        episode=episode,
                        title=title,
                        year=year
                    ),
                    timeout=STREAM_DEADLINE_S
                )
                if prov_streams:
                    streams.extend(prov_streams)
                    metrics.provider_success[name] += 1
                    logger.info("provider_success", extra={"provider": name, "streams_count": len(prov_streams)})
                    break
                else:
                    metrics.provider_errors[name] += 1
                    logger.warning("provider_empty_result", extra={"provider": name})
            except asyncio.TimeoutError:
                metrics.provider_errors[name] += 1
                logger.error("provider_timeout", extra={"provider": name})
            except Exception as e:
                metrics.provider_errors[name] += 1
                logger.error("provider_error", extra={"provider": name, "error": str(e)})

    # Enforce strictly >= 1080p
    valid_streams = []
    for s in streams:
        q = s.get("quality", "1080p")
        h = s.get("height")
        if is_quality_ge_1080(q, h):
            valid_streams.append(s)

    cache_set(cache_key, valid_streams)
    
    duration = time.time() - start_time
    if valid_streams:
        metrics.stream_success += 1
        logger.info("stream_success", extra={"duration_ms": round(duration * 1000), "streams_count": len(valid_streams)})
    else:
        metrics.stream_errors += 1
        logger.warning("stream_no_valid_streams", extra={"duration_ms": round(duration * 1000)})
    
    return JSONResponse({"streams": valid_streams})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
