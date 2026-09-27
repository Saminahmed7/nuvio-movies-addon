import requests

for name in ['Bollyflix', 'MoviesDrive', 'Moviesmod', 'VegaMovies']:
    url = f'https://api.github.com/repos/SaurabhKaperwan/CSX/contents/{name}/src/main/kotlin/com/megix'
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        items = r.json()
        for item in items:
            print(f'{name}: {item["type"]}: {item["name"]}')
    else:
        print(f'{name}: Status {r.status_code}')