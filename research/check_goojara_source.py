import requests

# Check phisher98 source for Goojara
url = 'https://api.github.com/repos/phisher98/cloudstream-extensions-phisher/contents/Goojara/src/main/kotlin/com/phisher/extensions'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    items = r.json()
    for item in items:
        print(f"{item['type']}: {item['name']}")
else:
    print(f'Status: {r.status_code}')