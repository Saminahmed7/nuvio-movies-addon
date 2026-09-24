from curl_cffi import requests
import re

url = "https://www.movy.sx/_next/static/chunks/1zyk0gv4kwtq5.js"
headers = {'User-Agent': 'Mozilla/5.0'}
text = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10).text
print("Length of 1zyk:", len(text))

# Search for artplayer initialization
pos = text.find('Artplayer')
while pos != -1:
    print("--- CONTEXT ARTPLAYER ---")
    print(text[max(0, pos - 100): min(len(text), pos + 500)])
    pos = text.find('Artplayer', pos + 1)
    if pos > 20000:
        break
