import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

# Download main script chunk
r = requests.get('https://cinesrc.st/_next/static/chunks/bc59313b9106dcf9.js', headers=headers, timeout=10)
print('Script len:', len(r.text))

text = r.text

# Look for fetch/post to internal endpoints
fetches = re.findall(r'fetch\(["\']([^"\']+)["\']', text)
print("Fetches:", fetches[:20])

# Look for server action IDs (40 hex chars or POST to /)
action_ids = re.findall(r'["\']([0-9a-f]{40})["\']', text)
print("Action IDs found:", action_ids[:10])

# Look for pow or challenge
pow_refs = [(m.start(), m.group(0)) for m in re.finditer(r'.{0,50}(?:pow|challenge|sha|worker|nonce|seed).{0,50}', text, re.I)]
for pos, match in pow_refs[:10]:
    print("PoW ref:", match[:100])

# Look for URLs
urls = re.findall(r'https?://[^\s"\'<>]+', text)
interesting_urls = [u for u in set(urls) if not 'google' in u and not 'font' in u]
print("URLs:", interesting_urls[:20])
