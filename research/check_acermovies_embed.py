from curl_cffi import requests
import re

base = 'https://acermovies.fun'
for path in ['/embed/27205', '/watch/27205', '/play/27205', '/stream/27205', '/player/27205']:
    r = requests.get(f'{base}{path}', impersonate='chrome133a', timeout=10)
    print(f'{path}: {r.status_code} - {r.url}')
    if r.status_code == 200:
        iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', r.text)
        if iframes:
            print(f'  iframes: {iframes}')
        m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
        if m3u8:
            print(f'  m3u8: {m3u8}')