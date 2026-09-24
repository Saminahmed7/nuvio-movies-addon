from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
text = requests.get(url, impersonate='chrome133a').text

for m in re.finditer(r'\bbQ\b', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 150)
    print(text[start:end])
    print("-" * 50)
