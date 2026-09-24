from curl_cffi import requests
import re

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
text = requests.get(url, impersonate='chrome133a').text

# Search for hls.js config or custom loader
pos = text.find('whysosigmabro')
while pos != -1:
    print("--- CONTEXT whysosigmabro ---")
    print(text[max(0, pos - 150): min(len(text), pos + 300)])
    pos = text.find('whysosigmabro', pos + 1)
