from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

pos = text.find('async function dD(')
if pos == -1:
    pos = text.find('function dD(')
if pos == -1:
    pos = text.find('dD=')

if pos != -1:
    print("--- CONTEXT dD ---")
    print(text[pos: pos + 1200])
else:
    for m in re.finditer(r'dD\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', text):
        print("Regex dD:", text[m.start(): m.start() + 800])
