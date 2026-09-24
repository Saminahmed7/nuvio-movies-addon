from curl_cffi import requests
import re

url = 'https://peachify.top/embed/movie/27205?autoPlay=true'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)

pushes = "".join(re.findall(r'self\.__next_f\.push\(\[1,"(.*)"\]\)', r.text))
try:
    unescaped = bytes(pushes, 'utf-8').decode('unicode_escape')
except Exception:
    unescaped = pushes

pos = unescaped.find('"$L7"')
if pos == -1:
    pos = unescaped.find('7:[')
if pos != -1:
    print(unescaped[pos - 50: pos + 1000])
else:
    print("Search for 27205 in unescaped:")
    for m in re.finditer(r'27205', unescaped):
        print(unescaped[max(0, m.start()-100): min(len(unescaped), m.end()+300)])
