from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://vixsrc.to/embed/231752?token=20d3d0506929cf7b62cad9b94589e89e&t=SW5jZXB0aW9u&expires=1790223243&lang=en&skin=vixsrc&canPlayFHD=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://vixsrc.to/movie/27205'
}

r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
print("Status:", r.status_code, "Length:", len(r.text))

# Search for m3u8 or player
m3u8 = re.findall(r'https?://[^\s"\'\\<>]+\.m3u8[^\s"\'\\<>]*', r.text)
print("m3u8 found:", m3u8)

soup = BeautifulSoup(r.text, 'lxml')
print("Title:", soup.title.string if soup.title else None)

with open('research/vixsrc_embed.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

print("Saved research/vixsrc_embed.html")
