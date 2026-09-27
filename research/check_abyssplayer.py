import requests
from bs4 import BeautifulSoup
import re

# Check the abyssplayer embed
url = 'https://abyssplayer.com/x-UxcyUVs'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://plextream.work/'})
print(f'abyssplayer: {r.status_code}')
soup = BeautifulSoup(r.text, 'html.parser')

# Check for video sources
videos = soup.select('video, source')
print(f'video/source tags: {len(videos)}')
for v in videos[:3]:
    print(f'  src: {v.get("src")}')

# Search for m3u8, mp4
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8[:5]}')

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f'mp4: {mp4[:5]}')

# Check scripts
scripts = soup.select('script')
for s in scripts:
    if s.string and ('m3u8' in s.string or 'source' in s.string or 'file:' in s.string or 'master' in s.string):
        print(f'Script with source: {s.string[:500]}')
        break

# Check iframe
iframes = soup.select('iframe')
print(f'iframes: {len(iframes)}')
for iframe in iframes[:3]:
    print(f'  src: {iframe.get("src")}')

# Check for any data attributes
for tag in soup.find_all(attrs={"data-src": True}):
    print(f'data-src: {tag.get("data-src")}')

for tag in soup.find_all(attrs={"data-file": True}):
    print(f'data-file: {tag.get("data-file")}')

# Save for analysis
with open('research/abyssplayer_embed.html', 'w', encoding='utf-8') as f:
    f.write(r.text)