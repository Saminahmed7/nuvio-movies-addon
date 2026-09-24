from curl_cffi import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
for c in ['1ayty9ezl44n3.js', '00fr704hnqv9t.js']:
    u = f'https://www.movy.sx/_next/static/chunks/{c}'
    r = requests.get(u, headers=headers, impersonate='chrome133a', timeout=10)
    print(f"=== {c} ({len(r.text)} bytes) ===")
    urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', r.text)
    clean = [x for x in set(urls) if not any(k in x for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'nextjs', 'github'))]
    if clean:
        print("  URLs:")
        for x in clean:
            print("   ", x)
    apis = re.findall(r'["\'`](/(?:api|embed|stream|source|play|v\d)[^"\'`\s]+)["\'`]', r.text)
    if apis:
        print("  APIs:", set(apis))
