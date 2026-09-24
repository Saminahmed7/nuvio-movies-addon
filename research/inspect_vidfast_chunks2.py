import httpx
import re

headers = {'User-Agent': 'Mozilla/5.0'}
for c in ['687-8e9f24493e814e00.js', 'aaea2bcf-18613745c71632cf.js', 'app/layout-ab6a5ef8de26af62.js']:
    url = f'https://vidfast.vc/_next/static/chunks/{c}'
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=12)
    print(f"{c}: {len(r.text)} bytes")
    # Search for api, stream, player, url
    apis = re.findall(r'["\'`](/(?:api|embed|stream|source|v\d)[^"\'`\s]+)["\'`]', r.text)
    if apis:
        print("  APIs:", set(apis))
    urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', r.text)
    clean = [u for u in set(urls) if any(k in u for k in ('api', 'embed', 'player', 'stream', 'source'))]
    if clean:
        print("  Streaming URLs:", clean[:10])
