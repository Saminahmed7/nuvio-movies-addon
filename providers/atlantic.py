"""Atlantic / Stellar provider for Nuvio/Stremio Movies & TV Addon.

Features:
- Direct HLS Streams via stellar.hls.lol resolver
- Supports Movies and TV Series
- 4K, 1440p, 1080p quality
"""
import re
import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://atlantic.st/",
    "Origin": "https://atlantic.st"
}
TIMEOUT = 8.0
RESOLVER_URL = "https://stellar.hls.lol/resolve"
CDN_BASE = "https://cdn.hls.lol"


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


def is_ge_1080(width: int, height: int) -> bool:
    if width >= 1900:
        return True
    if height >= 1080:
        return True
    return False


def parse_variants(manifest: str, ctype: str = "movie") -> list[dict]:
    variants = []
    lines = [line.strip() for line in manifest.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            bw_m = re.search(r"BANDWIDTH=(\d+)", line)
            bandwidth = int(bw_m.group(1)) if bw_m else 0

            res_m = re.search(r"RESOLUTION=(\d+)x(\d+)", line)
            width = int(res_m.group(1)) if res_m else 0
            height = int(res_m.group(2)) if res_m else 0

            if i + 1 < len(lines):
                var_url = lines[i + 1]
                if is_ge_1080(width, height):
                    q_label = "4K" if width >= 3840 or height >= 2160 else "1440p" if width >= 2560 or height >= 1440 else "1080p"
                    variants.append({
                        "quality": q_label,
                        "width": width,
                        "height": height,
                        "bandwidth": bandwidth,
                        "url": var_url,
                        "size_bytes": estimate_size(bandwidth, ctype)
                    })
    return variants


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | None = None
) -> list[dict]:
    if not tmdb_id:
        return []

    params = {
        "tmdbId": str(tmdb_id),
        "type": ctype
    }
    if ctype == "series":
        params["season"] = str(season)
        params["episode"] = str(episode)

    streams = []
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            # Step 1: Resolve to get the proxy URL
            r = await client.get(RESOLVER_URL, params=params)
            if r.status_code != 200:
                return []

            data = r.json()
            if not data.get("found") or not data.get("url"):
                return []

            proxy_url = data["url"]

            # Step 2: Fetch the master playlist from the proxy
            r2 = await client.get(proxy_url, follow_redirects=True)
            if r2.status_code != 200:
                return []

            manifest = r2.text

            # Extract subtitles from Atlantic (if available)
            subs = []
            # Atlantic might provide subtitles in the response or we can fetch separately
            # For now, we'll skip subtitle extraction for Atlantic

            variants = parse_variants(manifest, ctype=ctype)
            for v in variants:
                mbps = v["bandwidth"] / 1_000_000 if v["bandwidth"] else 0
                size_str = format_size(v["size_bytes"])
                size_desc = f" • ~{size_str}" if size_str else ""

                title_line = f"{title} ({year})" if year else title
                stream_title = (
                    f"{title_line}\n"
                    f"{v['quality']} ({v['width']}x{v['height']}) • {mbps:.1f} Mbps{size_desc}\n"
                    f"Direct High-Speed HLS via Atlantic"
                )

                stream_item = {
                    "name": f"[{v['quality']}] Atlantic",
                    "title": stream_title,
                    "url": v["url"],
                    "quality": v["quality"],
                    "height": v["height"],
                    "width": v["width"],
                    "size": v["size_bytes"],
                    "behaviorHints": {
                        "notWebReady": False,
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": UA,
                                "Referer": "https://atlantic.st/"
                            }
                        }
                    }
                }
                if subs:
                    stream_item["subtitles"] = subs[:25]

                streams.append(stream_item)
    except Exception as e:
        print(f"[Atlantic] Resolution error: {e}")
        return []

    return streams