"""VideoEasy provider for Nuvio/Stremio Movies & TV Addon.

Features:
- Fast multi-server extraction via speedracelight CDN & enc-dec.app
- 4K (2160p) and 1080p direct Cloudflare HLS streams
- Full subtitle extraction (VTT)
- Zero buffering with fast Cloudflare edge delivery
- Supports both Movies and TV Series
"""
import asyncio
import re
import logging
from urllib.parse import quote
import httpx

logger = logging.getLogger("nuvio-movies-addon")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
PLAYER_ORIGIN = "https://player.videasy.to"
HEADERS = {
    "Accept": "*/*",
    "Origin": PLAYER_ORIGIN,
    "Referer": f"{PLAYER_ORIGIN}/",
    "User-Agent": UA
}

TIMEOUT = 6.0
SEED_URL = "https://api.speedracelight.com/seed?mediaId={tmdb_id}"
API_BASE = "https://api.speedracelight.com"
DEC_API = "https://enc-dec.app/api/dec-videasy"

QUALITY_MAP = {
    "2160p": ("4K", 3840, 2160, 15_000_000),
    "4k": ("4K", 3840, 2160, 15_000_000),
    "1440p": ("1440p", 2560, 1440, 9_000_000),
    "2k": ("1440p", 2560, 1440, 9_000_000),
    "1080p": ("1080p", 1920, 1080, 5_500_000),
}


def format_size(bytes_val: int | float | None) -> str | None:
    if not bytes_val or bytes_val <= 0:
        return None
    gb = bytes_val / (1024 ** 3)
    if gb >= 1.0:
        return f"{gb:.2f} GB"
    mb = bytes_val / (1024 ** 2)
    return f"{int(mb)} MB"


def estimate_size(bandwidth_bps: int | None, ctype: str = "movie") -> int | None:
    if not bandwidth_bps or bandwidth_bps <= 0:
        return None
    duration_s = 6300 if ctype == "movie" else 2700
    return int((duration_s * bandwidth_bps) / 8)


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | str | None = None
) -> list[dict]:
    """Resolve >= 1080p streams from Videasy."""
    if not tmdb_id or not title:
        return []

    streams: list[dict] = []
    enc_title = quote(quote(str(title).strip(), safe=""), safe="")
    yr_str = str(year) if year else ""
    str_tmdb = str(tmdb_id)

    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            # 1. Fetch seed
            seed_res = await client.get(SEED_URL.format(tmdb_id=str_tmdb))
            if seed_res.status_code != 200:
                return []
            seed_data = seed_res.json()
            seed = seed_data.get("seed")
            if not seed:
                return []

            # 2. Query CDN (Yoru - 4K/1080p) and m4uhd (Breach - Subs) in parallel
            async def _fetch_server(srv: str) -> dict:
                if ctype == "movie":
                    url = f"{API_BASE}/{srv}/sources-with-title?title={enc_title}&mediaType=movie&year={yr_str}&tmdbId={str_tmdb}&enc=2&seed={seed}"
                else:
                    url = f"{API_BASE}/{srv}/sources-with-title?title={enc_title}&mediaType=tv&year={yr_str}&episodeId={episode}&seasonId={season}&tmdbId={str_tmdb}&enc=2&seed={seed}"
                try:
                    r = await client.get(url)
                    if r.status_code == 200 and len(r.text) > 20:
                        dec = await client.post(DEC_API, json={"text": r.text, "id": str_tmdb, "seed": seed})
                        if dec.status_code == 200:
                            return dec.json().get("result", {})
                except Exception:
                    pass
                return {}

            cdn_res, m4_res = await asyncio.gather(_fetch_server("cdn"), _fetch_server("m4uhd"))

            # Extract subtitles from m4uhd or cdn if present
            subs: list[dict] = []
            raw_subs = m4_res.get("subtitles") or cdn_res.get("subtitles") or []
            for s in raw_subs:
                sub_url = s.get("url")
                if sub_url and isinstance(sub_url, str):
                    lang = s.get("language") or s.get("lang") or "English"
                    subs.append({
                        "id": lang.lower().replace(" ", "_"),
                        "lang": lang,
                        "url": sub_url
                    })

            # Process sources from cdn (Yoru)
            sources = cdn_res.get("sources") or []
            for src in sources:
                raw_q = str(src.get("quality", "")).lower().strip()
                s_url = src.get("url")
                if not s_url or raw_q not in QUALITY_MAP:
                    continue

                q_label, width, height, bandwidth = QUALITY_MAP[raw_q]
                size_b = estimate_size(bandwidth, ctype)
                size_str = format_size(size_b)
                mbps = bandwidth / 1_000_000

                title_line = f"{title} ({year})" if year else title
                if ctype == "tv":
                    title_line = f"{title} S{season:02d}E{episode:02d}"

                stream_title = (
                    f"{title_line}\n"
                    f"{q_label} ({width}x{height}) • {mbps:.1f} Mbps • ~{size_str}\n"
                    f"Videasy Yoru (Cloudflare HLS)"
                )

                stream_item = {
                    "name": f"[{q_label}] Videasy",
                    "title": stream_title,
                    "url": s_url,
                    "quality": q_label,
                    "height": height,
                    "width": width,
                    "size": size_b,
                    "behaviorHints": {
                        "notWebReady": False,
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": UA,
                                "Origin": PLAYER_ORIGIN,
                                "Referer": f"{PLAYER_ORIGIN}/"
                            }
                        }
                    }
                }
                if subs:
                    stream_item["subtitles"] = subs

                streams.append(stream_item)

            # Sort: 4K first, then 1080p
            quality_rank = {"4K": 0, "1440p": 1, "1080p": 2}
            streams.sort(key=lambda x: quality_rank.get(x.get("quality"), 99))

    except Exception as e:
        logger.warning("videasy_resolve_error", extra={"error": str(e), "tmdb_id": tmdb_id})

    return streams