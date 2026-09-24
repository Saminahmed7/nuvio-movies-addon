from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

pos = text.find('eat-peach.sbs')
if pos != -1:
    print("--- CONTEXT EAT-PEACH ---")
    print(text[max(0, pos - 300): min(len(text), pos + 700)])
