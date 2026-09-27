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

# Try with different URL formats
urls_to_try = [
    'https://acermovies.fun/movie/27205',
    'https://acermovies.fun/watch/27205',
    'https://acermovies.fun/embed/27205',
    'https://acermovies.fun/stream/27205',
]

for url in urls_to_try:
    print(f'\nTesting URL: {url}')
    data = {'url': url, 'seriesType': 'movie'}
    r = requests.post(f'{base}/api/sourceUrl', json=data, headers=headers, impersonate='chrome133a', timeout=15)
    print(f'  Status: {r.status_code}')
    print(f'  Response: {r.text}')

# Also check if there's a way to get the source from the search API
print('\n--- Testing search ---')
search_data = {'searchQuery': 'Inception'}
r3 = requests.post(f'{base}/api/search', json=search_data, headers=headers, impersonate='chrome133a', timeout=15)
print(f'Search: {r3.status_code}')
print(f'Response: {r3.text[:1000]}')