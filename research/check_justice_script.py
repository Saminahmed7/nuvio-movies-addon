import httpx

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {
    "User-Agent": UA,
    "Referer": "https://atlantic.st/",
    "Origin": "https://atlantic.st"
}

# Check the justice.hls.lol script
r = httpx.get('https://justice.hls.lol/api/script.js', headers=HEADERS, timeout=10)
print(f"Script Status: {r.status_code}")
print(f"Length: {len(r.text)}")

import re
# Search for API endpoints
apis = re.findall(r'["\'](/api/[^"\'\s]+)["\']', r.text)
print(f"\nAPI endpoints:")
for a in set(apis):
    print(f'  {a}')

# Search for resolver
resolver = re.findall(r'["\']([^"\']*resolve[^"\']*)["\']', r.text)
print(f"\nResolver mentions:")
for r_url in set(resolver):
    print(f'  {r_url}')

# Search for CDN
cdn = re.findall(r'["\']([^"\']*hls\.lol[^"\']*)["\']', r.text)
print(f"\nCDN mentions:")
for c in set(cdn):
    print(f'  {c}')

# Search for m3u8 or stream
stream = re.findall(r'["\']([^"\']*m3u8[^"\']*)["\']', r.text)
print(f"\nm3u8 mentions:")
for s in set(stream):
    print(f'  {s}')

# Save script for analysis
with open('research/justice_script.js', 'w') as f:
    f.write(r.text)