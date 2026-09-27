from curl_cffi import requests
import re
import json

# Check the embed page
base = 'https://watch.corsflix.dpdns.org'
r = requests.get(f'{base}/embed/27205', impersonate='chrome133a', timeout=10)
print(f'Status: {r.status_code}')

text = r.text

# Check for NEXT_DATA
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
if next_data:
    data = json.loads(next_data[0])
    page_props = data.get('props', {}).get('pageProps', {})
    print(f'pageProps keys: {list(page_props.keys())}')
    for k, v in page_props.items():
        if isinstance(v, dict) and len(v) > 2:
            print(f'  {k}: {list(v.keys())}')
        elif isinstance(v, list) and len(v) > 0:
            print(f'  {k}: list of {len(v)} items')

# Search for iframes
iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', text)
print(f'iframes: {iframes}')

# Search for m3u8
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
print(f'm3u8: {m3u8}')

# Search for any video URLs
video_urls = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4|mkv|webm)[^\s"\'<>]*', text)
print(f'video URLs: {video_urls}')

# Search for source/stream in scripts
scripts = re.findall(r'<script[^>]*>([^<]+)</script>', text)
for i, script in enumerate(scripts):
    if any(k in script.lower() for k in ['source', 'server', 'stream', 'm3u8', 'video']):
        print(f'Script {i}: {script[:500]}')