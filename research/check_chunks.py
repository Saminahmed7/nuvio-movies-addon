import re
import httpx

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

chunks_to_check = [
    'static/chunks/1446-59080e42f9a250d9.js',
    'static/chunks/2427-f1dd7c2a4b7832e1.js',
    'static/chunks/7300-4265723c6b372545.js',
    'static/chunks/37a763b4-5a3b4f5484a24d2c.js',
    'static/chunks/a0f95e74-deee7f8b88cc1338.js',
    'static/chunks/823c5380-1dfb1d3849cbbdbc.js',
    'static/chunks/2751-11dbb3731c0eb357.js',
]

for chunk in chunks_to_check:
    url = f'https://www.rivestream.app/_next/{chunk}'
    try:
        r = httpx.get(url, headers=headers, timeout=10)
        print(f'{chunk}: {r.status_code} ({len(r.text)} bytes)')
        text = r.text
        # Look for keywords
        for m in re.finditer(r'(https?://[^\s"\'`<>]+)', text):
            u = m.group(1)
            if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'nextjs', 'github')):
                print(f'   URL in {chunk}: {u[:100]}')
        
        # Look for API routes
        for ep in re.findall(r'["\'`](/(?:api|api/v\d|backend|server|stream)[^"\'`\s]+)["\'`]', text):
            print(f'   API in {chunk}: {ep}')
    except Exception as e:
        print(f'{chunk}: error {e}')
