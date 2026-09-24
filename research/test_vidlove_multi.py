from curl_cffi import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

# Test 1: Another Movie - Fight Club (tmdb: 550)
url_movie = "https://api.vidlove.cc/movie?id=550&mode=json&sources=vidapi"
r = requests.get(url_movie, headers=headers, impersonate='chrome133a', timeout=10)
print(f"Fight Club (550): status {r.status_code}")
if r.status_code == 200:
    res = r.json()
    print("  Source:", res.get("source", {}).get("label"))
    print("  URL snippet:", res.get("source", {}).get("url")[:80])

# Test 2: TV Series - Breaking Bad (tmdb: 1396) S1E1
tv_urls = [
    "https://api.vidlove.cc/tv?id=1396&season=1&episode=1&mode=json&sources=vidapi",
    "https://api.vidlove.cc/tv?id=1396&s=1&e=1&mode=json&sources=vidapi",
    "https://api.vidlove.cc/show?id=1396&season=1&episode=1&mode=json&sources=vidapi",
    "https://api.vidlove.cc/tv/1396/1/1?mode=json&sources=vidapi"
]

for u in tv_urls:
    try:
        tr = requests.get(u, headers=headers, impersonate='chrome133a', timeout=10)
        print(f"TV check ({u.split('?')[0]}): status {tr.status_code}")
        if tr.status_code == 200:
            tres = tr.json()
            print("  Found TV URL!", tres.get("source", {}).get("label"), tres.get("source", {}).get("url")[:60] if tres.get("source") else tres)
            break
    except Exception as e:
        print(f"  Error on {u}: {e}")
