from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

pos = text.find('dF=')
if pos == -1:
    pos = text.find('dF =')
if pos == -1:
    pos = text.find('function dF(')
if pos == -1:
    pos = text.find('dF(')

if pos != -1:
    print("--- CONTEXT dF ---")
    print(text[max(0, pos - 100): min(len(text), pos + 1000)])
else:
    print("dF not found directly, let's search regex")
    m = re.search(r'dF\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>', text)
    if m:
        print(text[m.start(): m.start() + 1000])
