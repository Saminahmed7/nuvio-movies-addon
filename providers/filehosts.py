"""File host extractors for Nuvio/Stremio Movies & TV Addon.

Ports CSX CloudStream extractors to Python.
Extracts direct video stream URLs from file hosting services.
All free - no debrid services required.
"""
import re
import httpx
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 10.0


def get_base_url(url: str) -> str:
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return url


def get_quality(text: str) -> str:
    if not text:
        return "1080p"
    match = re.search(r'(\d{3,4})[pP]', text)
    if match:
        return f"{match.group(1)}p"
    lower = text.lower()
    if '4k' in lower or '2160' in lower:
        return '4K'
    if '2k' in lower or '1440' in lower:
        return '1440p'
    if '1080' in lower:
        return '1080p'
    if '720' in lower:
        return '720p'
    if '480' in lower:
        return '480p'
    return '1080p'


async def extract_fastdlserver(url: str, client: httpx.AsyncClient) -> list[dict]:
    """FastDLServer: Simple redirect - follow Location header."""
    streams = []
    try:
        r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=False)
        location = r.headers.get('location', '')
        if location:
            if not location.startswith('http'):
                location = get_base_url(url) + location
            streams.append({
                "name": "[1080p] FastDLServer",
                "url": location,
                "quality": "1080p",
            })
    except Exception:
        pass
    return streams


