import asyncio
import re
import httpx

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
HEADERS = {
    'User-Agent': UA,
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
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

def is_quality_ge_1080(width: int | None, height: int | None) -> bool:
    if width and width >= 1920:
        return True
    if height and height >= 1080:
        return True
    # Standard cinema 2.4:1 ratio (1920x800) is 1080p width
    if width and width >= 1900 and height and height >= 750:
        return True
    return False

def parse_manifest_variants(manifest_str: str, ctype: str = "movie") -> list[dict]:
    variants = []
    lines = [l.strip() for l in manifest_str.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            bw_m = re.search(r'BANDWIDTH=(\d+)', line)
            bandwidth = int(bw_m.group(1)) if bw_m else 0
            
            res_m = re.search(r'RESOLUTION=(\d+)x(\d+)', line)
            width = int(res_m.group(1)) if res_m else 0
            height = int(res_m.group(2)) if res_m else 0
            
            if i + 1 < len(lines):
                url = lines[i+1]
                if is_quality_ge_1080(width, height):
                    q_label = "4K" if width >= 3840 or height >= 2160 else "1440p" if width >= 2560 or height >= 1440 else "1080p"
                    variants.append({
                        "quality": q_label,
                        "width": width,
                        "height": height,
                        "bandwidth": bandwidth,
                        "url": url,
                        "size_bytes": estimate_size(bandwidth, ctype)
                    })
    return variants

async def resolve_vidlove(tmdb_id: int | str, ctype: str = "movie", season: int = 1, episode: int = 1, title: str = "", year: int | None = None) -> list[dict]:
    streams = []
    if ctype == "movie":
        url = f"https://api.vidlove.cc/movie?id={tmdb_id}&mode=json"
    else:
        url = f"https://api.vidlove.cc/tv?id={tmdb_id}&season={season}&episode={episode}&mode=json"

    async with httpx.AsyncClient(headers=HEADERS, timeout=8.0) as client:
        try:
            r = await client.get(url)
            if r.status_code != 200:
                # Try fallback with sources=vidapi
                r = await client.get(f"{url}&sources=vidapi")
            if r.status_code != 200:
                return []
            
            data = r.json()
            source = data.get("source") or {}
            manifest = source.get("manifest")
            if not manifest:
                return []
            
            subs = []
            for s in data.get("subtitles", []):
                if s.get("file"):
                    subs.append({
                        "id": s.get("label", "en"),
                        "lang": s.get("label", "English"),
                        "url": s.get("file")
                    })
            
            variants = parse_manifest_variants(manifest, ctype=ctype)
            for v in variants:
                mbps = v["bandwidth"] / 1_000_000 if v["bandwidth"] else 0
                size_str = format_size(v["size_bytes"])
                size_desc = f" • ~{size_str}" if size_str else ""
                
                title_line = f"{title} ({year})" if year else title
                stream_title = f"{title_line}\n{v['quality']} ({v['width']}x{v['height']}) • {mbps:.1f} Mbps{size_desc}\nDirect High-Speed HLS (No buffering)"
                
                streams.append({
                    "name": f"[{v['quality']}] Vidlove",
                    "title": stream_title,
                    "url": v["url"],
                    "quality": v["quality"],
                    "height": v["height"],
                    "width": v["width"],
                    "behaviorHints": {
                        "notWebReady": False,
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": UA,
                                "Referer": "https://player.vidlove.cc/"
                            }
                        }
                    },
                    "subtitles": subs[:20]  # top 20 subtitles
                })
        except Exception as e:
            print(f"Error resolving vidlove: {e}")
            return []
    return streams

async def main():
    # Test Inception (tmdb: 27205)
    print("Testing Inception (movie)...")
    s_movie = await resolve_vidlove(27205, ctype="movie", title="Inception", year=2010)
    print(f"Got {len(s_movie)} streams:")
    for s in s_movie:
        print(f"  Name: {s['name']}")
        print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
        print(f"  URL: {s['url'][:60]}...")
        print(f"  Subtitles count: {len(s['subtitles'])}")

    # Test Breaking Bad (tmdb: 1396) S1E1
    print("\nTesting Breaking Bad (series)...")
    s_tv = await resolve_vidlove(1396, ctype="series", season=1, episode=1, title="Breaking Bad", year=2008)
    print(f"Got {len(s_tv)} streams:")
    for s in s_tv:
        print(f"  Name: {s['name']}")
        print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
        print(f"  URL: {s['url'][:60]}...")

if __name__ == "__main__":
    asyncio.run(main())
