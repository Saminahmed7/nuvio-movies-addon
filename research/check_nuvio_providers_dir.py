import requests

# Check providers directory
url = 'https://api.github.com/repos/phisher98/nuvio-providers/contents/providers'
r = requests.get(url, timeout=10)
items = r.json()
for item in items:
    print(f"{item['type']}: {item['name']}")