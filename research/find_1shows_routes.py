from curl_cffi import requests
from bs4 import BeautifulSoup
import re

r = requests.get('http://1shows.bz/', headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a')
# Search for hrefs
hrefs = re.findall(r'href=["\']([^"\']+)["\']', r.text)
print("Hrefs in 1shows:")
for h in set(hrefs):
    if not h.startswith('#') and not h.startswith('http'):
        print(" ", h)
