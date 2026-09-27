import requests
from bs4 import BeautifulSoup
import re

# Test Goojara
print("=== Goojara ===")
url = 'https://ww1.goojara.to'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.select('a[href]')
movie_links = [l['href'] for l in links if l.get('href') and any(k in l['href'] for k in ['/movie/', '/series/', '/watch/', '/play/'])]
print(f"Movie/Series links: {len(movie_links)}")
for l in movie_links[:5]:
    print(f"  {l}")

# Test BanglaPlex
print("\n=== BanglaPlex ===")
url2 = 'https://banglaplex.lat'
r2 = requests.get(url2, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
soup2 = BeautifulSoup(r2.text, 'html.parser')
links2 = soup2.select('a[href]')
movie_links2 = [l['href'] for l in links2 if l.get('href') and any(k in l['href'] for k in ['/movie/', '/series/', '/watch/', '/play/'])]
print(f"Movie/Series links: {len(movie_links2)}")
for l in movie_links2[:5]:
    print(f"  {l}")