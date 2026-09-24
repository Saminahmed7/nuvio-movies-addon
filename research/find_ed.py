import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

matches = re.finditer(r'(?:function ed\(|var ed\s*=|let ed\s*=|const ed\s*=)', text)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 3000)
    print("--- CONTEXT ED ---")
    print(text[start:end])
