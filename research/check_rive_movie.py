from curl_cffi import requests
import re
import json

# Check Rive movie page
r = requests.get('https://www.rivestream.app/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

print(f"Rive movie page Status: {r.status_code}")
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

# Search for iframes
iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', text)
print(f"\niframes: {iframes}")

# Search for any embed/watch links
watch_links = re.findall(r'href=["\']([^"\']*(?:watch|play|embed)[^"\']*)["\']', text)
print(f"watch/play/embed links: {watch_links[:10]}")

# Check for any server/source mentions in scripts
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text)
print(f"\nScripts ({len(scripts)}):")
for s in scripts[:10]:
    print(f'  {s}')

# Save for analysis
with open('research/rive_movie.html', 'w', encoding='utf-8') as f:
    f.write(text)