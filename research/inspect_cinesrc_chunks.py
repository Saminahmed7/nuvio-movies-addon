import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

# Download the main embed-specific JS chunks - looking for API logic
interesting_scripts = [
    '/_next/static/chunks/a6dad97d9634a72d.js',  # likely the embed page component
    '/_next/static/chunks/82833103ff1460c9.js',
    '/_next/static/chunks/693f69582a5d99f6.js',
    '/_next/static/chunks/7d3e9216f4741c06.js',
]

for script in interesting_scripts:
    url = 'https://cinesrc.st' + script
    r = requests.get(url, headers=headers, timeout=10)
    print(f"\n=== {script} (len={len(r.text)}) ===")
    text = r.text
    
    # Search for fetch / POST patterns
    for m in re.finditer(r'fetch\(["\`][^\)`"]+["\`]', text):
        print("FETCH:", m.group(0)[:100])
    
    # Search for server action IDs
    hex_ids = re.findall(r'["\']([0-9a-f]{40})["\']', text)
    if hex_ids:
        print("HEX IDs:", hex_ids[:5])
    
    # Look for API endpoints
    api_refs = re.findall(r'["\']/?(?:api|action|server|next|stream)[^"\']*["\']', text, re.I)
    if api_refs:
        print("API refs:", api_refs[:10])
    
    # Look for POST
    posts = re.findall(r'method:\s*["\']POST["\']', text, re.I)
    if posts:
        print("POST calls:", len(posts))
    
    # Look for "sha" or "pow" 
    pow_m = re.findall(r'.{20}sha.{20}|.{20}pow.{20}|.{20}nonce.{20}|.{20}worker.{20}', text, re.I)
    if pow_m:
        print("PoW refs:", pow_m[:3])
    
    # Print first 500 chars
    print("First 500:", text[:500])
