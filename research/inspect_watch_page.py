import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/pages/watch-50c3ac99e31a3038.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
print('Length of watch.js:', len(text))
print(text[:1500])
