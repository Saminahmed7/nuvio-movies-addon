from curl_cffi import requests
import re
import json

# Check the actual movie page
r = requests.get('https://www.movy.sx/movie/27205', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}, impersonate='chrome133a', timeout=10)

text = r.text

# Extract NEXT_DATA
next_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', text)
if next_data:
    data = json.loads(next_data[0])
    page_props = data.get("props", {}).get("pageProps", {})
    details = page_props.get("details", {})
    print(f"details keys: {list(details.keys()) if isinstance(details, dict) else type(details)}")
    if isinstance(details, dict):
        for k, v in details.items():
            if k in ['sources', 'servers', 'streams', 'videos', 'watch', 'providers']:
                print(f"\n  {k}: {type(v)}")
                if isinstance(v, list):
                    for item in v[:3]:
                        print(f"    {item}")
                elif isinstance(v, dict):
                    print(f"    {v}")
        
        # Print full details structure
        print(f"\nFull details:")
        print(json.dumps(details, indent=2)[:3000])