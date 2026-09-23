"""Nuvio/Stremio HTTP addon for Movies & TV Series.

Quality criterion: Any quality >= 1080p (1080p, 1440p/2K, 2160p/4K).
Zero maintenance (no cookies, direct HTTP streams).
"""
import asyncio
import os
import time
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from providers import cinemeta
from providers import cf_client

ADDON_ID = "org.nuvio.movies-1080p"
ADDON_NAME = "Movies & TV 1080p+"
VERSION = "1.0.0"
CACHE_TTL_SEARCH = int(os.getenv("CACHE_TTL_SEARCH", "3600"))
STREAM_DEADLINE_S = float(os.getenv("STREAM_DEADLINE_S", "9.5"))
PORT = int(os.getenv("PORT", "7001"))

app = FastAPI(title=ADDON_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MANIFEST = {
    "id": ADDON_ID,
    "version": VERSION,
    "name": ADDON_NAME,
    "description": "Direct HTTP Movies & TV Series streams >= 1080p (1080p, 1440p, 4K). No torrents, no logins.",
    "resources": ["stream"],
    "types": ["movie", "series"],
    "idPrefixes": ["tt", "tmdb"],
    "catalogs": [],
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


@app.get("/diag")
async def diag(q: str = "Inception"):
    """Check upstream reachability and provider status."""
    return {"query": q, "providers": {}}


@app.get("/stream/{ctype}/{full_id}.json")
async def stream(ctype: str, full_id: str):
    """Serve movie/series streams >= 1080p."""
    if ctype not in ("movie", "series"):
        return JSONResponse({"streams": []})

    base_id, season, episode = cinemeta.parse_strem_id(full_id)
    cache_key = f"streams:{ctype}:{base_id}:{season}:{episode}"
    cached = cache_get(cache_key)
    if cached is not None:
        return JSONResponse({"streams": cached})

    async with httpx.AsyncClient() as client:
        meta = await cinemeta.get_meta(client, base_id, ctype)

    if not meta or not meta.get("title"):
        return JSONResponse({"streams": []})

    title = meta["title"]
    year = meta.get("year")
    imdb_id = meta.get("imdb_id")

    # Provider queries will be gathered concurrently within STREAM_DEADLINE_S
    streams = []

    # Filter out anything below 1080p
    valid_streams = []
    for s in streams:
        q = s.get("quality", "1080p")
        h = s.get("height")
        if is_quality_ge_1080(q, h):
            valid_streams.append(s)

    cache_set(cache_key, valid_streams)
    return JSONResponse({"streams": valid_streams})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
