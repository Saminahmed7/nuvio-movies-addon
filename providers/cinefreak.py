"""Cinefreak source site scraper for Nuvio/Stremio Movies & TV Addon.

Scrapes Cinefreak for movie/TV show pages and extracts direct download links.
All free - no paid services.
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
BASE_URL = "https://cinefreak.net"


async def search_cinefreak(client: httpx.AsyncClient, query: str) -> list[dict]:
    results = []
    try:
        search_url = f"{BASE_URL}/?s={query}"
        r = await client.get(search_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.select('article, .post-cards > div, .movie-item')

        for article in articles:
            link_elem = article.select_one('a[href]')
            if not link_elem:
                continue
            href = link_elem.get('href', '')
            title = link_elem.get_text(strip=True) or link_elem.get('title', '')
            if href and title and '/movie/' in href or '/series/' in href or 'full-movie' in href or 'full-series' in href:
                results.append({
                    "title": title,
                    "url": href if href.startswith('http') else BASE_URL + href,
                })
    except Exception as e:
        print(f"[Cinefreak] Search error: {e}")

    return results


async def extract_direct_links(client: httpx.AsyncClient, page_url: str) -> list[dict]:
    """Extract direct download links from a Cinefreak content page."""
    links = []
    try:
        r = await client.get(page_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')

        # Look for cinecloud file pages
        for a in soup.select('a[href*="cinecloud"]'):
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if href:
                links.append({"url": href, "text": text, "type": "cinecloud"})

        # Look for direct FSL/fast cloud links (direct file URLs)
        for a in soup.select('a[href]'):
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if not href:
                continue
            # Direct file links (r2.dev, etc.)
            if any(k in href for k in ['.mkv', '.mp4', '.avi', '.m3u8']):
                links.append({"url": href, "text": text, "type": "direct"})
            # FSL / Fast Cloud links
            elif any(k in text.upper() for k in ['FSL', 'FAST CLOUD', 'DIRECT DL', 'DIRECT SERVER']):
                links.append({"url": href, "text": text, "type": "fsl"})

        # If we have cinecloud links, follow them to get direct file URLs
        direct_links = []
        for link in links:
            if link["type"] == "cinecloud":
                try:
                    r2 = await client.get(link["url"], headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
                    if r2.status_code == 200:
                        soup2 = BeautifulSoup(r2.text, 'html.parser')
                        # Look for direct file URLs
                        for a in soup2.select('a[href]'):
                            href = a.get('href', '')
                            text = a.get_text(strip=True)
                            if any(k in href for k in ['.mkv', '.mp4', '.m3u8']):
                                direct_links.append({"url": href, "text": text})
                except Exception:
                    pass
            elif link["type"] in ("direct", "fsl"):
                direct_links.append(link)

        return direct_links

    except Exception as e:
        print(f"[Cinefreak] Extract error: {e}")

    return links


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | None = None
) -> list[dict]:
    if not title:
        return []

    streams = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
        results = await search_cinefreak(client, title)
        if not results:
            return []

        content_url = results[0]["url"]
        direct_links = await extract_direct_links(client, content_url)

        for link in direct_links:
            url = link["url"]
            if not url.startswith('http'):
                url = BASE_URL + url

            streams.append({
                "name": "[1080p] Cinefreak",
                "title": f"{title} ({year})" if year else title,
                "url": url,
                "quality": "1080p",
                "size": 0,
                "behaviorHints": {
                    "notWebReady": False,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": UA,
                            "Referer": content_url,
                        }
                    }
                }
            })

    return streams