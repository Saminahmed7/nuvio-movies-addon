from curl_cffi import requests
import re
import json

# Check the watch page
r = requests.get('https://www.movy.sx/watch/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

print(f"Watch page Status: {r.status_code}")
print(f"Final URL: {r.url}")

text = r.text

# Check for NEXT_DATA
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
if next_data:
    data = json.loads(next_data[0])
    page_props = data.get("props", {}).get("pageProps", {})
    print(f"pageProps keys: {list(page_props.keys())}")
    details = page_props.get("details", {})
    print(f"details keys: {list(details.keys()) if isinstance(details, dict) else type(details)}")
    if isinstance(details, dict):
        for k, v in details.items():
            if k in ['sources', 'servers', 'streams', 'videos', 'watch', 'providers', 'sourcesData']:
                print(f"\n  {k}: {type(v)}")
                if isinstance(v, list):
                    for item in v[:3]:
                        print(f"    {item}")
                elif isinstance(v, dict):
                    print(f"    {v}")

# Search for any embed/iframe sources
iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', text)
print(f"\niframes: {iframes}")

# Search for m3u8
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
print(f"m3u8: {m3u8}")

# Search for any API calls in scripts
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text)
for script in scripts[:5]:
    print(f"\nChecking script: {script}")
    if script.startswith('/'):
        script_url = f'https://www.movy.sx{script}'
    else:
        script_url = script
    try:
        sr = requests.get(script_url, impersonate='chrome133a', timeout=5)
        # Search for source/stream/server in script
        for keyword in ['source', 'stream', 'server', 'm3u8', 'embed']:
            matches = re.findall(rf'["\'][^"\']*{keyword}[^"\']*["\']', sr.text, re.IGNORECASE)
            if matches:
                print(f"  {keyword} in {script}: {set(matches)[:3]}")
    except:
        pass