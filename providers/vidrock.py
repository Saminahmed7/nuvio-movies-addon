"""Vidrock provider for Nuvio/Stremio Movies & TV Addon.

Features:
- Multiple server sources (Atlas, Luna, Orion)
- AES-GCM decryption of stream URLs
- Direct HLS Streams >= 1080p
- Supports Movies and TV Series
"""
import base64
import re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://vidrock.net/",
    "Origin": "https://vidrock.net"
}
TIMEOUT = 10.0

# Vidrock AES-GCM key (from reverse engineering)
KEY_HEX = "7f3e9c2a8b5d1f4e6a9c3b7d2e5f8a1c4b6d9e2f5a8c1b4d7e9f2a5c8b1d4e7f"
KEY = bytes.fromhex(KEY_HEX)
AESGCM_CIPHER = AESGCM(KEY)

# Server priority order (best first)
SERVER_PRIORITY = ["Atlas", "Luna", "Orion", "Nova", "Astra"]


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


def decrypt_vidrock(enc_str: str) -> str | None:
    """Decrypt Vidrock AES-GCM encrypted URL."""
    if not enc_str:
        return None
    try:
        # base64url decode
        rem = len(enc_str) % 4
        if rem == 2:
            enc_str += "=="
        elif rem == 3:
            enc_str += "="
        raw = base64.urlsafe_b64decode(enc_str)
        if len(raw) < 28:
            return None
        iv = raw[:12]
        ciphertext_and_tag = raw[12:]
        dec = AESGCM_CIPHER.decrypt(iv, ciphertext_and_tag, None)
        return dec.decode("utf-8")
    except Exception:
        return None


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


async def _fetch_manifest(client: httpx.AsyncClient, m3u8_url: str) -> str | None:
    """Fetch HLS master manifest with proper headers."""
    try:
        r = await client.get(m3u8_url, headers={"User-Agent": UA, "Referer": "https://vidrock.net/"}, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code == 200 and "#EXTM3U" in r.text:
            return r.text
    except Exception:
        pass
    return None


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

    if ctype == "movie":
        url = f"https://vidrock.net/api/movie/{tmdb_id}"
    else:
        url = f"https://vidrock.net/api/tv/{tmdb_id}/{season}/{episode}"

    streams = []
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
            r = await client.get(url)
            if r.status_code != 200:
                return []

            data = r.json()

            # Try servers in priority order
            for server_name in SERVER_PRIORITY:
                server_data = data.get(server_name)
                if not server_data or not isinstance(server_data, dict):
                    continue
                enc_url = server_data.get("url")
                if not enc_url:
                    continue

                decrypted_url = decrypt_vidrock(enc_url)
                if not decrypted_url:
                    continue

                # Fetch and parse master manifest
                manifest = await _fetch_manifest(client, decrypted_url)
                if not manifest:
                    continue

                variants = parse_variants(manifest, ctype=ctype)
                if not variants:
                    continue

                # Extract language info
                lang = server_data.get("language", "English")
                flag = server_data.get("flag", "us")

                for v in variants:
                    mbps = v["bandwidth"] / 1_000_000 if v["bandwidth"] else 0
                    size_str = format_size(v["size_bytes"])
                    size_desc = f" • ~{size_str}" if size_str else ""

                    title_line = f"{title} ({year})" if year else title
                    stream_title = (
                        f"{title_line}\n"
                        f"{v['quality']} ({v['width']}x{v['height']}) • {mbps:.1f} Mbps{size_desc}\n"
                        f"Vidrock {server_name} ({lang})"
                    )

                    stream_item = {
                        "name": f"[{v['quality']}] Vidrock {server_name}",
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
                                    "Referer": "https://vidrock.net/"
                                }
                            }
                        }
                    }
                    streams.append(stream_item)

    except Exception as e:
        print(f"[Vidrock] Resolution error: {e}")
        return []

    return streams