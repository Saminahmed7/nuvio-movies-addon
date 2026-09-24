import httpx
from bs4 import BeautifulSoup
import re

url = 'https://vidfast.vc/movie/27205'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.rivestream.app/'
}

r = httpx.get(url, headers=headers, follow_redirects=True, timeout=12)
print("vidfast.vc/movie/27205 status:", r.status_code, len(r.text))

# Search for any string containing /api/ or iframe or script or embed
soup = BeautifulSoup(r.text, 'lxml')
scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("Scripts:")
for s in scripts:
    print(" ", s)

# Search HTML for data or JSON
for script in soup.find_all('script'):
    if not script.get('src') and script.string:
        if any(k in script.string for k in ('stream', 'source', 'token', 'url', 'video', 'embed')):
            print("Inline script snippet:", script.string[:200])
