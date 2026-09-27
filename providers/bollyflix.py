"""Bollyflix source site scraper for Nuvio/Stremio Movies & TV Addon.

Scrapes Bollyflix for movie/TV show pages and extracts file host links.
Uses dynamic URLs from urls.json (CSX pattern).
"""
import re
import json
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
URLS_JSON = "https://raw.githubusercontent.com/SaurabhKaperwan/Utils/refs/heads/main/urls.json"

# Fallback URLs if urls.json is unavailable
FALLBACK_URLS = {
    "bollyflix": "https://bollyflix.frl",
    "moviesdrive": "https://moviesdrive.forum",
    "moviesmod": "https://moviesleech.rest",
    "vegamovies": "https://vegamovies.mq",
}


async def get_base_url(client: httpx.AsyncClient, source: str) -> str:
    """Get the current base URL for a source site."""
    try:
        r = await client.get(URLS_JSON, headers=HEADERS, timeout=5.0)
        if r.status_code == 200:
            data = r.json()
            url = data.get(source, "")
            if url:
                return url.rstrip('/')
    except Exception:
        pass
    return FALLBACK_URLS.get(source, "")


async def search_bollyflix(client: httpx.AsyncClient, query: str) -> list[dict]:
    """Search Bollyflix for content."""
    base_url = await get_base_url(client, "bollyflix")
    if not base_url:
        return []

    results = []
    try:
        search_url = f"{base_url}/search/{query}/page/1/"
        r = await client.get(search_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.select('div.post-cards > article')

        for article in articles:
            link_elem = article.select_one('a')
            if not link_elem:
                continue
            href = link_elem.get('href', '')
            title = link_elem.get('title', '') or link_elem.get_text(strip=True)
            if href and title:
                results.append({
                    "title": title,
                    "url": href if href.startswith('http') else base_url + href,
                })
    except Exception as e:
        print(f"[Bollyflix] Search error: {e}")

    return results


async def extract_file_host_links(client: httpx.AsyncClient, page_url: str) -> list[dict]:
    """Extract file host links from a Bollyflix content page."""
    links = []
    try:
        r = await client.get(page_url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')

        # Find download buttons
        buttons = soup.select('a.maxbutton-download-links, a.dl, a.btnn, a.maxbutton-1, a.maxbutton-5')
        for btn in buttons:
            href = btn.get('href', '')
            text = btn.get_text(strip=True)
            if not href:
                continue

            # Decode base64 url= parameters
            if 'url=' in href:
                try:
                    b64_val = href.split('url=')[-1]
                    href = base64.b64decode(b64_val).decode('utf-8')
                except Exception:
                    pass

            # Identify file host
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
                })

        # Also check for episode links (TV shows)
        ep_buttons = soup.select('a.maxbutton-episode-links, .maxbutton-g-drive, .maxbutton-af-download')
        for btn in ep_buttons:
            href = btn.get('href', '')
            text = btn.get_text(strip=True)
            if not href:
                continue

            if 'url=' in href:
                try:
                    b64_val = href.split('url=')[-1]
                    href = base64.b64decode(b64_val).decode('utf-8')
                except Exception:
                    pass

            host = ""
            if 'gdflix' in href.lower() or 'gdlink' in href.lower():
                host = "gdflix"
            elif 'hubcloud' in href.lower() or 'vcloud' in href.lower():
                host = "hubcloud"
            elif 'driveleech' in href.lower() or 'driveseed' in href.lower():
                host = "driveleech"

            if host:
                links.append({
                    "host": host,
                    "url": href,
                    "text": text,
                    "episode": True,
                })

    except Exception as e:
        print(f"[Bollyflix] Extract error: {e}")

    return links


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | None = None
) -> list[dict]:
    """Resolve Bollyflix streams for a given TMDB ID."""
    if not title:
        return []

    streams = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
        # Search for content
        results = await search_bollyflix(client, title)
        if not results:
            return []

        # Take first result
        content_url = results[0]["url"]

        # Extract file host links
        links = await extract_file_host_links(client, content_url)
        if not links:
            return []

        # Extract actual streams from file host links
        from providers import filehosts
        for link in links:
            try:
                host_streams = await filehosts.extract_stream(link["url"], client)
                for s in host_streams:
                    s["name"] = f"[{s['quality']}] Bollyflix {link['host']}"
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
                print(f"[Bollyflix] Error extracting {link['host']}: {e}")

        # If no streams extracted, fall back to returning the links
        if not streams:
            for link in links:
                streams.append({
                    "name": f"[{link['host']}] Bollyflix",
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