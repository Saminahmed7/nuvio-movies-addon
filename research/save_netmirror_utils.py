import requests

url = 'https://raw.githubusercontent.com/Sushan64/NetMirror-Extension/master/Netmirror/src/main/kotlin/com/horis/cncverse/Utils.kt'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    with open('research/NetMirror_Utils.kt', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print('Saved to research/NetMirror_Utils.kt')
    print(f'Length: {len(r.text)}')
else:
    print(f'Status: {r.status_code}')