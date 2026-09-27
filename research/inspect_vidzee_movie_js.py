import requests
import re

url = "https://player.vidzee.wtf/assets/embed.movie._tmdb-C_7qLwmt.js"
r = requests.get(url, timeout=10)
print(f"Downloaded embed JS, len={len(r.text)}")

with open("research/vidzee_movie_embed.js", "w", encoding="utf-8") as f:
    f.write(r.text)

# Look for server functions, fetch, post, get
for m in re.finditer(r'["\'](/_serverFn/[^"\']+)["\']', r.text):
    print("Found server function:", m.group(1))

# Print all strings with /api or /server or http
for m in re.finditer(r'https?://[^\s"\'`<>]+', r.text):
    print("Found URL:", m.group(0))

for m in re.finditer(r'["\'](/api[^"\']+)["\']', r.text):
    print("Found /api:", m.group(1))
