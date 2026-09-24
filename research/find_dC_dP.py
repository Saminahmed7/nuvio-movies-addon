from curl_cffi import requests

url = 'https://peachify.top/_next/static/chunks/72f7ae58a2fa97e2.js'
text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10).text

pos = text.find('async function dD(')
if pos != -1:
    print("--- CONTEXT BEFORE dD ---")
    print(text[max(0, pos - 800): pos])
