from curl_cffi import requests
import re

url = 'https://vidrock.net/assets/index-C9cBdXG8.js'
text = requests.get(url, impersonate='chrome133a').text

matches = re.finditer(r'(?:fetch\(`\$\{qb\}|fetch\(`\$\{TF\}|fetch\([a-zA-Z0-9_]*qb|fetch\([a-zA-Z0-9_]*TF)', text)
for m in matches:
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 300)
    print("--- FETCH CALL ---")
    print(text[start:end])

# Also search for qb +
pos = text.find('`${qb}')
while pos != -1:
    print("--- QB TEMPLATE ---")
    print(text[max(0, pos - 50): min(len(text), pos + 300)])
    pos = text.find('`${qb}', pos + 1)
