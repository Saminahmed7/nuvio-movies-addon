from curl_cffi import requests

base = 'https://api2.acermovies.fun'
r = requests.get(f'{base}/', impersonate='chrome133a', timeout=10)
print(f'Root: {r.status_code}')
print(f'Response: {r.text[:200]}')

endpoints = [
    '/source/27205',
    '/movie/27205',
    '/stream/27205',
    '/v1/movie/27205',
    '/v1/source/27205',
    '/api/source/27205',
    '/api/movie/27205',
]

headers = {'Referer': 'https://acermovies.fun/'}

for ep in endpoints:
    r = requests.get(f'{base}{ep}', headers=headers, impersonate='chrome133a', timeout=10)
    ct = r.headers.get('content-type', '')
    print(f'{ep}: {r.status_code} - {ct}')
    if r.status_code == 200:
        print(f'  {r.text[:300]}')