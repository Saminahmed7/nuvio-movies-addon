from curl_cffi import requests
import json

base = 'https://acermovies.fun'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://acermovies.fun/',
    'Origin': 'https://acermovies.fun',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest'
}

# Try different API endpoints
endpoints = [
    f'{base}/api/sourceUrl?mediaId=27205&mediaType=movie',
    f'{base}/api/sourceQuality?mediaId=27205&mediaType=movie',
    f'{base}/api/sourceEpisodes?mediaId=27205&mediaType=tv',
    f'{base}/api/list?mediaId=27205&mediaType=movie',
]

for ep in endpoints:
    print(f'\nTesting: {ep}')
    r = requests.get(ep, headers=headers, impersonate='chrome133a', timeout=10)
    print(f'  Status: {r.status_code}')
    print(f'  Content-Type: {r.headers.get("content-type")}')
    print(f'  Response: {r.text[:500]}')
    if r.status_code == 200 and 'application/json' in r.headers.get('content-type', ''):
        try:
            print(f'  JSON: {json.dumps(r.json(), indent=2)[:500]}')
        except:
            pass