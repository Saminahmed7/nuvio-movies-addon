import requests
import re

url = "https://player.vidzee.wtf/assets/index-B97m00TC.js"
r = requests.get(url, timeout=10)
print(f"Downloaded JS, len={len(r.text)}")

with open("research/vidzee_bundle.js", "w", encoding="utf-8") as f:
    f.write(r.text)

# Search for api paths, fetch, axios, endpoints
matches = set(re.findall(r'["\'](/api/[^"\']+)["\']', r.text))
print("API endpoints found:", matches)

# Search for /server or /stream or routes
routes = set(re.findall(r'["\'](/[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+)["\']', r.text))
interesting_routes = [x for x in routes if any(k in x for k in ['api', 'movie', 'tv', 'watch', 'embed', 'player', 'stream', 'source'])]
print("Interesting routes:", interesting_routes[:20])

# Search for keys or AES
for word in ['AES', 'CBC', 'key', 'secret', 'token']:
    m = re.findall(rf'.{{0,30}}{word}.{{0,30}}', r.text)
    if m:
        print(f"Matches for {word} (first 3):", m[:3])
