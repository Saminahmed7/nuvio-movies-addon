import requests

# Check phisher98 source for BanglaPlex
url = 'https://api.github.com/repos/phisher98/cloudstream-extensions-phisher/contents/BanglaPlex/src/main/kotlin/com/phisher/extensions'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    items = r.json()
    for item in items:
        print(f"{item['type']}: {item['name']}")
else:
    print(f'Status: {r.status_code}')