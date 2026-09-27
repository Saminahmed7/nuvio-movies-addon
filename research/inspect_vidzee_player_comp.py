import requests
import re

url = "https://player.vidzee.wtf/assets/Ads-BJkRehrQ.js"
r = requests.get(url, timeout=10)
print(f"Downloaded Ads JS, len={len(r.text)}")

with open("research/vidzee_player_component.js", "w", encoding="utf-8") as f:
    f.write(r.text)

# Search for /_serverFn/ or /api/
for m in re.finditer(r'["\'](/[^"\']+)["\']', r.text):
    s = m.group(1)
    if any(k in s for k in ['_serverFn', 'api', 'server', 'stream', 'token', 'key', 'http']):
        print("Found route/URL:", s)

# Search for fetch calls
for m in re.finditer(r'fetch\([^)]+\)', r.text):
    print("Fetch:", m.group(0)[:100])
