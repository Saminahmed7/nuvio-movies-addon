import asyncio
import base64
import re
from urllib.parse import quote, urljoin
import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
ORIGIN = "https://cinejoy.pk"
HEADERS = {
    "Accept": "*/*",
    "Origin": ORIGIN,
    "Referer": f"{ORIGIN}/",
    "User-Agent": UA
}

TIMEOUT = 6.0
WING_BASE = "https://api.wing.st"
ENC_API = "https://enc-dec.app/api/enc-cinejoy"
DEC_API = "https://enc-dec.app/api/dec-cinejoy"
SUB_BASE_MOVIE = "https://sub.vdrk.site/v1/movie/"
SUB_BASE_TV = "https://sub.vdrk.site/v1/tv/"

SERVERS = ["Lisbon", "Nebula"]

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def base64url_decode(data: str) -> bytes:
    data += "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data)

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
    return width >= 1900 or height >= 1080

def parse_variants(manifest: str, base_url: str, ctype: str = "movie") -> list[dict]:
    variants = []
    lines = [line.strip() for line in manifest.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF:"):
            res_match = re.search(r"RESOLUTION=(\d+)x(\d+)", line)
            bw_match = re.search(r"BANDWIDTH=(\d+)", line)
            if not res_match:
                continue
            width = int(res_match.group(1))
            height = int(res_match.group(2))
            bandwidth = int(bw_match.group(1)) if bw_match else 5_000_000

            if i + 1 < len(lines):
                var_url = lines[i + 1]
                if not var_url.startswith("#") and is_ge_1080(width, height):
                    full_url = urljoin(base_url, var_url)
                    q_label = "4K" if width >= 3840 or height >= 2160 else "1440p" if width >= 2560 or height >= 1440 else "1080p"
                    variants.append({
                        "quality": q_label,
                        "width": width,
                        "height": height,
                        "bandwidth": bandwidth,
                        "url": full_url,
                        "size_bytes": estimate_size(bandwidth, ctype)
                    })
    return variants

async def fetch_subtitles(client: httpx.AsyncClient, tmdb_id: str, ctype: str, season: int = 1, episode: int = 1) -> list[dict]:
    subs = []
    try:
        url = f"{SUB_BASE_MOVIE}{tmdb_id}" if ctype == "movie" else f"{SUB_BASE_TV}{tmdb_id}/{season}/{episode}"
        r = await client.get(url, timeout=3.0)
        if r.status_code == 200:
            for s in r.json():
                lang = s.get("label") or s.get("language") or "English"
                file_url = s.get("file") or s.get("url")
                if file_url and (".vtt" in file_url or ".srt" in file_url):
                    subs.append({
                        "id": lang.lower().replace(" ", "_"),
                        "lang": lang,
                        "url": file_url
                    })
    except Exception:
        pass
    return subs

async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | str | None = None
) -> list[dict]:
    if not tmdb_id or not title:
        return []

    streams: list[dict] = []
    str_tmdb = str(tmdb_id)
    yr_str = str(year) if year else ""
    enc_title = quote(str(title).strip())
    media_type = "movie" if ctype == "movie" else "series"

    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            subs_task = asyncio.create_task(fetch_subtitles(client, str_tmdb, ctype, season, episode))

            async def _fetch_server(server_name: str) -> list[dict]:
                server_streams = []
                if ctype == "movie":
                    url = f"{WING_BASE}/?title={enc_title}&type=movie&year={yr_str}&tmdb={str_tmdb}&server={server_name}"
                else:
                    url = f"{WING_BASE}/?title={enc_title}&type=series&year={yr_str}&tmdb={str_tmdb}&server={server_name}&season={season}&episode={episode}"

                try:
                    enc_r = await client.get(f"{ENC_API}?url={quote(url)}")
                    if enc_r.status_code != 200:
                        return []
                    enc_json = enc_r.json()
                    if enc_json.get("status") != 200:
                        return []
                    data = enc_json["result"]["data"]
                    state = enc_json["result"]["state"]

                    g_res = await client.post(f"{WING_BASE}/g", content=base64url_decode(data))
                    if g_res.status_code != 200 or len(g_res.content) == 0:
                        return []

                    dec_r = await client.post(DEC_API, json={"text": base64url_encode(g_res.content), "state": state})
                    if dec_r.status_code != 200:
                        return []
                    dec_json = dec_r.json()
                    stream_items = dec_json.get("result", {}).get("data", {}).get("stream", [])

                    for item in stream_items:
                        playlist_url = item.get("playlist")
                        if not playlist_url or not playlist_url.startswith("http"):
                            continue

                        # Fetch master playlist
                        pl_res = await client.get(playlist_url)
                        if pl_res.status_code != 200:
                            continue
                        manifest_text = pl_res.text
                        if "transcoding on node" in manifest_text:
                            continue

                        variants = parse_variants(manifest_text, playlist_url, ctype=ctype)
                        for v in variants:
                            mbps = v["bandwidth"] / 1_000_000
                            size_str = format_size(v["size_bytes"])
                            title_line = f"{title} ({year})" if year else title
                            if ctype == "tv" or ctype == "series":
                                title_line = f"{title} S{season:02d}E{episode:02d}"

                            stream_title = (
                                f"{title_line}\n"
                                f"{v['quality']} ({v['width']}x{v['height']}) • {mbps:.1f} Mbps • ~{size_str}\n"
                                f"Cinejoy {server_name} (HLS)"
                            )

                            server_streams.append({
                                "name": f"[{v['quality']}] Cinejoy {server_name}",
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
                                            "Origin": ORIGIN,
                                            "Referer": f"{ORIGIN}/"
                                        }
                                    }
                                }
                            })
                except Exception:
                    pass
                return server_streams

            # Fetch Lisbon and Nebula in parallel
            res_lists = await asyncio.gather(_fetch_server("Lisbon"), _fetch_server("Nebula"))
            for s_list in res_lists:
                streams.extend(s_list)

            # Attach subtitles
            subs = await subs_task
            if subs:
                for s in streams:
                    s["subtitles"] = subs

    except Exception:
        pass

    return streams

async def main():
    print("Testing Fight Club...")
    m_streams = await resolve(550, "movie", title="Fight Club", year=1999)
    print("Fight Club streams:", len(m_streams))
    for s in m_streams:
        print(" ", s["name"], s["quality"], s["url"][:60], "subs:", len(s.get("subtitles", [])))

    print("\nTesting Fallout S01E01...")
    tv_streams = await resolve(106379, "series", season=1, episode=1, title="Fallout", year=2024)
    print("Fallout streams:", len(tv_streams))
    for s in tv_streams:
        print(" ", s["name"], s["quality"], s["url"][:60], "subs:", len(s.get("subtitles", [])))

if __name__ == "__main__":
    asyncio.run(main())
