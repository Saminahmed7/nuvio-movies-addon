from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
text = requests.get(url, impersonate='chrome133a').text

for target in ['vidvault.ru', 'vidrock.net/api']:
    print(f"=== {target} ===")
    pos = text.find(target)
    while pos != -1:
        print(text[max(0, pos - 150): min(len(text), pos + 400)])
        pos = text.find(target, pos + 1)
        if pos > 200000:
            break