async def extract_gdflix(url: str, client: httpx.AsyncClient) -> list[dict]:
    """GDFlix/GDLink: Parse HTML for download buttons."""
    streams = []
    try:
        r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        base_url = get_base_url(str(r.url))

        file_name = ""
        name_elem = soup.select_one('ul > li.list-group-item:contains("Name")')
        if name_elem:
            file_name = name_elem.get_text().replace("Name : ", "").strip()
        quality = get_quality(file_name)

        buttons = soup.select('div.text-center a')
        for btn in buttons:
            text = btn.get_text(strip=True)
            link = btn.get('href', '')
            if not link:
                continue

            if any(k in text for k in ['FSL V2', 'DIRECT DL', 'DIRECT SERVER', 'CLOUD DOWNLOAD']):
                streams.append({
                    "name": f"[{quality}] GDFlix {text}",
                    "url": link if link.startswith('http') else base_url + link,
                    "quality": quality,
                })
            elif 'FAST CLOUD' in text:
                try:
                    r2 = await client.get(base_url + link, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
                    if r2.status_code == 200:
                        soup2 = BeautifulSoup(r2.text, 'html.parser')
                        dlink = soup2.select_one('div.card-body a')
                        if dlink and dlink.get('href'):
                            streams.append({
                                "name": f"[{quality}] GDFlix FastCloud",
                                "url": dlink['href'],
                                "quality": quality,
                            })
                except Exception:
                    pass
            elif 'Instant DL' in text:
                try:
                    r2 = await client.get(link, headers=HEADERS, timeout=TIMEOUT, follow_redirects=False)
                    location = r2.headers.get('location', '')
                    if location:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(location)
                        params = parse_qs(parsed.query)
                        instant_link = params.get('url', [''])[0]
                        if instant_link:
                            streams.append({
                                "name": f"[{quality}] GDFlix Instant",
                                "url": instant_link,
                                "quality": quality,
                            })
                except Exception:
                    pass
    except Exception:
        pass
    return streams


async def extract_hubcloud(url: str, client: httpx.AsyncClient) -> list[dict]:
    """HubCloud/VCloud: Extract URLs from JavaScript variables."""
    streams = []
    try:
        r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        text = r.text

        # Try to find direct m3u8/mp4 URLs in JavaScript
        urls = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)[^\s"\'<>]*', text)
        for u in urls:
            streams.append({
                "name": "[1080p] HubCloud",
                "url": u,
                "quality": "1080p",
            })

        if streams:
            return streams

        # Try double atob pattern
        b64_matches = re.findall(r"atob\(atob\(['\"]([^'\"]+)['\"]\)\)", text)
        for b64 in b64_matches:
            try:
                import base64
                decoded = base64.b64decode(base64.b64decode(b64)).decode('utf-8')
                if decoded.startswith('http'):
                    streams.append({
                        "name": "[1080p] HubCloud",
                        "url": decoded,
                        "quality": "1080p",
                    })
            except Exception:
                pass

        # Try var url = '...' pattern
        var_matches = re.findall(r"var\s+url\s*=\s*['\"]([^'\"]+)['\"]", text)
        for u in var_matches:
            if u.startswith('http'):
                streams.append({
                    "name": "[1080p] HubCloud",
                    "url": u,
                    "quality": "1080p",
                })

        # Parse HTML for download buttons
        soup = BeautifulSoup(text, 'html.parser')
        buttons = soup.select('h2 a.btn, div.text-center a')
        for btn in buttons:
            text_btn = btn.get_text(strip=True)
            link = btn.get('href', '')
            if not link:
                continue
            if any(k in text_btn.lower() for k in ['fsl', 'mega', 'buzz', 'direct']):
                streams.append({
                    "name": f"[1080p] HubCloud {text_btn}",
                    "url": link,
                    "quality": "1080p",
                })

    except Exception:
        pass
    return streams


async def extract_driveleech(url: str, client: httpx.AsyncClient) -> list[dict]:
    """Driveleech/Driveseed: Parse HTML for download links."""
    streams = []
    try:
        r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        base_url = get_base_url(str(r.url))

        # Find download buttons
        buttons = soup.select('div.text-center > a')
        for btn in buttons:
            text = btn.get_text(strip=True)
            link = btn.get('href', '')
            if not link:
                continue

            if any(k in text.lower() for k in ['cloud', 'instant', 'resume', 'direct']):
                streams.append({
                    "name": f"[1080p] Driveleech {text}",
                    "url": link if link.startswith('http') else base_url + link,
                    "quality": "1080p",
                })

        # Also check for direct m3u8/mp4 links in page
        import re as _re
        urls = _re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)[^\s"\'<>]*', r.text)
        for u in urls:
            streams.append({
                "name": "[1080p] Driveleech",
                "url": u,
                "quality": "1080p",
            })

    except Exception:
        pass
    return streams


async def extract_gofile(url: str, client: httpx.AsyncClient) -> list[dict]:
    """Gofile: API-based file listing."""
    streams = []
    try:
        # Extract file ID from URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')
        if not parts:
            return []

        file_id = parts[-1]

        # Create account
        r = await client.post("https://api.gofile.io/accounts", headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return []

        data = r.json()
        if data.get("status") != "ok":
            return []

        account_token = data["data"]["token"]
        headers = {**HEADERS, "Authorization": account_token}

        # Get file info
        r2 = await client.get(f"https://api.gofile.io/contents/{file_id}?wt=4fd6sg89d7s6", headers=headers, timeout=TIMEOUT)
        if r2.status_code != 200:
            return []

        file_data = r2.json()
        if file_data.get("status") != "ok":
            return []

        files = file_data.get("data", {}).get("children", {})
        for file_id_key, file_info in files.items():
            download_url = file_info.get("link")
            if download_url:
                quality = get_quality(file_info.get("name", ""))
                streams.append({
                    "name": f"[{quality}] Gofile",
                    "url": download_url,
                    "quality": quality,
                })

    except Exception:
        pass
    return streams


async def extract_stream(url: str, client: httpx.AsyncClient) -> list[dict]:
    """Route URL to appropriate file host extractor."""
    url_lower = url.lower()

    if 'fastdlserver' in url_lower:
        return await extract_fastdlserver(url, client)
    elif 'gdflix' in url_lower or 'gdlink' in url_lower:
        return await extract_gdflix(url, client)
    elif 'hubcloud' in url_lower or 'vcloud' in url_lower:
        return await extract_hubcloud(url, client)
    elif 'driveleech' in url_lower or 'driveseed' in url_lower:
        return await extract_driveleech(url, client)
    elif 'gofile' in url_lower:
        return await extract_gofile(url, client)
    else:
        # Try generic extraction - follow redirects and check for m3u8/mp4
        try:
            r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=False)
            location = r.headers.get('location', '')
            if location:
                return [{"name": "[1080p] Direct", "url": location, "quality": "1080p"}]
        except Exception:
            pass
        return []