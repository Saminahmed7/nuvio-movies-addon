from curl_cffi import requests
import re

# Get the CorsFlix movie page and search for player data
r = requests.get('https://watch.corsflix.dpdns.org/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text

# Look for any data- attributes or JavaScript variables
# Search for data- attributes
data_attrs = re.findall(r'data-[^=]+=["\'][^"\']*["\']', text)
for d in set(data_attrs):
    print(d)

# Search for any window. or self. assignments
window_vars = re.findall(r'window\.[a-zA-Z_][a-zA-Z0-9_]*\s*=', text)
print(f"\nwindow vars: {set(window_vars)}")

# Search for any JSON in script tags
scripts = re.findall(r'<script[^>]*>([^<]+)</script>', text)
for i, script in enumerate(scripts):
    if any(k in script.lower() for k in ['source', 'server', 'stream', 'player', 'm3u8', 'embed']):
        print(f"\nScript {i} (relevant):")
        print(script[:500])

# Search for any server/source text in page
for keyword in ['server', 'source', 'stream', 'player', 'choose', 'select']:
    matches = re.findall(rf'[^>]*{keyword}[^<]*', text, re.IGNORECASE)
    if matches:
        print(f"\n{keyword} mentions:")
        for m in set(matches)[:5]:
            print(f"  {m.strip()}")