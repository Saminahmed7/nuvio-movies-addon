import requests
import re

r = requests.get('https://player.vidzee.wtf/', timeout=5)
print("status:", r.status_code)
scripts = re.findall(r'src=["\']([^"\']+)["\']', r.text)
print("scripts:", scripts)

# Also check for movie/tv player URLs, e.g. /movie/550 or /watch or /api
for path in ['/movie/550', '/tv/1399/1/1', '/embed/550', '/api/server']:
    res = requests.get(f'https://player.vidzee.wtf{path}', timeout=5)
    print(f"Path {path}: status {res.status_code}, len: {len(res.text)}")
    if res.status_code == 200 and 'script' in res.text:
        more_scripts = re.findall(r'src=["\']([^"\']+)["\']', res.text)
        print(f"  Scripts on {path}:", more_scripts)
