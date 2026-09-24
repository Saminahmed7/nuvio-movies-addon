from curl_cffi import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://vidfast.pro/movie/27205'
}

for chunk in ['585-06626bce041c7708.js', '365-71c2a8238d040bc9.js']:
    url = f'https://vidfast.pro/_next/static/chunks/{chunk}'
    r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
    print(f"{chunk}: {len(r.text)} bytes")
    # Search for api
    apis = re.findall(r'["\'`](/(?:api|embed|source|stream)[^"\'`\s]+)["\'`]', r.text)
    print(f"  APIs in {chunk}:", set(apis))
    # Search for URLs
    urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', r.text)
    clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react'))]
    print(f"  URLs in {chunk}:", clean[:10])
