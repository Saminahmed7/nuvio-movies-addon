import asyncio
import httpx
import time
from urllib.parse import quote

HEADERS = {
    'Accept': '*/*',
    'Origin': 'https://player.videasy.to',
    'Referer': 'https://player.videasy.to/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

async def fetch_videasy(tmdb_id, title, year, ctype='movie', season=1, episode=1, imdb_id=''):
    t0 = time.time()
    enc_title = quote(quote(title, safe=''), safe='')
    async with httpx.AsyncClient(headers=HEADERS, timeout=6.0) as client:
        # Step 1: Get seed
        seed_r = await client.get(f'https://api.speedracelight.com/seed?mediaId={tmdb_id}')
        if seed_r.status_code != 200:
            return []
        seed = seed_r.json().get('seed')

        # Step 2: Fetch cdn and m4uhd concurrently
        async def query_server(srv):
            if ctype == 'movie':
                url = f'https://api.speedracelight.com/{srv}/sources-with-title?title={enc_title}&mediaType=movie&year={year}&tmdbId={tmdb_id}&imdbId={imdb_id}&enc=2&seed={seed}'
            else:
                url = f'https://api.speedracelight.com/{srv}/sources-with-title?title={enc_title}&mediaType=tv&year={year}&episodeId={episode}&seasonId={season}&tmdbId={tmdb_id}&imdbId={imdb_id}&enc=2&seed={seed}'
            r = await client.get(url)
            if r.status_code == 200 and len(r.text) > 20:
                dec = await client.post('https://enc-dec.app/api/dec-videasy', json={'text': r.text, 'id': str(tmdb_id), 'seed': seed})
                if dec.status_code == 200:
                    return dec.json().get('result', {})
            return {}

        results = await asyncio.gather(query_server('cdn'), query_server('m4uhd'))
        t1 = time.time()
        print(f'{title} ({ctype}) fetched in {t1-t0:.2f}s:')
        for i, res in enumerate(results):
            srv_name = ['cdn (Yoru)', 'm4uhd (Breach)'][i]
            sources = res.get('sources', [])
            subs = res.get('subtitles', [])
            print(f'  {srv_name}: {len(sources)} sources, {len(subs)} subs')
            for s in sources:
                print(f'    [{s.get("quality")}] {s.get("url")[:70]}...')

async def main():
    await fetch_videasy(550, 'Fight Club', 1999, 'movie', imdb_id='tt0137523')
    await fetch_videasy(106379, 'Fallout', 2024, 'tv', season=1, episode=1, imdb_id='tt12637874')
    await fetch_videasy(1396, 'Breaking Bad', 2008, 'tv', season=1, episode=1, imdb_id='tt0903747')

if __name__ == '__main__':
    asyncio.run(main())
