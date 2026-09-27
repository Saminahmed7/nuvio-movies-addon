import requests

url = 'https://raw.githubusercontent.com/SaurabhKaperwan/CSX/master/CineStream/src/main/kotlin/com/megix/CineStreamUtils.kt'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    with open('research/CineStreamUtils.kt', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print('Saved to research/CineStreamUtils.kt')
    print(f'Length: {len(r.text)}')
else:
    print(f'CineStreamUtils: {r.status_code}')