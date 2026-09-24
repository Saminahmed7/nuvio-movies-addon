import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

# Find where ea or V or Artplayer is rendered
matches = re.finditer(r'(?:<V|<ea|\.jsx\(V|\.jsx\(ea|\.jsxs\(V|\.jsxs\(ea)', text)
for m in matches:
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 300)
    print("--- CONTEXT CALL ---")
    print(text[start:end])
