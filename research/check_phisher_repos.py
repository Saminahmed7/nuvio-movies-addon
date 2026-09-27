import requests

# Check phisher98's other repos for source
url = 'https://api.github.com/users/phisher98/repos'
r = requests.get(url, timeout=10, params={'per_page': 100})
repos = r.json()
for repo in repos:
    if 'extension' in repo['name'].lower() or 'provider' in repo['name'].lower() or 'cloudstream' in repo['name'].lower():
        print(f"{repo['name']} - {repo['description']}")