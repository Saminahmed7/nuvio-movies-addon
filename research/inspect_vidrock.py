from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
r = requests.get(url, impersonate='chrome133a', timeout=10)
text = r.text
print("Length of vidrock index.js:", len(text))

# Search for APIs
apis = re.findall(r'["\'`](/(?:api|embed|stream|source|play|v\d)[^"\'`\s]+)["\'`]', text)
print("APIs in vidrock:", set(apis))

# Search for external URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'github', 'cloudflare'))]
print("External URLs in vidrock:")
for u in clean[:15]:
    print(" ", u)
