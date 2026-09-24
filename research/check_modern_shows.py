from curl_cffi import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

shows = [
    ("Fallout", 106379, 1, 1),
    ("House of the Dragon", 94997, 1, 1),
    ("Stranger Things", 66732, 1, 1),
    ("The Boys", 76479, 1, 1),
]

for name, tmdb_id, s, e in shows:
    url = f"https://api.vidlove.cc/tv?id={tmdb_id}&season={s}&episode={e}&mode=json&sources=vidapi"
    r = requests.get(url, headers=headers, impersonate='chrome133a')
    if r.status_code == 200:
        manifest = r.json().get('source', {}).get('manifest', '')
        has_1080 = "1920x" in manifest or "RESOLUTION=1920" in manifest
        has_4k = "3840x" in manifest or "RESOLUTION=3840" in manifest
        print(f"[{name}] HTTP 200 | Has 1080p: {has_1080} | Has 4K: {has_4k}")
        for line in manifest.splitlines():
            if line.startswith("#EXT-X-STREAM-INF"):
                print(f"   {line}")
    else:
        print(f"[{name}] HTTP {r.status_code}")
