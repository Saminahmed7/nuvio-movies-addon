import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://atlantic.st/",
    "Origin": "https://atlantic.st"
}
RESOLVER_URL = "https://stellar.hls.lol/resolve"

# Test Inception
params = {"tmdbId": "27205", "type": "movie"}
r = httpx.get(RESOLVER_URL, params=params, headers=HEADERS, timeout=10)
print(f"Resolve Status: {r.status_code}")
print(f"Resolve Response: {r.text}")

import json
data = r.json()
if data.get("url"):
    proxy_url = data["url"]
    print(f"\nProxy URL: {proxy_url}")
    
    # Step 2: Fetch master playlist
    r2 = httpx.get(proxy_url, headers=HEADERS, timeout=10, follow_redirects=True)
    print(f"Master Playlist Status: {r2.status_code}")
    print(f"Final URL: {r2.url}")
    print(f"Master Playlist (first 2000 chars): {r2.text[:2000]}")