from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('async function TQ(')
if pos == -1: pos = text.find('function TQ(')
if pos == -1: pos = text.find('TQ=')
if pos == -1: pos = text.find('TQ =')
if pos == -1: pos = text.find('const TQ')

if pos != -1:
    print(text[pos: pos + 1200])
else:
    for m in re.finditer(r'TQ\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', text):
        print(text[m.start(): m.start() + 600])
