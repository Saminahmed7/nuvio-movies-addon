from curl_cffi import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
for c in ['72f7ae58a2fa97e2.js', '4451fba4a875935b.js']:
    url = f'https://peachify.top/_next/static/chunks/{c}'
    r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
    print(f"=== {c} ({len(r.text)} bytes) ===")
    # Look for fetch or api
    apis = re.findall(r'["\'`](/(?:api|embed|stream|source|v\d)[^"\'`\s]+)["\'`]', r.text)
    if apis:
        print("  APIs:", set(apis))
    fetches = re.findall(r'fetch\([\"\'`]([^\"\'`]+)[\"\'`]', r.text)
    if fetches:
        print("  Fetches:", set(fetches))
