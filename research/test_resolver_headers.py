import httpx

url = 'https://stellar.hls.lol/resolve'
params = {'tmdbId': '27205', 'type': 'movie'}

for ref in ['https://atlantic.st/', 'https://stellar.hls.lol/', 'https://cdn.hls.lol/']:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': ref,
        'Origin': 'https://atlantic.st'
    }
    r = httpx.get(url, params=params, headers=headers, timeout=10)
    data = r.json()
    print(f'Referer: {ref}')
    print(f'  Status: {r.status_code}')
    print(f'  Found: {data.get("found")}')
    print(f'  URL: {data.get("url", "N/A")[:80]}...')
    print()