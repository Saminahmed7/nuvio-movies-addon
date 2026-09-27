"""GDFlix/GDLink file host extractor for Nuvio/Stremio Movies & TV Addon.

Ports the CSX CloudStream GDFlix extractor to Python.
Extracts direct download links from GDFlix/GDLink pages.
"""
import re
import base64
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
    """Extract scheme://host from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return url


def get_index_quality(text: str) -> int:
    """Extract quality index from text (e.g., '1080p' -> 1080)."""
    if not text:
        return 0
    match = re.search(r'(\d{3,4})[pP]', text)
    if match:
        return int(match.group(1))
    lower = text.lower()
    if '4k' in lower:
        return 2160
    if '2k' in lower:
        return 1440
    return 0


async def extract_gdflix(url: str, client: httpx.AsyncClient) -> list[dict]:
    """Extract direct download links from a GDFlix/GDLink page."""
    streams = []
    try:
        r = await client.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        base_url = get_base_url(str(r.url))

        # Extract file info
        file_name = ""
        file_size = ""
        name_elem = soup.select_one('ul > li.list-group-item:contains("Name")')
        if name_elem:
            file_name = name_elem.get_text().replace("Name : ", "").strip()
        size_elem = soup.select_one('ul > li.list-group-item:contains("Size")')
        if size_elem:
            file_size = size_elem.get_text().replace("Size : ", "").strip()

        quality = get_index_quality(file_name)

        # Find download buttons
        buttons = soup.select('div.text-center a')
        for btn in buttons:
            text = btn.get_text(strip=True)
            link = btn.get('href', '')
            if not link:
                continue

            # Handle different button types
            if any(k in text for k in ['FSL V2', 'DIRECT DL', 'DIRECT SERVER']):
                streams.append({
                    "name": f"GDFlix {text}",
                    "url": link,
                    "quality": quality,
                    "file_name": file_name,
                    "file_size": file_size,
                })
            elif 'CLOUD DOWNLOAD' in text:
                streams.append({
                    "name": f"GDFlix {text}",
                    "url": link,
                    "quality": quality,
                    "file_name": file_name,
                    "file_size": file_size,
                })
            elif 'FAST CLOUD' in text:
                try:
                    r2 = await client.get(base_url + link, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
                    if r2.status_code == 200:
                        soup2 = BeautifulSoup(r2.text, 'html.parser')
                        dlink = soup2.select_one('div.card-body a')
                        if dlink and dlink.get('href'):
                            streams.append({
                                "name": f"GDFlix FastCloud",
                                "url": dlink['href'],
                                "quality": quality,
                                "file_name": file_name,
                                "file_size": file_size,
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
                                "name": f"GDFlix Instant",
                                "url": instant_link,
                                "quality": quality,
                                "file_name": file_name,
                                "file_size": file_size,
                            })
                except Exception:
                    pass
            elif 'pixeldra' in link.lower():
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(link)
                    base = f"{parsed.scheme}://{parsed.netloc}"
                    if 'download' in link.lower():
                        final_url = link
                    else:
                        file_id = link.rstrip('/').split('/')[-1]
                        final_url = f"{base}/api/file/{file_id}?download"
                    streams.append({
                        "name": f"GDFlix Pixeldrain",
                        "url": final_url,
                        "quality": quality,
                        "file_name": file_name,
                        "file_size": file_size,
                    })
                except Exception:
                    pass

    except Exception as e:
        print(f"[GDFlix] Error: {e}")

    return streams


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | None = None
) -> list[dict]:
    """Resolve GDFlix streams for a given TMDB ID."""
    # This is a file host extractor - it needs a GDFlix URL to work
    # The actual scraping of source sites to find GDFlix links is done elsewhere
    return []