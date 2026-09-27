import requests
from bs4 import BeautifulSoup
import re

# Check Goojara movie page
url = 'https://goojara.to/movie/the-shawshank-redemption-1994/'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f'Goojara movie: {r.status_code}')

soup = BeautifulSoup(r.text, 'html.parser')

# Look for watch/play links
links = soup.select('a[href*="watch"], a[href*="play"], a[href*="server"], a[href*="stream"]')
print(f'Watch/Play links: {len(links)}')
for link in links[:10]:
    print(f'  {link.get("href")} - {link.get_text(strip=True)[:60]}')

# Check for iframes
iframes = soup.select('iframe')
print(f'iframes: {len(iframes)}')
for iframe in iframes[:3]:
    print(f'  src: {iframe.get("src")}')

# Search for m3u8, mp4
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8[:3]}')

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f'mp4: {mp4[:3]}')