import requests
from bs4 import BeautifulSoup
import re

# Check BanglaPlex watch page
url = 'https://banglaplex.biz/watch/the-vvaan.html'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f'BanglaPlex watch: {r.status_code}')
soup = BeautifulSoup(r.text, 'html.parser')

# Look for iframe, video, source, m3u8, mp4
iframes = soup.select('iframe')
print(f'iframes: {len(iframes)}')
for iframe in iframes[:3]:
    print(f'  src: {iframe.get("src")}')

# Check for video sources
videos = soup.select('video, source')
print(f'video/source tags: {len(videos)}')
for v in videos[:3]:
    print(f'  src: {v.get("src")}')

# Search for m3u8, mp4 in page
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8[:3]}')

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f'mp4: {mp4[:3]}')

# Check for embed scripts
scripts = soup.select('script[src]')
print(f'scripts: {len(scripts)}')
for s in scripts[:5]:
    print(f'  {s.get("src")}')