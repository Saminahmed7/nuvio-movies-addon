from curl_cffi import requests

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('de(l)')
if pos != -1:
    print(text[max(0, pos - 400): min(len(text), pos + 400)])
