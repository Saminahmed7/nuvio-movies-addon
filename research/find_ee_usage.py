from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

# Find where "ee" is used
matches = re.finditer(r'(?:ee\[|ee\.find|ee\.map|apis\[|\.apis\b)', text)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 300)
    print("--- CONTEXT EE ---")
    print(text[start:end])
