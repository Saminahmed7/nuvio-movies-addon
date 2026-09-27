import re

with open('research/vidzee_bundle.js', encoding='utf-8') as f:
    text = f.read()

urls = set(re.findall(r'https?://[^\s"\'`<>]+', text))
for u in sorted(urls):
    print("URL:", u)

# Search for /api
for m in re.finditer(r'/api[^\s"\'`]+', text):
    print("API:", m.group(0))

# Search for window or location
for m in re.finditer(r'window\.[a-zA-Z0-9_\.]+', text):
    print("Window:", m.group(0))
