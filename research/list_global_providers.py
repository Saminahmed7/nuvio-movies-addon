import requests

url = 'https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/refs/heads/builds/plugins.json'
r = requests.get(url, timeout=10)
plugins = r.json()

global_providers = []
for p in plugins:
    if p.get('status') == 1:
        lang = p.get('language', 'en')
        tv_types = p.get('tvTypes', [])
        if 'Movie' in tv_types or 'TvSeries' in tv_types:
            if lang in ['en', 'hi', 'mx', 'fr', 'de', 'pt-br', 'id', 'fil', 'ta', 'bn']:
                global_providers.append(p)

print(f'Global providers: {len(global_providers)}')
for p in global_providers:
    desc = p.get('description', 'No description')
    print(f"{p['name']} ({p['language']}) - {p['tvTypes']} - {desc[:80]}")