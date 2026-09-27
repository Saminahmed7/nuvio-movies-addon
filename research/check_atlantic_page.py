import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://atlantic.st/",
    "Origin": "https://atlantic.st"
}

# Check the Atlantic embed page for a movie
r = httpx.get('https://atlantic.st/movie/27205', headers=HEADERS, timeout=10, follow_redirects=True)
print(f"Movie page Status: {r.status_code}")
print(f"Final URL: {r.url}")

# Look for player/embed links
import re
iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', r.text)
print(f"\niframes: {iframes}")

# Look for any m3u8 or stream URLs
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f"\nm3u8: {m3u8[:5]}")

# Look for API calls
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text)
print(f"\nscripts: {scripts[:10]}")

# Check for next.js data
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', r.text)
if next_data:
    import json
    data = json.loads(next_data[0])
    print(f"\nNEXT_DATA keys: {list(data.keys())}")
    # Look for stream info
    props = data.get("props", {})
    page_props = props.get("pageProps", {})
    print(f"pageProps keys: {list(page_props.keys())}")