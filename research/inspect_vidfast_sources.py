import httpx
import re

url = 'https://vidfast.vc/_next/static/chunks/365-71c2a8238d040bc9.js'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
text = httpx.get(url, headers=headers, follow_redirects=True, timeout=15).text
print('Length of 365 on vidfast.vc:', len(text))

# Search for /api/ routes
apis = re.findall(r'["\'`](/(?:api|stream|source|play|v\d)[^"\'`\s]+)["\'`]', text)
print('APIs in vidfast chunk 365:', set(apis))

# Search for master.m3u8 or .m3u8
m3u8 = re.findall(r'https?://[^\s"\'\\<>]+\.m3u8[^\s"\'\\<>]*', text)
print('m3u8 mentions in 365:', set(m3u8[:10]))

# Search for endpoints or base URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if any(k in u for k in ('api', 'embed', 'player', 'stream', 'source', 'video'))]
print('\nStreaming/API URLs in 365:')
for u in clean[:15]:
    print(' ', u)
