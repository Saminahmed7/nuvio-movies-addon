from curl_cffi import requests
import re
import json

# The b35ebba4 field might be a key for fetching sources
# Let's try the API with that key
r = requests.get('https://www.movy.sx/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
data = json.loads(next_data[0])
page_props = data.get("props", {}).get("pageProps", {})
details = page_props.get("details", {})

b35_key = details.get("b35ebba4")
tmdb_id = details.get("tmdbId")
print(f"b35ebba4 key: {b35_key}")
print(f"tmdbId: {tmdb_id}")

# Try various API endpoints with this key
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.movy.sx/',
    'Origin': 'https://www.movy.sx'
}

endpoints = [
    f'https://api.wecollege.net/movie/{tmdb_id}',
    f'https://api.wecollege.net/movie/{tmdb_id}?key={b35_key}',
    f'https://api.wecollege.net/stream/{tmdb_id}',
    f'https://api.wecollege.net/sources/{tmdb_id}',
    f'https://api.wecollege.net/watch/{tmdb_id}',
    f'https://db.wecollege.net/movie/{tmdb_id}',
    f'https://www.movy.sx/api/movie/{tmdb_id}',
    f'https://www.movy.sx/api/watch/{tmdb_id}',
]

for ep in endpoints:
    try:
        resp = requests.get(ep, headers=headers, impersonate='chrome133a', timeout=10)
        print(f"{ep} -> HTTP {resp.status_code:3} ({len(resp.text)} bytes)")
        if resp.status_code == 200:
            print(f"  Response: {resp.text[:500]}")
    except Exception as e:
        print(f"{ep} -> ERROR: {e}")