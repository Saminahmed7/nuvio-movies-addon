from curl_cffi import requests

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('c=await de(l)')
if pos != -1:
    print(text[max(0, pos - 1200): pos + 200])
