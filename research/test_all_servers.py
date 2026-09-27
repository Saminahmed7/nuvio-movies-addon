import httpx
from urllib.parse import quote

HEADERS = {
    'Accept': '*/*',
    'Origin': 'https://player.videasy.to',
    'Referer': 'https://player.videasy.to/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

tmdb_id = '550'
title = 'Fight Club'
year = '1999'
imdb_id = 'tt0137523'
enc_title = quote(quote(title, safe=''), safe='')

seed_r = httpx.get(f'https://api.speedracelight.com/seed?mediaId={tmdb_id}', headers=HEADERS, timeout=5.0)
seed = seed_r.json()['seed']

servers = ['cdn', 'm4uhd', 'hdmovie', 'meine', 'lamovie', 'superflix']
for s in servers:
    url = f'https://api.speedracelight.com/{s}/sources-with-title?title={enc_title}&mediaType=movie&year={year}&tmdbId={tmdb_id}&imdbId={imdb_id}&enc=2&seed={seed}'
    try:
        r = httpx.get(url, headers=HEADERS, timeout=4.0)
        if r.status_code == 200 and len(r.text) > 20:
            dec = httpx.post('https://enc-dec.app/api/dec-videasy', json={'text': r.text, 'id': tmdb_id, 'seed': seed}, timeout=4.0)
            res = dec.json().get('result', {})
            sources = res.get('sources', [])
            print(f'{s}: {[x.get("quality") for x in sources]}')
        else:
            print(f'{s}: status {r.status_code}')
    except Exception as e:
        print(f'{s}: error {e}')
