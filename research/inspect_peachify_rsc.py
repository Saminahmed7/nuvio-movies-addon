from curl_cffi import requests
import re

url = 'https://peachify.top/embed/movie/27205?autoPlay=true'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)

pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*)"\]\)', r.text)
for idx, p in enumerate(pushes):
    try:
        unescaped = bytes(p, 'utf-8').decode('unicode_escape')
    except Exception:
        unescaped = p
    print(f"--- PUSH {idx} ---")
    print(unescaped[:1500])
