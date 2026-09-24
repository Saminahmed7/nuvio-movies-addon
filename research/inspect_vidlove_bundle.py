from curl_cffi import requests
import re

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://player.vidlove.cc/'
}

r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
text = r.text
print("Length of vidlove index.js:", len(text))

# Search for api routes
apis = re.findall(r'["\'`](/(?:api|embed|stream|source|play|v\d)[^"\'`\s]+)["\'`]', text)
print("APIs in vidlove index.js:", set(apis))

# Search for external URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'github'))]
print("External URLs in vidlove index.js:")
for u in clean[:15]:
    print(" ", u)
