import requests

# Get full videasy.js
url = 'https://raw.githubusercontent.com/phisher98/nuvio-providers/main/providers/videasy.js'
r = requests.get(url, timeout=15)
content = r.text
with open('research/videasy_full.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved to research/videasy_full.js")
print(f"Total length: {len(content)}")