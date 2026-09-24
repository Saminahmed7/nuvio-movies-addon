import httpx
from bs4 import BeautifulSoup
import re

r = httpx.get('https://docs.pstream.cfd/', headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
soup = BeautifulSoup(r.text, 'lxml')

links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
print("Docs links:")
for l in set(links):
    print(" ", l)
