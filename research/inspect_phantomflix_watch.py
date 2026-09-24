import httpx
from bs4 import BeautifulSoup
import re

url = 'https://phantomflix.net/watch/movie/27205'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = httpx.get(url, headers=headers, follow_redirects=True, timeout=12)

soup = BeautifulSoup(r.text, 'lxml')
print("Title:", soup.title.string if soup.title else None)

iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
print("iframes:", iframes)

# Search for any streaming URLs or APIs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', r.text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'nextjs', 'github', 'tmdb.org'))]
print("Streaming URLs:")
for u in clean:
    print(" ", u)

# Check scripts
for s in soup.find_all('script'):
    if s.get('src') and 'watch' in s.get('src'):
        print("Watch script:", s.get('src'))
