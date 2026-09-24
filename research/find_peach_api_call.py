from curl_cffi import requests
import re

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

pos = text.find('moviebox')
if pos != -1:
    print("--- CONTEXT MOVIEBOX ---")
    print(text[pos: pos + 2500])
