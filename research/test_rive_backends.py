from curl_cffi import requests
from bs4 import BeautifulSoup
import re

candidates = [
    ('peachify', 'https://peachify.top/embed/movie/27205?autoPlay=true'),
    ('multiembed', 'https://multiembed.mov/directstream.php?video_id=27205&tmdb=1'),
    ('pstream', 'https://iframe.pstream.mov/embed/tmdb-movie-27205')
]

for name, url in candidates:
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://www.rivestream.app/'}, impersonate='chrome133a', timeout=10)
        print(f"=== {name} (HTTP {r.status_code}, {len(r.text)} bytes) ===")
        # Check for direct video links, m3u8, or iframe
        m3u8 = re.findall(r'https?://[^\s"\'\\<>]+\.m3u8[^\s"\'\\<>]*', r.text)
        if m3u8:
            print("  m3u8 found:", m3u8)
        soup = BeautifulSoup(r.text, 'lxml')
        iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
        if iframes:
            print("  iframes found:", iframes)
        scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
        print("  scripts count:", len(scripts))
    except Exception as e:
        print(f"=== {name} ERROR: {e} ===")
