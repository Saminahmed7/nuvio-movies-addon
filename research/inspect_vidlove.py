from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://player.vidlove.cc/embed/movie/27205?server=Dark'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://phantomflix.net/'
}

r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
print("Vidlove status:", r.status_code, len(r.text))

soup = BeautifulSoup(r.text, 'lxml')
print("Title:", soup.title.string if soup.title else None)

# Find iframes or video players
iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
print("iframes in Vidlove:", iframes)

# Find stream URLs
m3u8 = re.findall(r'https?://[^\s"\'\\<>]+\.m3u8[^\s"\'\\<>]*', r.text)
print("m3u8 in Vidlove:", m3u8)

scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
print("Scripts in Vidlove:", scripts[:10])

with open('research/vidlove_27205.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
