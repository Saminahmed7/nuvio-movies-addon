from curl_cffi import requests
import re
import json

# Get the full page and look for player/embed code
r = requests.get('https://www.movy.sx/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text

# Look for any JavaScript variables that might contain source info
# Search for window.__ or self.__ or data-
for pattern in [r'window\.__[^=]+=', r'self\.__[^=]+=', r'data-source', r'data-server', r'data-stream']:
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        print(f"Pattern {pattern}: {set(matches)}")

# Look for any JSON data in script tags
scripts = re.findall(r'<script[^>]*>([^<]+)</script>', text)
for i, script in enumerate(scripts):
    if 'source' in script.lower() or 'server' in script.lower() or 'stream' in script.lower():
        # Try to find JSON-like structures
        json_matches = re.findall(r'\{[^{}]*(?:source|server|stream|url|m3u8)[^{}]*\}', script)
        for jm in json_matches[:3]:
            print(f"Script {i} JSON-like: {jm[:200]}")

# Save full page for manual inspection
with open('research/movy_full.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved full page to research/movy_full.html")