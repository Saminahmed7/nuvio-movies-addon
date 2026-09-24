from curl_cffi import requests
import re

url = 'https://vidfast.pro/_next/static/chunks/365-71c2a8238d040bc9.js'
r = requests.get(url, impersonate='chrome133a', timeout=15)
text = r.text

# Search for API endpoints
apis = re.findall(r'["\'`](/api/[^"\'`\s]+)["\'`]', text)
print('API endpoints in vidfast chunk 365:')
for a in set(apis):
    print(' ', a)

# Search for fetch calls
fetches = re.findall(r'fetch\(["\`]([^"\'`]+)["\`]', text)
print('\nFetch URLs:')
for f in set(fetches):
    if 'api' in f or 'source' in f or 'embed' in f or 'stream' in f:
        print(' ', f)