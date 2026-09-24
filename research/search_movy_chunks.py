from curl_cffi import requests
import re

# Fetch the Movy page bundle
chunks = ['1qoza-7hj8o97.js', '1zyk0gv4kwtq5.js', '0nu0eje3907fe.js', '3rhsii4i811du.js', '3ntjt_vgr2yt8.js']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for c in chunks:
    u = f'https://www.movy.sx/_next/static/chunks/{c}'
    r = requests.get(u, headers=headers, impersonate='chrome133a', timeout=10)
    if 'wecollege' in r.text or 'stream' in r.text.lower():
        print(f"Found in {c}:")
        for m in re.finditer(r'https?://[a-zA-Z0-9\.\-_/]+', r.text):
            if any(k in m.group(0) for k in ('wecollege', 'api', 'source', 'embed', 'stream')):
                print("  ", m.group(0))
