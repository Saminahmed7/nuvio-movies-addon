from curl_cffi import requests
from bs4 import BeautifulSoup

r = requests.get('https://67movies.st/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, impersonate='chrome133a', timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
print("67movies links:")
for l in [x for x in links if any(k in x for k in ('watch', 'movie', 'film', 'view'))][:10]:
    print(" ", l)
