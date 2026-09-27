import requests
from bs4 import BeautifulSoup
import re

# Check a specific movie page
url = 'https://9kmovies2.life/the-paradise-2026-hindi-line-telugu-hdtsno-ads/'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f'Movie page: {r.status_code}')

soup = BeautifulSoup(r.text, 'html.parser')

# Look for download links
download_links = soup.select('a[href*="download"], a[href*="server"], a[href*="watch"], a[href*="stream"]')
print(f'Download/Stream links: {len(download_links)}')
for link in download_links[:10]:
    print(f'  {link.get("href")} - {link.get_text(strip=True)[:60]}')

# Search for m3u8, mp4
m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8[:3]}')

mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
print(f'mp4: {mp4[:3]}')

# Check for iframes
iframes = soup.select('iframe')
print(f'iframes: {len(iframes)}')
for iframe in iframes[:3]:
    print(f'  src: {iframe.get("src")}')

# Check for any scripts with sources
scripts = soup.select('script')
for s in scripts:
    if s.string and ('source' in s.string or 'file:' in s.string or 'm3u8' in s.string or 'mp4' in s.string):
        print(f'Script with source: {s.string[:300]}')
        break