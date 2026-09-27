import requests

# Check providers in this repo
for name in ['Bollyflix', 'CineStream', 'MoviesDrive', 'Moviesmod', 'VegaMovies']:
    url = f'https://api.github.com/repos/SaurabhKaperwan/CSX/contents/{name}'
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        items = r.json()
        for item in items:
            print(f'{name}: {item["type"]}: {item["name"]}')
    else:
        print(f'{name}: Status {r.status_code}')