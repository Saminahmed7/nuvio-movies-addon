from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://stellar.gdn/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
soup = BeautifulSoup(r.text, 'lxml')

# Find watch links or scripts
links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
print("Stellar sample links:")
for l in [x for x in links if any(k in x for k in ('watch', 'movie', 'tv'))][:10]:
    print(" ", l)

scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("\nStellar scripts:")
for s in scripts[:10]:
    print(" ", s)
