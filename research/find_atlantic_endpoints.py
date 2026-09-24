from curl_cffi import requests
import re

url = 'https://atlantic.st/assets/index-BA2TuH7B.js'
text = requests.get(url, impersonate='chrome133a').text

for target in ['api.atlantic.st', 'stellar.hls.lol', 'cdn.hls.lol']:
    print(f"=== SEARCH {target} ===")
    pos = text.find(target)
    while pos != -1:
        print(text[max(0, pos - 150): min(len(text), pos + 350)])
        pos = text.find(target, pos + 1)
        if pos > 200000:
            break
