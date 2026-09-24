import httpx

# Check movie
url = 'https://api.vidlove.cc/movie?id=27205&mode=json&sources=vidapi'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}
r = httpx.get(url, headers=headers, timeout=8)
print(f'Movie Status: {r.status_code}')
data = r.json()
print(f'Movie Subtitles: {data.get("subtitles")}')

# Check another movie
url2 = 'https://api.vidlove.cc/movie?id=550&mode=json&sources=vidapi'  # Fight Club
r2 = httpx.get(url2, headers=headers, timeout=8)
print(f'\nFight Club Status: {r2.status_code}')
data2 = r2.json()
print(f'Fight Club Subtitles: {data2.get("subtitles")}')