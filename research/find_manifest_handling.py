from curl_cffi import requests
import re

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('.manifest')
while pos != -1:
    print("--- CONTEXT .manifest ---")
    print(text[max(0, pos - 100): min(len(text), pos + 400)])
    pos = text.find('.manifest', pos + 1)
    if pos > 100000:
        break
