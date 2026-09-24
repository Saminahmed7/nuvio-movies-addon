from curl_cffi import requests
from bs4 import BeautifulSoup
import re

for name, u in [('Atlantic', 'https://atlantic.st/'), ('Aether', 'https://aether.ist/')]:
    r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, impersonate='chrome133a', timeout=10)
    soup = BeautifulSoup(r.text, 'lxml')
    print(f"=== {name} ({u}) ===")
    scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
    print("  Scripts:", scripts[:5])
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    print("  Sample links:", [l for l in links if any(k in l for k in ('watch', 'movie', 'tv'))][:5])
    # Search for Turnstile or CF
    if any('turnstile' in (s.get('src') or '') for s in soup.find_all('script')):
        print("  WARNING: Has Turnstile!")
    else:
        print("  Clean: No Turnstile in HTML.")
