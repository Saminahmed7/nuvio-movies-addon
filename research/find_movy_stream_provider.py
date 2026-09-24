from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.movy.sx/movie/27205?play=true'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://www.movy.sx/'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)

soup = BeautifulSoup(r.text, 'lxml')
scripts = [s.get('src') for s in soup.find_all('script') if s.get('src') and '_next/static/chunks' in s.get('src')]
print(f"Total chunks in Movy movie page: {len(scripts)}")

for s in scripts:
    u = f"https://www.movy.sx{s}"
    resp = requests.get(u, headers=headers, impersonate='chrome133a', timeout=10)
    text = resp.text
    # Search for stream providers
    providers = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
    clean = [p for p in set(providers) if any(k in p for k in ('vidsrc', 'embed', 'player', 'stream', 'autoembed', 'vidlink', 'smashystream'))]
    if clean:
        print(f"In {s}:")
        for c in clean:
            print("  ", c)
