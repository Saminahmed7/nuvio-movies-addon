from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'http://1shows.bz/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

print("1shows title:", soup.title.string if soup.title else None)
links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
print("Sample links:")
for l in [x for x in links if any(k in x for k in ('watch', 'movie', 'tv'))][:10]:
    print(" ", l)

scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("\nScripts in 1shows:")
for s in scripts[:10]:
    print(" ", s)
