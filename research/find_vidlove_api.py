from curl_cffi import requests
import re

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
headers = {'User-Agent': 'Mozilla/5.0'}
text = requests.get(url, headers=headers, impersonate='chrome133a').text

pos = text.find('api.vidlove.cc')
while pos != -1:
    print("--- CONTEXT API.VIDLOVE.CC ---")
    print(text[max(0, pos - 150): min(len(text), pos + 500)])
    pos = text.find('api.vidlove.cc', pos + 1)
