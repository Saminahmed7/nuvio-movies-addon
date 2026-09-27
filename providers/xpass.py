import asyncio
import base64
import hashlib
import json
import logging
import re
from urllib.parse import urljoin
import httpx
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger("nuvio-movies-addon")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
ORIGIN = "https://play.xpass.top"
HEADERS = {
    "Accept": "*/*",
    "Origin": ORIGIN,
    "Referer": f"{ORIGIN}/",
    "User-Agent": UA,
}

TIMEOUT = 5.0
BUILD_ID = "spv3-build-1787821613-50e5fc97c9dce367"
SUB_BASE_MOVIE = "https://sub.vdrk.site/v1/movie/"
SUB_BASE_TV = "https://sub.vdrk.site/v1/tv/"

# Preferred high-bitrate servers to probe from the 28-60 servers returned
PRIORITY_SERVERS = ["TIK", "VIP", "FIL", "WIS"]


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
    if not tmdb_id:
        return []

    streams: list[dict] = []
    str_tmdb = str(tmdb_id)
    page_url = f"{ORIGIN}/e/movie/{str_tmdb}" if ctype == "movie" else f"{ORIGIN}/e/tv/{str_tmdb}/{season}/{episode}"

    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            subs_task = asyncio.create_task(fetch_subtitles(client, str_tmdb, ctype, season, episode))

            # 1. Fetch embed page
            embed_res = await client.get(page_url)
            if embed_res.status_code != 200:
                return []

            m_data_url = re.search(r'var dataUrl="([^"]+)"', embed_res.text)
            if not m_data_url:
                return []

            data_url = m_data_url.group(1)
            data_path = data_url.split("?")[0]
            m_token = re.search(r'token=([^&]+)', data_url)
            token = m_token.group(1) if m_token else ""

            # 2. Derive decryption key: SHA-256("spv3-data-response|{BUILD_ID}|{data_path}|{token}")
            key_seed = f"spv3-data-response|{BUILD_ID}|{data_path}|{token}"
            key = hashlib.sha256(key_seed.encode("utf-8")).digest()

            # 3. Fetch encrypted server list
            enc_res = await client.get(
                urljoin(ORIGIN, data_url),
                headers={**HEADERS, "Referer": page_url}
            )
            if enc_res.status_code != 200:
                return []

            enc_text = enc_res.text.strip().replace("-", "+").replace("_", "/")
            enc_text += "=" * (-len(enc_text) % 4)
            raw_bytes = base64.b64decode(enc_text)
            if len(raw_bytes) < 28:
                return []

            iv = raw_bytes[:12]
            ciphertext_and_tag = raw_bytes[12:]
            aesgcm = AESGCM(key)
            decrypted_json_bytes = aesgcm.decrypt(iv, ciphertext_and_tag, None)
            servers = json.loads(decrypted_json_bytes.decode("utf-8"))

            # Pick prioritized servers (up to 4)
            selected_servers = []
            for prefix in PRIORITY_SERVERS:
                for s in servers:
                    s_name = s.get("name", "")
                    if s_name.startswith(prefix) and s.get("url") and not s.get("dl"):
                        selected_servers.append(s)
                        break
            if not selected_servers:
                selected_servers = [s for s in servers if s.get("url") and not s.get("dl")][:4]

            # 4. Resolve playlists in parallel
            async def _fetch_playlist(server_info: dict) -> list[dict]:
                s_streams = []
                s_name = server_info.get("name", "XPass")
                rel_url = server_info.get("url", "")
                try:
                    pl_json_res = await client.get(urljoin(ORIGIN, rel_url), headers={**HEADERS, "Referer": page_url})
                    if pl_json_res.status_code != 200:
                        return []
                    pl_data = pl_json_res.json()
                    playlists = pl_data.get("playlist", [])
                    for p in playlists:
                        sources = p.get("sources", [])
                        for src in sources:
                            stream_file = src.get("file", "")
                            if not stream_file.startswith("http"):
                                continue

                            manifest_res = await client.get(stream_file, headers=HEADERS)
                            if manifest_res.status_code != 200:
                                continue

                            variants = parse_variants(manifest_res.text, stream_file, ctype=ctype)
                            for v in variants:
                                mbps = v["bandwidth"] / 1_000_000
                                size_str = format_size(v["size_bytes"])
                                title_line = f"{title} ({year})" if year else title
                                if ctype == "tv" or ctype == "series":
                                    title_line = f"{title} S{season:02d}E{episode:02d}"

                                stream_title = (
                                    f"{title_line}\n"
                                    f"{v['quality']} ({v['width']}x{v['height']}) • {mbps:.1f} Mbps • ~{size_str}\n"
                                    f"XPass {s_name} (HLS)"
                                )

                                s_streams.append({
                                    "name": f"[{v['quality']}] XPass {s_name}",
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
                except Exception as ex:
                    logger.debug("XPass server %s error: %s", s_name, ex)
                return s_streams

            pl_lists = await asyncio.gather(*[_fetch_playlist(s) for s in selected_servers])
            for p_list in pl_lists:
                streams.extend(p_list)

            # Attach subtitles
            subs = await subs_task
            if subs:
                for s in streams:
                    s["subtitles"] = subs

    except Exception as e:
        logger.error("XPass resolve error for tmdb %s: %s", tmdb_id, e)

    return streams


async def main():
    print("Testing XPass Movie (Fight Club)...")
    m_streams = await resolve(550, "movie", title="Fight Club", year=1999)
    print("Fight Club streams:", len(m_streams))
    for s in m_streams:
        print(" ", s["name"], s["quality"], s["url"][:60], "subs:", len(s.get("subtitles", [])))

    print("\nTesting XPass TV (Fallout S01E01)...")
    tv_streams = await resolve(106379, "series", season=1, episode=1, title="Fallout", year=2024)
    print("Fallout streams:", len(tv_streams))
    for s in tv_streams:
        print(" ", s["name"], s["quality"], s["url"][:60], "subs:", len(s.get("subtitles", [])))


if __name__ == "__main__":
    asyncio.run(main())
