import requests
from bs4 import BeautifulSoup
import re

# Check BanglaPlex watch page
url = 'https://banglaplex.biz/watch/the-vvaan.html'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f"Watch page: {r.status_code}")
soup = BeautifulSoup(r.text, 'html.parser')

# Look for iframes
iframes = soup.select('iframe')
print(f"iframes: {len(iframes)}")
for iframe in iframes[:3]:
    print(f"  src: {iframe.get('src')}")

# Look for video sources
videos = soup.select('video, source')
print(f"video/source tags: {len(videos)}")
for v in videos[:3]:
    print(f"  src: {v.get('src')}")

# Search for m3u8, mp4
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f"m3u8: {m3u8[:3]}")

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f"mp4: {mp4[:3]}")

# Check for embed scripts
scripts = soup.select('script')
for s in scripts:
    if s.string and ('m3u8' in s.string or 'source' in s.string or 'file:' in s.string or 'stream' in s.string):
        print(f"Script with stream info: {s.string[:300]}")
        break

# Check for any data attributes
for tag in soup.find_all(attrs={"data-src": True}):
    print(f"data-src: {tag.get('data-src')}")

for tag in soup.find_all(attrs={"data-url": True}):
    print(f"data-url: {tag.get('data-url')}")

# Check for any buttons or links to stream
buttons = soup.select('button, a')
stream_buttons = [b for b in buttons if b.get_text(strip=True) and any(k in b.get_text(strip=True).lower() for k in ['watch', 'play', 'stream', 'embed'])]
print(f"Stream buttons: {len(stream_buttons)}")
for b in stream_buttons[:5]:
    print(f"  {b.get_text(strip=True)} -> {b.get('href', 'no href')}")