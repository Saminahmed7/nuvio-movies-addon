import requests

url = 'https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/builds/plugins.json'
r = requests.get(url, timeout=10)
plugins = r.json()
for p in plugins:
    if p.get('status') == 1:
        desc = p.get('description', 'No description')
        print(f"{p['name']} - {desc[:60]}")