from curl_cffi import requests
import re
import json

# Check CorsFlix movie page in detail
base = 'https://watch.corsflix.dpdns.org'
r = requests.get(f'{base}/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

print(f"Status: {r.status_code}")
print(f"Final URL: {r.url}")

text = r.text

# Check for NEXT_DATA
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
if next_data:
    data = json.loads(next_data[0])
    page_props = data.get("props", {}).get("pageProps", {})
    print(f"pageProps keys: {list(page_props.keys())}")
    
    details = page_props.get("details", {})
    if details:
        print(f"details keys: {list(details.keys()) if isinstance(details, dict) else type(details)}")
    else:
        # Try other keys
        for k, v in page_props.items():
            if isinstance(v, dict) and len(v) > 3:
                print(f"  {k}: {list(v.keys())[:10]}")
            elif isinstance(v, list) and len(v) > 0:
                print(f"  {k}: list of {len(v)} items")

# Search for iframes
iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', text)
print(f"\niframes: {iframes}")

# Search for any watch/embed links
watch_links = re.findall(r'href=["\']([^"\']*(?:watch|play|embed|server)[^"\']*)["\']', text)
print(f"watch/play/embed/server links: {watch_links[:10]}")

# Search for any m3u8 or stream URLs
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
print(f"m3u8: {m3u8}")

# Search for any API calls in the page
api_urls = re.findall(r'["\'](/api/[^"\']+)["\']', text)
print(f"API URLs: {set(api_urls)}")

# Save for analysis
with open('research/corsflix_movie.html', 'w', encoding='utf-8') as f:
    f.write(text)