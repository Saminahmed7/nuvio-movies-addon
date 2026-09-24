from curl_cffi import requests
import re

url = 'http://1shows.bz/_next/static/chunks/4248-1ab7745edae28e83.js'
text = requests.get(url, impersonate='chrome133a').text
print("Length of 4248:", len(text))

# Search for /watch/ or /movie/
matches = re.findall(r'/(?:watch|movie|stream|embed|title)[a-zA-Z0-9_\-/]+', text)
print("Route patterns:", set(matches[:20]))

# Search for domains / APIs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = [u for u in set(urls) if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'github'))]
print("URLs in 4248:")
for u in clean:
    print(" ", u)
