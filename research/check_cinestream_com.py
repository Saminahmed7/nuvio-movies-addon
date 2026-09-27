import requests

url = 'https://api.github.com/repos/SaurabhKaperwan/CSX/contents/CineStream/src/main/kotlin/com'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    items = r.json()
    for item in items:
        print(f'{item["type"]}: {item["name"]}')
else:
    print(f'Status: {r.status_code}')