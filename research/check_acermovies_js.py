from curl_cffi import requests
import re

r = requests.get('https://acermovies.fun/watch/27205', impersonate='chrome133a', timeout=10)
text = r.text

for pattern in ['fetch', 'axios', 'api2', 'acermovies', 'sourceUrl', 'getSource', 'source', 'stream', 'm3u8', 'playlist']:
    matches = re.findall(rf'[^>\s]*{pattern}[^<\s]*', text, re.IGNORECASE)
    unique_matches = set(matches)
    if unique_matches:
        print(f'{pattern}: {list(unique_matches)[:10]}')

with open('research/acermovies_watch.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved to research/acermovies_watch.html")