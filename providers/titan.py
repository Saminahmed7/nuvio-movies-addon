"""Titan VII provider for Nuvio/Stremio Movies & TV Addon.

Features:
- Direct 1080p MP4 streams via FrameX TV (Films365 source)
- Native subtitle tracks (VTT)
- Supports both Movies and TV Series
"""
import logging

import httpx

logger = logging.getLogger("nuvio-movies-addon")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
HEADERS = {
    "Accept": "application/json",
    "Origin": "https://framextv.xyz",
    "Referer": "https://framextv.xyz/",
    "User-Agent": UA,
}
TIMEOUT = 7.0
API_BASES = [
    "https://api.framextv.xyz",
    "https://api.framextv.cc",
    "https://api.framextv.tech",
]
PROVIDER = "titan"

QUALITY_MAP = {
    "2160p": ("4K", 3840, 2160),
    "4k": ("4K", 3840, 2160),
    "uhd": ("4K", 3840, 2160),
    "1440p": ("1440p", 2560, 1440),
    "2k": ("1440p", 2560, 1440),
    "1080p": ("1080p", 1920, 1080),
    "fhd": ("1080p", 1920, 1080),
}


def quality_meta(raw_quality: str | None) -> tuple[str, int, int] | None:
    q = str(raw_quality or "").strip().lower()
    if q in QUALITY_MAP:
        return QUALITY_MAP[q]
    digits = "".join(ch for ch in q if ch.isdigit())
    if digits.isdigit():
        height = int(digits)
        if height >= 2160:
            return ("4K", 3840, height)
        if height >= 1440:
            return ("1440p", 2560, height)
        if height >= 1080:
            return ("1080p", 1920, height)
    return None


def parse_subtitles(raw_subs: list | None) -> list[dict]:
    subs: list[dict] = []
    seen: set[str] = set()
    for s in raw_subs or []:
        if not isinstance(s, dict):
            continue
        sub_url = s.get("url")
        if not sub_url or not isinstance(sub_url, str) or sub_url in seen:
            continue
        seen.add(sub_url)
        lang = s.get("language") or s.get("lang") or s.get("label") or "English"
        subs.append({
            "id": str(lang).lower().replace(" ", "_"),
            "lang": lang,
            "url": sub_url,
        })
    return subs[:25]


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | str | None = None
) -> list[dict]:
    """Resolve >= 1080p streams from Titan VII."""
    if not tmdb_id:
        return []

    media_type = "movie" if ctype == "movie" else "tv"
    params = {
        "type": media_type,
        "id": str(tmdb_id),
        "provider": PROVIDER,
    }
    if media_type == "tv":
        params["season"] = str(season)
        params["episode"] = str(episode)

    data = {}
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            for base in API_BASES:
                try:
                    r = await client.get(f"{base}/api/stream", params=params)
                    if r.status_code != 200:
                        continue
                    body = r.json()
                    if body.get("success") and body.get("sources"):
                        data = body
                        break
                except Exception:
                    continue
    except Exception as e:
        logger.warning("titan_resolve_error", extra={"error": str(e), "tmdb_id": tmdb_id})
        return []

    if not data:
        return []

    subs = parse_subtitles(data.get("subtitles"))
    title_line = f"{title} ({year})" if year else title
    if media_type == "tv":
        title_line = f"{title} S{season:02d}E{episode:02d}"

    streams: list[dict] = []
    for src in data.get("sources") or []:
        if not isinstance(src, dict):
            continue
        url = src.get("url")
        meta = quality_meta(src.get("quality"))
        if not url or not isinstance(url, str) or not meta:
            continue

        q_label, width, height = meta
        server = src.get("server") or "Titan VII"
        stream_type = str(src.get("type") or "mp4").upper()

        stream_item = {
            "name": f"[{q_label}] {server}",
            "title": (
                f"{title_line}\n"
                f"{q_label} ({width}x{height}) • {stream_type} • Titan VII\n"
                f"Films365 Direct (No buffering)"
            ),
            "url": url,
            "quality": q_label,
            "height": height,
            "width": width,
            "behaviorHints": {
                "notWebReady": False,
                "proxyHeaders": {
                    "request": {
                        "User-Agent": UA,
                        "Referer": "https://www.films365.org/",
                        "Origin": "https://www.films365.org",
                    }
                },
            },
        }
        if subs:
            stream_item["subtitles"] = subs

        streams.append(stream_item)

    quality_rank = {"4K": 0, "1440p": 1, "1080p": 2}
    streams.sort(key=lambda x: quality_rank.get(x.get("quality"), 99))
    return streams
