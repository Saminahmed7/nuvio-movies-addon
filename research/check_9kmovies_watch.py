import requests
from bs4 import BeautifulSoup
import re

# Check 9kMovies movie page - try to find a movie page
# First get a category page
url = 'https://9kmovies.llc/category/hollywood-latest-movies/'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
print(f'Category page: {r.status_code}')

soup = BeautifulSoup(r.text, 'html.parser')
# Find movie links
links = soup.select('a[href]')
movie_links = [l['href'] for l in links if l.get('href') and '/movie/' in l['href'] or '/download-' in l['href']]
print(f'Movie links: {len(movie_links)}')
for l in movie_links[:5]:
    print(f'  {l}')

if movie_links:
    # Check a movie page
    movie_url = movie_links[0]
    if not movie_url.startswith('http'):
        movie_url = 'https://9kmovies.llc' + movie_url
    
    r2 = requests.get(movie_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'\nMovie page: {r2.status_code}')
    
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    
    # Look for download/stream links
    download_links = soup2.select('a[href*="download"], a[href*="stream"], a[href*="watch"]')
    print(f'Download/stream links: {len(download_links)}')
    for link in download_links[:5]:
        print(f'  {link.get("href")} - {link.get_text(strip=True)[:50]}')
    
    # Search for m3u8, mp4
    m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r2.text)
    print(f'm3u8: {m3u8[:3]}')
    
    mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r2.text)
    print(f'mp4: {mp4[:3]}')
    
    # Check for iframes
    iframes = soup2.select('iframe')
    print(f'iframes: {len(iframes)}')
    for iframe in iframes[:3]:
        print(f'  src: {iframe.get("src")}')