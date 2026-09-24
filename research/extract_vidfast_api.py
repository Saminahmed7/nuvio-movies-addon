from curl_cffi import requests
import re

url = 'https://vidfast.pro/_next/static/chunks/app/movie/%5Bid%5D/page-2b404c4e3d6ea450.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://vidfast.pro/movie/27205'
}

r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
text = r.text
print('Length of page.js:', len(text))

# Find API calls
endpoints = re.findall(r'["\'`](/(?:api|embed|source|stream)[^"\'`\s]+)["\'`]', text)
print('Endpoints in vidfast movie page:')
for ep in set(endpoints):
    print(' ', ep)

# Find fetch URLs
fetches = re.findall(r'fetch\([\"\'`]([^\"\'`]+)[\"\'`]', text)
print('Direct fetch URLs:')
for f in set(fetches):
    print(' ', f)

with open('research/vidfast_page.js', 'w', encoding='utf-8') as f:
    f.write(text)
