from curl_cffi import requests
import json
import time

base = 'https://api2.acermovies.fun'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://acermovies.fun/',
    'Origin': 'https://acermovies.fun',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Try polling the sourceUrl endpoint
data = {'url': 'https://acermovies.fun/movie/27205', 'seriesType': 'movie'}

print("Initial request...")
r = requests.post(f'{base}/api/sourceUrl', json=data, headers=headers, impersonate='chrome133a', timeout=15)
print(f'Initial: {r.text}')

# Poll for a few seconds
for i in range(10):
    time.sleep(1)
    r = requests.post(f'{base}/api/sourceUrl', json=data, headers=headers, impersonate='chrome133a', timeout=15)
    print(f'Poll {i+1}: {r.text}')
    if 'sourceUrl' in r.text:
        print('Got sourceUrl!')
        break