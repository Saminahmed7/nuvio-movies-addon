import httpx
import re

url = 'https://vidcore.net/movie/27205'
r = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10, follow_redirects=True)
print(f'Status: {r.status_code}')
print(f'Final URL: {r.url}')

iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', r.text)
print(f'iframes: {iframes}')

m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
print(f'm3u8: {m3u8}')

# Also check for API calls in the page
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text)
print(f'scripts: {scripts[:10]}')