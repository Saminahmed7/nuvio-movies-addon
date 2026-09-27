import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

r = requests.get('https://cinesrc.st/embed/movie/550', headers=headers, timeout=10)
print('status:', r.status_code, 'len:', len(r.text))

with open('research/cinesrc_embed.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

# Find scripts preloaded
scripts = re.findall(r'href="(/_next/[^"]+\.js)"', r.text)
print("Preloaded scripts:", scripts[:10])

# Find _next inline data
m = re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', r.text, re.DOTALL)
if m:
    print("Next data:", m.group(1)[:500])

# Find server action IDs
m2 = re.findall(r'"([0-9a-f]{40})"', r.text)
print("Potential action IDs:", m2[:5])
