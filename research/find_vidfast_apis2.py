from curl_cffi import requests
import re

url = 'https://vidfast.pro/_next/static/chunks/app/movie/%5Bid%5D/page-2b404c4e3d6ea450.js'
r = requests.get(url, impersonate='chrome133a', timeout=15)
text = r.text
print(f'Length: {len(text)}')

apis = re.findall(r'["\'`](/api/[^"\'`\s]+)["\'`]', text)
print('API endpoints:')
for a in set(apis):
    print(' ', a)

fetches = re.findall(r'fetch\(["\`]([^"\'`]+)["\`]', text)
print('\nFetch URLs:')
for f in set(fetches):
    if 'api' in f or 'source' in f or 'embed' in f or 'stream' in f:
        print(' ', f)