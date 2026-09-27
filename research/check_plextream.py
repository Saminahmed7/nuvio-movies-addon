import requests
from bs4 import BeautifulSoup
import re

# Check the plextream embed
url = 'https://plextream.work/embed.php?id=S205GHo1'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://banglaplex.biz/'})
print(f'plextream embed: {r.status_code}')
soup = BeautifulSoup(r.text, 'html.parser')

# Check for video sources
videos = soup.select('video, source')
print(f'video/source tags: {len(videos)}')
for v in videos[:3]:
    print(f'  src: {v.get("src")}')

# Search for m3u8, mp4
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8[:3]}')

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f'mp4: {mp4[:3]}')

# Check for any sources in scripts
scripts = soup.select('script')
for s in scripts:
    if s.string and ('m3u8' in s.string or 'source' in s.string or 'file:' in s.string):
        print(f'Script with source: {s.string[:200]}')
        break

# Check iframe
iframes = soup.select('iframe')
print(f'iframes: {len(iframes)}')
for iframe in iframes[:3]:
    print(f'  src: {iframe.get("src")}')

# Save for analysis
with open('research/plextream_embed.html', 'w', encoding='utf-8') as f:
    f.write(r.text)