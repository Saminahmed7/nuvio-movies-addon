import httpx
import re

text = httpx.get('https://www.rivestream.app/_next/static/chunks/2427-f1dd7c2a4b7832e1.js').text

# Find all server objects with label, value, star, category, src
pos = text.find('Turbo-Server')
if pos != -1:
    chunk = text[max(0, pos - 4000): min(len(text), pos + 4000)]
    print(chunk[:7000])
