from curl_cffi import requests
import re
import json

# Check the movie page again for watch links
r = requests.get('https://www.movy.sx/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text

# Find all links
links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', text)
watch_links = [l for l in links if 'watch' in l.lower() or 'play' in l.lower() or 'stream' in l.lower()]
print("Watch/Play/Stream links:")
for l in watch_links[:20]:
    print(f'  {l}')

# Also check for buttons or data attributes that might trigger watch
buttons = re.findall(r'<button[^>]*>.*?</button>', text, re.DOTALL)
for b in buttons[:10]:
    if 'watch' in b.lower() or 'play' in b.lower():
        print(f"\nButton: {b[:200]}")

# Check for data attributes
data_attrs = re.findall(r'data-[^=]+=["\'][^"\']*["\']', text)
for d in data_attrs[:20]:
    print(f"  {d}")