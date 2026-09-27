from curl_cffi import requests
import re

# Check the actual movie page
r = requests.get('https://www.movy.sx/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

print(f"Status: {r.status_code}")

# Look for any API calls or stream URLs in the page
text = r.text

# Search for sources, streams, servers
for keyword in ['source', 'stream', 'server', 'm3u8', 'embed', 'api', 'watch']:
    matches = re.findall(rf'["\'][^"\']*{keyword}[^"\']*["\']', text, re.IGNORECASE)
    if matches:
        unique_matches = set(matches)
        print(f"\n{keyword} mentions:")
        for m in list(unique_matches)[:10]:
            print(f'  {m}')

# Look for any URLs that might be stream related
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
stream_urls = [u for u in set(urls) if any(k in u for k in ('stream', 'source', 'server', 'embed', 'player', 'cdn', 'm3u8'))]
print(f"\nStream-related URLs:")
for u in stream_urls[:15]:
    print(f'  {u}')

# Check for NEXT_DATA
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
if next_data:
    import json
    data = json.loads(next_data[0])
    print(f"\nNEXT_DATA keys: {list(data.keys())}")
    props = data.get("props", {})
    page_props = props.get("pageProps", {})
    print(f"pageProps keys: {list(page_props.keys())}")
    # Look for movie data
    for key in ['movie', 'sources', 'servers', 'streams', 'video']:
        if key in page_props:
            print(f"  Found {key}: {type(page_props[key])}")