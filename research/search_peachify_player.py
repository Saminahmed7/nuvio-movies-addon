from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10)
text = r.text

# Find all fetches or external URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'nextjs', 'github', 'flagsapi'))]
print("URLs in 72f7ae58a2fa97e2.js:")
for u in clean:
    print(" ", u)

# Search for any endpoint
for m in re.finditer(r'["\'`](/(?:api|api/v\d|source|stream|backend|data)[^"\'`\s]+)["\'`]', text):
    print("Endpoint:", m.group(1))
