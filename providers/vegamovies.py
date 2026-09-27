"""VegaMovies source site scraper for Nuvio/Stremio Movies & TV Addon.

Scrapes VegaMovies for movie/TV show pages and extracts file host links.
Uses dynamic URLs from urls.json (CSX pattern).
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
URLS_JSON = "https://raw.githubusercontent.com/SaurabhKaperwan/Utils/refs/heads/main/urls.json"
FALLBACK_URL = "https://vegamovies.mq"


async def get_base_url(client: httpx.AsyncClient) -> str:
    try:
        r = await client.get(URLS_JSON, headers=HEADERS, timeout=5.0)
        if r.status_code == 200:
            data = r.json()
            url = data.get("vegamovies", "")
            if url:
                return url.rstrip('/')
    except Exception:
        pass
    return FALLBACK_URL


async def search_vegamovies(client: httpx.AsyncClient, query: str) -> list[dict]:
    base_url = await get_base_url(client)
    if not base_url:
        return []

    results = []
    try:
        search_url = f"{base_url}/search.php?q={query}&page=1"
        r = await client.get(search_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.select('div.movies-grid > a')

        for item in items:
            href = item.get('href', '')
            title = item.get_text(strip=True) or item.get('title', '')
            if href and title:
                results.append({
                    "title": title,
                    "url": href if href.startswith('http') else base_url + href,
                })
    except Exception as e:
        print(f"[VegaMovies] Search error: {e}")

    return results


async def extract_file_host_links(client: httpx.AsyncClient, page_url: str) -> list[dict]:
    links = []
    try:
        r = await client.get(page_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')

        # Find quality sections (4K, 1080p, 720p)
        quality_tags = soup.select('main > h3')
        for h3 in quality_tags:
            quality_text = h3.get_text(strip=True)
            if not any(k in quality_text.lower() for k in ['4k', '1080p', '720p']):
                continue

            # Find download buttons near this quality header
            parent = h3.parent
            if not parent:
                continue

            buttons = parent.select('a:has(button.dwd-button), a.dwd-button, a[href*="gdflix"], a[href*="hubcloud"], a[href*="driveleech"]')
            for btn in buttons:
                href = btn.get('href', '')
                text = btn.get_text(strip=True)
                if not href:
                    continue

                host = ""
                if 'gdflix' in href.lower() or 'gdlink' in href.lower():
                    host = "gdflix"
                elif 'hubcloud' in href.lower() or 'vcloud' in href.lower():
                    host = "hubcloud"
                elif 'driveleech' in href.lower() or 'driveseed' in href.lower():
                    host = "driveleech"
                elif 'gofile' in href.lower():
                    host = "gofile"
                elif 'fastdlserver' in href.lower():
                    host = "fastdlserver"

                if host:
                    links.append({
                        "host": host,
                        "url": href,
                        "text": text,
                        "quality": quality_text,
                    })

        # Also check for any direct file host links in the page
        all_links = soup.select('a[href]')
        for a in all_links:
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if not href:
                continue

            host = ""
            if 'gdflix' in href.lower() or 'gdlink' in href.lower():
                host = "gdflix"
            elif 'hubcloud' in href.lower() or 'vcloud' in href.lower():
                host = "hubcloud"
            elif 'driveleech' in href.lower() or 'driveseed' in href.lower():
                host = "driveleech"

            if host and not any(l["url"] == href for l in links):
                links.append({
                    "host": host,
                    "url": href,
                    "text": text,
                    "quality": "1080p",
                })

    except Exception as e:
        print(f"[VegaMovies] Extract error: {e}")

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
        results = await search_vegamovies(client, title)
        if not results:
            return []

        content_url = results[0]["url"]
        links = await extract_file_host_links(client, content_url)
        if not links:
            return []

        from providers import filehosts
        for link in links:
            try:
                host_streams = await filehosts.extract_stream(link["url"], client)
                for s in host_streams:
                    s["name"] = f"[{s['quality']}] VegaMovies {link['host']}"
                    s["title"] = f"{title} ({year})" if year else title
                    s["behaviorHints"] = {
                        "notWebReady": False,
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": UA,
                                "Referer": content_url,
                            }
                        }
                    }
                    streams.append(s)
            except Exception as e:
                print(f"[VegaMovies] Error extracting {link['host']}: {e}")

        if not streams:
            for link in links:
                streams.append({
                    "name": f"[{link['host']}] VegaMovies",
                    "title": f"{title} ({year})" if year else title,
                    "url": link["url"],
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