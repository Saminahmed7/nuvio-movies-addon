from curl_cffi import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

for name, url in [("Aether", "https://aether.ist/movie/27205"), ("FlyStream", "https://flystream.net/movie/27205")]:
    r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
    print(f"\n==================== {name} ====================")
    soup = BeautifulSoup(r.text, 'lxml')
    print("Title:", soup.title.string if soup.title else None)
    iframes = soup.find_all('iframe')
    print("Iframes:", [i.get('src') for i in iframes])
    scripts = soup.find_all('script')
    print("Scripts count:", len(scripts))
    for s in scripts:
        src = s.get('src', '')
        text = s.string or ''
        if any(w in src or w in text for w in ['player', 'embed', 'stream', 'api', 'source', 'video']):
            print("  Script match:", src if src else text[:120])
