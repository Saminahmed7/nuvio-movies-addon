import httpx
import re

text = httpx.get('https://www.rivestream.app/_next/static/chunks/2427-f1dd7c2a4b7832e1.js').text

# Find where /api/req/movie/ is used
for m in re.finditer(r'/api/req/(?:movie|tv)/[^\s"]*', text):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 300)
    print("--- CONTEXT ---")
    print(text[start:end])
