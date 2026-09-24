import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

matches = re.finditer(r'(?:emit\(["\']load["\']|\.trigger\(["\']load["\']|\.load\(|url:)', text)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 150)
    print("--- EMIT LOAD ---")
    print(text[start:end])
    break
