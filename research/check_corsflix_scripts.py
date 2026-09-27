from curl_cffi import requests
import re

# Get the CorsFlix movie page and search for player data
r = requests.get('https://watch.corsflix.dpdns.org/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text

# Search for any JSON in script tags
scripts = re.findall(r'<script[^>]*>([^<]+)</script>', text)
for i, script in enumerate(scripts):
    if any(k in script.lower() for k in ['source', 'server', 'stream', 'player', 'm3u8', 'embed']):
        print(f"\nScript {i} (relevant):")
        print(script[:1000])

# Save for analysis
with open('research/corsflix_full.html', 'w', encoding='utf-8') as f:
    f.write(text)