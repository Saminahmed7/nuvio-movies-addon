import requests

r = requests.get('https://raw.githubusercontent.com/self-similarity/MegaRepo/builds/plugins.json', timeout=10)
plugins = r.json()
print(f'Total plugins: {len(plugins)}')
english_movies = []
for p in plugins:
    tv = p.get('tvTypes', [])
    lang = p.get('language', '')
    if ('Movie' in tv or 'TvSeries' in tv) and lang == 'en':
        english_movies.append(p)

print(f'English Movie/TV plugins: {len(english_movies)}')
for p in english_movies[:30]:
    print(f"- {p.get('name')}: {p.get('repositoryUrl', '')} (internalUrl: {p.get('internalName')})")
