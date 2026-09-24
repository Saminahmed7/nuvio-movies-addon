from curl_cffi import requests
import re

url = 'https://anyembed.xyz/assets/index-uplUFmH_.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('function Ci(')
if pos == -1:
    pos = text.find('Ci=')
if pos == -1:
    pos = text.find('Ci =')

if pos != -1:
    print(text[pos: pos + 800])
