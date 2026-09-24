from curl_cffi import requests
import re

url = 'https://anyembed.xyz/assets/Watch-Kd47OxZq.js'
r = requests.get(url, headers={'Referer': 'https://anyembed.xyz/movie/27205'}, impersonate='chrome133a', timeout=10)
text = r.text
print("Length of Watch.js:", len(text))

# Search for /api/ routes
apis = re.findall(r'["\'`](/(?:api|embed|stream|source|play|v\d)[^"\'`\s]+)["\'`]', text)
print("APIs in Watch.js:", set(apis))

# Search for external URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'github', 'cloudflare'))]
print("External URLs in Watch.js:")
for u in clean[:20]:
    print(" ", u)
