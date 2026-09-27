from curl_cffi import requests
import re
import json

# Check Acer Movies
r = requests.get('https://acermovies.fun/movie/27205', impersonate='chrome133a', timeout=10)
print(f'Status: {r.status_code}')
print(f'Final URL: {r.url}')

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

# Search for watch/embed links
watch_links = re.findall(r'href=["\']([^"\']*(?:watch|play|embed)[^"\']*)["\']', text)
print(f'watch/play/embed links: {watch_links[:10]}')

# Search for any API calls
api_urls = re.findall(r'["\'](/api/[^"\']+)["\']', text)
print(f'API URLs: {set(api_urls)}')

# Search for any stream URLs
stream_urls = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4|mkv)[^\s"\'<>]*', text)
print(f'Stream URLs: {stream_urls}')