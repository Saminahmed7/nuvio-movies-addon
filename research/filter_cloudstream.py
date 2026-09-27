import json
import requests

# Fetch the plugins list
url = 'https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/refs/heads/builds/plugins.json'
r = requests.get(url, timeout=10)
plugins = r.json()

# Filter for Movie/TvSeries providers (not anime-only)
movie_providers = []
for p in plugins:
    tv_types = p.get('tvTypes', [])
    if 'Movie' in tv_types or 'TvSeries' in tv_types:
        movie_providers.append({
            'name': p['name'],
            'language': p.get('language', 'en'),
            'description': p.get('description', ''),
            'tvTypes': tv_types,
            'url': p['url']
        })

# Print movie/TV providers
for p in movie_providers:
    print(f"{p['name']} ({p['language']}) - {p['tvTypes']}")
    print(f"  {p['description']}")
    print()