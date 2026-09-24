from curl_cffi import requests
import re

url = 'https://anyembed.xyz/assets/index-uplUFmH_.js'
text = requests.get(url, impersonate='chrome133a').text

matches = re.finditer(r'(?:fetchSources|getSources|scrapeStream|sourceUrl|providerList|streamProviders)', text)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 300)
    print("--- CONTEXT ---")
    print(text[start:end])
