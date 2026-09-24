from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://phantomflix.net/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

print("PhantomFlix title:", soup.title.string if soup.title else None)
scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("Scripts in PhantomFlix:")
for s in scripts:
    print(" ", s)

# Find sample links
links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
print("\nLinks:")
for l in [x for x in links if any(k in x for k in ('movie', 'watch', 'tv'))][:10]:
    print(" ", l)
