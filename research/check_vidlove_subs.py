import httpx

url = 'https://api.vidlove.cc/tv?id=106379&season=1&episode=1&mode=json&sources=vidapi'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}
r = httpx.get(url, headers=headers, timeout=8)
print(f'Status: {r.status_code}')
data = r.json()
print(f'Keys: {list(data.keys())}')
print(f'Subtitles: {data.get("subtitles")}')
print(f'Source keys: {list(data.get("source", {}).keys())}')