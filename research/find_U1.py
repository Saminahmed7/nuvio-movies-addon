from curl_cffi import requests
import re

url = 'https://atlantic.st/assets/index-BA2TuH7B.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('async function U1(')
if pos == -1:
    pos = text.find('function U1(')
if pos == -1:
    pos = text.find('U1=')
if pos == -1:
    pos = text.find('U1 =')

if pos != -1:
    print(text[pos: pos + 1000])
else:
    for m in re.finditer(r'U1\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', text):
        print(text[m.start(): m.start() + 600])
