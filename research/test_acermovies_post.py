from curl_cffi import requests
import json

base = 'https://api2.acermovies.fun'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://acermovies.fun/',
    'Origin': 'https://acermovies.fun',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Try the sourceUrl endpoint with POST
data = {'url': 'https://acermovies.fun/movie/27205', 'seriesType': 'movie'}
r = requests.post(f'{base}/api/sourceUrl', json=data, headers=headers, impersonate='chrome133a', timeout=15)
print(f'POST /api/sourceUrl: {r.status_code} - {r.headers.get("content-type")}')
print(f'Response: {r.text[:500]}')

# Also try sourceQuality
data2 = {'url': 'https://acermovies.fun/movie/27205'}
r2 = requests.post(f'{base}/api/sourceQuality', json=data2, headers=headers, impersonate='chrome133a', timeout=15)
print(f'\nPOST /api/sourceQuality: {r2.status_code} - {r2.headers.get("content-type")}')
print(f'Response: {r2.text[:500]}')