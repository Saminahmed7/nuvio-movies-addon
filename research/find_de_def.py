from curl_cffi import requests

url = 'https://player.vidlove.cc/assets/index-BzRddvSt.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('async function de(')
if pos == -1:
    pos = text.find('function de(')
if pos == -1:
    pos = text.find('de=')

if pos != -1:
    print(text[pos: pos + 500])
