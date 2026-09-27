import httpx

url = 'https://stellar.hls.lol/resolve'
params = {'tmdbId': '27205', 'type': 'movie'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://atlantic.st/',
    'Origin': 'https://atlantic.st'
}

r = httpx.get(url, params=params, headers=headers, timeout=10)
data = r.json()
proxy_url = data.get("url")
print(f"Proxy URL: {proxy_url}")

# Try fetching with different headers
for ref in ['https://atlantic.st/', 'https://stellar.hls.lol/', '']:
    h = dict(headers)
    if ref:
        h['Referer'] = ref
    else:
        h.pop('Referer', None)
    
    r2 = httpx.get(proxy_url, headers=h, timeout=10, follow_redirects=True)
    print(f"\nReferer: {ref or '(none)'}")
    print(f"  Status: {r2.status_code}")
    print(f"  Final URL: {r2.url}")
    print(f"  Content-Type: {r2.headers.get('content-type')}")
    if 'html' in r2.headers.get('content-type', ''):
        print(f"  Got HTML (first 200 chars): {r2.text[:200]}")
    else:
        print(f"  Got manifest (first 500 chars): {r2.text[:500]}")

# Also try without follow_redirects
print("\n--- Without follow_redirects ---")
r3 = httpx.get(proxy_url, headers=headers, timeout=10, follow_redirects=False)
print(f"Status: {r3.status_code}")
print(f"Headers: {dict(r3.headers)}")
print(f"Text: {r3.text[:200]}")