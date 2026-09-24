from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
text = requests.get(url, impersonate='chrome133a').text

for fn in ['EQ', 'SQ']:
    pos = text.find(f'function {fn}(')
    if pos == -1: pos = text.find(f'{fn}=')
    if pos == -1: pos = text.find(f'{fn} =')
    if pos == -1: pos = text.find(f'const {fn}')
    print(f"=== {fn} ===")
    if pos != -1:
        print(text[max(0, pos - 100): pos + 600])
    else:
        for m in re.finditer(rf'\b{fn}\s*=\s*', text):
            print(text[max(0, m.start() - 100): m.start() + 600])
