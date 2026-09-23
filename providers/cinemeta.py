"""Resolve a Stremio/Nuvio stream ID to movie/series metadata.

Primary lookup: Cinemeta API (https://v3-cinemeta.strem.io).
Fallback lookup: TMDB / public metadata.
"""
import re
import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Nuvio-Movies-Addon/1.0"
TIMEOUT = 6

_meta_cache: dict[str, dict] = {}


def parse_strem_id(full_id: str) -> tuple[str, int, int]:
    """Split 'tt0903747:1:4' / 'tt0137523' / 'tmdb:1234:1:4' into (base_id, season, episode)."""
    parts = full_id.split(':')
    if len(parts) >= 3 and parts[-2].isdigit() and parts[-1].isdigit():
        season, episode = int(parts[-2]), int(parts[-1])
        base = ':'.join(parts[:-2])
    else:
        base, season, episode = full_id, 1, 1
    return base, season, episode


def clean_title(name: str) -> str:
    """Clean unwanted prefixes/suffixes from title."""
    name = re.sub(r'\s*\(4K\)\s*$', '', name, flags=re.I)
    name = re.sub(r'\s*\(1080p\)\s*$', '', name, flags=re.I)
    return name.strip()


async def get_meta(client: httpx.AsyncClient, base_id: str, content_type: str = "movie") -> dict | None:
    """Fetch title, year, and normalized metadata for a movie or TV series."""
    if base_id in _meta_cache:
        return _meta_cache[base_id]

    types_to_try = [content_type] if content_type in ('series', 'movie') else ['movie', 'series']
    for ctype in types_to_try:
        url = f"https://v3-cinemeta.strem.io/meta/{ctype}/{base_id}.json"
        try:
            r = await client.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
            if r.status_code == 200:
                meta = r.json().get('meta', {})
                name = meta.get('name')
                if name:
                    year_val = meta.get('year') or meta.get('releaseInfo')
                    year = None
                    if year_val:
                        m = re.search(r'(\d{4})', str(year_val))
                        if m:
                            year = int(m.group(1))
                    
                    res = {
                        "base_id": base_id,
                        "imdb_id": meta.get("imdb_id") or (base_id if base_id.startswith("tt") else None),
                        "title": clean_title(name),
                        "year": year,
                        "type": meta.get("type", ctype),
                        "genres": meta.get("genres", []),
                    }
                    _meta_cache[base_id] = res
                    return res
        except Exception:
            continue

    return None
