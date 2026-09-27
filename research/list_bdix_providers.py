import requests

url = 'https://raw.githubusercontent.com/redowan99/Redowan-CloudStream/builds/plugins.json'
r = requests.get(url, timeout=10)
plugins = r.json()

print(f'Total providers: {len(plugins)}')
for p in plugins:
    status = 'ACTIVE' if p.get('status') == 1 else 'INACTIVE'
    desc = p.get('description', 'No description')
    print(f"{p['name']} ({p['language']}) - {status} - {p['tvTypes']} - {desc[:80]}")