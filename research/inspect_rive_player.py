import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
print('Length of 1446:', len(text))

# Search for m3u8-proxy
for m in re.finditer(r'proxy\.valhallastream\.com[^\s"\'\\<>]*', text):
    start = max(0, m.start() - 300)
    end = min(len(text), m.end() + 400)
    print("--- CONTEXT VALHALLASTREAM ---")
    print(text[start:end])

# Search for how sources are set
for m in re.finditer(r'(?:getSources|fetchSources|loadStream|setSource|currentSource|sources:)[^\s"\'\\<>]*', text):
    start = max(0, m.start() - 150)
    end = min(len(text), m.end() + 250)
    print("--- CONTEXT SOURCES ---")
    print(text[start:end])
    break
