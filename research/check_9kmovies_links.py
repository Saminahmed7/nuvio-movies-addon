import requests
from bs4 import BeautifulSoup
import re

# Check 9kMovies - try the main page
url = 'https://9kmovies.llc'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f'Main page: {r.status_code}')

soup = BeautifulSoup(r.text, 'html.parser')
# Find all links
links = soup.select('a[href]')
for link in links[:50]:
    href = link.get('href', '')
    text = link.get_text(strip=True)
    if any(k in href for k in ['movie', 'download', 'watch', 'series', 'category']) and text:
        print(f'  {href} - {text[:50]}')