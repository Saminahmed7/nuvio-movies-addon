from curl_cffi import requests
import re

url = 'https://atlantic.st/assets/index-BA2TuH7B.js'
r = requests.get(url, impersonate='chrome133a', timeout=10)
text = r.text
print("Length of Atlantic index.js:", len(text))

# Search for streaming providers, embeds, APIs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'github', 'cloudflare'))]
print("URLs in Atlantic:")
for u in clean[:20]:
    print(" ", u)

# Search for /api/ routes
apis = re.findall(r'["\'`](/(?:api|embed|stream|source|play|v\d)[^"\'`\s]+)["\'`]', text)
if apis:
    print("APIs in Atlantic:", set(apis))
