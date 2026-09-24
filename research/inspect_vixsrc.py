from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://vixsrc.to/movie/27205'
r = requests.get(url, impersonate='chrome133a', timeout=10)
print("=== vixsrc.to/movie/27205 ===")
print("Status:", r.status_code)

soup = BeautifulSoup(r.text, 'lxml')
print("Title:", soup.title.string if soup.title else None)

iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
print("iframes:", iframes)

scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("scripts:", scripts)

m3u8 = re.findall(r'https?://[^\s"\'\\<>]+\.m3u8[^\s"\'\\<>]*', r.text)
print("m3u8 found:", m3u8)

with open('research/vixsrc_27205.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
