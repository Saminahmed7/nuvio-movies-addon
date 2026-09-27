from curl_cffi import requests
import re
import json

# Try Rive mirrors
mirrors = [
    'https://rivestream.ru',
    'https://rivestream.pw',
    'https://corsflix.net',
    'https://watch.corsflix.dpdns.org',
]

for base in mirrors:
    print(f"\n{'='*60}")
    print(f"Testing {base}")
    print(f"{'='*60}")
    
    # Try homepage
    r = requests.get(base, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }, impersonate='chrome133a', timeout=10)
    print(f"Homepage: {r.status_code} - {r.url}")
    
    if r.status_code == 200:
        text = r.text
        # Check for movie page
        r2 = requests.get(f'{base}/movie/27205', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, impersonate='chrome133a', timeout=10)
        print(f"  Movie page: {r2.status_code} - {r2.url}")
        
        if r2.status_code == 200:
            # Check for NEXT_DATA
            next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', r2.text)
            if next_data:
                data = json.loads(next_data[0])
                page_props = data.get("props", {}).get("pageProps", {})
                print(f"  pageProps keys: {list(page_props.keys())}")
                
            # Check iframes
            iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', r2.text)
            print(f"  iframes: {iframes[:5]}")
            
            # Check for watch links
            watch_links = re.findall(r'href=["\']([^"\']*(?:watch|play|embed)[^"\']*)["\']', r2.text)
            print(f"  watch/play/embed links: {watch_links[:5]}")
            
            break