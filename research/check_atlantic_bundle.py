import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://atlantic.st/",
    "Origin": "https://atlantic.st"
}

# Check the main Atlantic bundle
r = httpx.get('https://atlantic.st/assets/index-BA2TuH7B.js', headers=HEADERS, timeout=10)
print(f"Bundle Status: {r.status_code}")
print(f"Length: {len(r.text)}")

import re
# Search for stellar.hls.lol
stellar = re.findall(r'[^a-zA-Z0-9](stellar\.hls\.lol[^"\'\s]*)[^a-zA-Z0-9]', r.text)
print(f"\nstellar.hls.lol mentions:")
for s in set(stellar):
    print(f'  {s}')

# Search for resolver
resolver = re.findall(r'["\']([^"\']*resolve[^"\']*)["\']', r.text)
print(f"\nResolver mentions:")
for r_url in set(resolver):
    print(f'  {r_url}')

# Search for any API calls with tmdb
tmdb = re.findall(r'["\']([^"\']*tmdb[^"\']*)["\']', r.text)
print(f"\ntmdb mentions:")
for t in set(tmdb):
    print(f'  {t}')

# Search for vdrk.site subtitles
vdrk = re.findall(r'["\']([^"\']*vdrk[^"\']*)["\']', r.text)
print(f"\nvdrk mentions:")
for v in set(vdrk):
    print(f'  {v}')

# Search for CDN
cdn = re.findall(r'["\']([^"\']*cdn\.hls\.lol[^"\']*)["\']', r.text)
print(f"\ncdn.hls.lol mentions:")
for c in set(cdn):
    print(f'  {c}')

# Save for analysis
with open('research/atlantic_bundle.js', 'w') as f:
    f.write(r.text)