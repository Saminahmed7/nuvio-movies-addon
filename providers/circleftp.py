"""CircleFTP provider for Nuvio/Stremio Movies & TV Addon.

Features:
- BDIX (Bangladesh IX) provider - works on supported ISPs
- Direct HTTP streams from CircleFTP servers
- Supports Movies, TV Series, Anime, Cartoons, Asian Dramas, Documentaries
- Categories for different content types (English, Hindi, South Indian, Anime, etc.)
- Download support
- Chromecast support
"""
import re
import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}
TIMEOUT = 15.0

# CircleFTP configuration
MAIN_URL = "http://new.circleftp.net"
MAIN_API_URL = "http://new.circleftp.net:5000"
FALLBACK_API_URL = "http://15.1.1.50:5000"

# Categories from the provider
CATEGORIES = {
    "80": "Featured",
    "6": "English Movies",
    "9": "English & Foreign TV Series",
    "22": "Dubbed TV Series",
    "2": "Hindi Movies",
    "5": "Hindi TV Series",
    "238": "Indian TV Show",
    "7": "English & Foreign Hindi Dubbed Movies",
    "8": "Foreign Language Movies",
    "3": "South Indian Dubbed Movies",
    "4": "South Indian Movies",
    "1": "Animation Movies",
    "21": "Anime Series",
    "85": "Documentary",
    "15": "WWE"
}

# Content types mapping
CONTENT_TYPES = {
    "singleVideo": "movie",
    "series": "series"
}

QUALITY_KEYWORDS = {
    "4k": "4K", "2160p": "4K", "uhd": "4K",
    "1440p": "1440p", "2k": "1440p",
    "1080p": "1080p", "fhd": "1080p", "1080": "1080p",
    "720p": "720p", "hd": "720p",
    "480p": "480p", "sd": "480p",
    "360p": "360p",
    "240p": "240p"
}


def format_size(bytes_val: int | float | None) -> str | None:
    if not bytes_val or bytes_val <= 0:
        return None
    gb = bytes_val / (1024 ** 3)
    if gb >= 1.0:
        return f"{gb:.2f} GB"
    mb = bytes_val / (1024 ** 2)
    return f"{int(mb)} MB"


def extract_quality(title: str, quality_field: str = "") -> str:
    """Extract quality from title or quality field."""
    text = f"{title} {quality_field}".lower()
    
    for keyword, quality in QUALITY_KEYWORDS.items():
        if keyword in text:
            return quality
    
    # Try to extract from patterns like "1080p", "720p", etc.
    match = re.search(r'(\d{3,4})p', text)
    if match:
        return f"{match.group(1)}p"
    
    return "1080p"  # Default


def extract_year(text: str) -> str | None:
    """Extract year from text."""
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return match.group(0) if match else None


def get_dub_status(title: str) -> dict:
    """Check for dub/sub status from title."""
    title_lower = title.lower()
    return {
        "dub": any(k in title_lower for k in ("dubbed", "dual audio", "multi audio")),
        "sub": False
    }


async def fetch_api_json(client: httpx.AsyncClient, endpoint: str, cache_time: int = 60) -> dict | None:
    """Fetch JSON from CircleFTP API with fallback."""
    clean_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    
    for base_url in [MAIN_API_URL, FALLBACK_API_URL]:
        try:
            r = await client.get(
                f"{base_url}{clean_endpoint}",
                headers=HEADERS,
                timeout=TIMEOUT,
                follow_redirects=True
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None


def parse_post_to_stream(post: dict, base_url: str, api_url: str) -> dict | None:
    """Convert a CircleFTP post to a stream item."""
    content_type = post.get("type", "")
    stream_type = CONTENT_TYPES.get(content_type)
    
    if not stream_type:
        return None
    
    post_id = post.get("id")
    title = post.get("title", "")
    image_sm = post.get("imageSm", "")
    
    year = extract_year(title)
    quality = extract_quality(title)
    dub_status = get_dub_status(title)
    
    stream_url = f"{base_url}/content/{post_id}"
    poster = f"{api_url}/uploads/{image_sm}" if image_sm else ""
    
    stream_item = {
        "name": f"[{quality}] CircleFTP",
        "title": f"{title} ({year})" if year else title,
        "url": stream_url,
        "quality": quality,
        "behaviorHints": {
            "notWebReady": False,
            "proxyHeaders": {
                "request": {
                    "User-Agent": UA,
                    "Referer": MAIN_URL + "/"
                }
            }
        }
    }
    if poster:
        stream_item["poster"] = poster
    
    return stream_item


async def resolve(
    tmdb_id: int | str,
    ctype: str = "movie",
    season: int = 1,
    episode: int = 1,
    title: str = "",
    year: int | None = None
) -> list[dict]:
    """Resolve CircleFTP streams for a given TMDB ID."""
    if not tmdb_id:
        return []
    
    streams = []
    
    async with httpx.AsyncClient(headers=HEADERS, timeout=TIMEOUT) as client:
        # Try to search for the content
        search_query = title if title else ""
        if not search_query:
            # If no title provided, we can't search effectively
            # The provider doesn't support direct TMDB ID lookup
            return []
        
        try:
            # Search API
            json_data = await fetch_api_json(client, f"/api/posts?searchTerm={search_query}&order=desc", cache_time=0)
            if not json_data:
                return []
            
            posts = json_data.get("posts", [])
            if not posts:
                return []
            
            # Find matching post
            target_post = None
            for post in posts:
                if post.get("type") in ("singleVideo", "series"):
                    post_title = post.get("title", "").lower()
                    # Simple title matching
                    if search_query.lower() in post_title or post_title in search_query.lower():
                        target_post = post
                        break
            
            if not target_post and posts:
                target_post = posts[0]  # Fallback to first result
            
            if not target_post:
                return []
            
            # Get detailed content
            content_id = target_post.get("id")
            if not content_id:
                return []
            
            detail_json = await fetch_api_json(client, f"/api/posts/{content_id}")
            if not detail_json:
                return []
            
            load_data = detail_json
            content_title = load_data.get("title", "")
            content_type = load_data.get("type", "")
            content_year = load_data.get("year", "")
            image = load_data.get("image", "")
            meta_data = load_data.get("metaData", "")
            
            stream_type = CONTENT_TYPES.get(content_type)
            if not stream_type or stream_type != ctype:
                return []
            
            year_str = str(year) if year else (content_year if content_year else "")
            quality = extract_quality(content_title)
            dub_status = get_dub_status(content_title)
            
            stream_url = f"{MAIN_URL}/content/{content_id}"
            poster = f"{FALLBACK_API_URL}/uploads/{image}" if image else ""
            
            stream_item = {
                "name": f"[{quality}] CircleFTP",
                "title": f"{content_title} ({year_str})" if year_str else content_title,
                "url": stream_url,
                "quality": quality,
                "behaviorHints": {
                    "notWebReady": False,
                    "proxyHeaders": {
                        "request": {
                            "User-Agent": UA,
                            "Referer": MAIN_URL + "/"
                        }
                    }
                }
            }
            if poster:
                stream_item["poster"] = poster
            
            streams.append(stream_item)
            
        except Exception as e:
            print(f"[CircleFTP] Resolution error: {e}")
            return []
    
    return streams