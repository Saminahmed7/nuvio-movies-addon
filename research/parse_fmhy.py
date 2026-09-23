import sys
import io
import re
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('research/fmhy_video.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
sites = []

for line in lines:
    line_clean = line.strip()
    if not line_clean.startswith('*'):
        continue
    
    star = 'None'
    if '🌟' in line_clean:
        star = 'Gold'
    elif '⭐' in line_clean:
        star = 'Silver'

    m = re.search(r'\[([^\]]+)\]\((https?://[^\)]+)\)', line_clean)
    if not m:
        continue
    title = m.group(1).strip()
    url = m.group(2).strip()

    if title.lower() in ('status', 'discord', 'telegram', 'github', 'docs', 'source code', 'guide', '2', '3', '4', '5'):
        continue

    is_4k = bool(re.search(r'\b4k\b|\b2160p?\b', line_clean, re.I))
    is_1080p = bool(re.search(r'\b1080p?\b', line_clean, re.I)) or is_4k
    
    is_streaming = any(k in line_clean.lower() for k in ('movie', 'tv', 'anime', 'stream'))

    if is_streaming and (is_1080p or is_4k):
        mirrors = [m.group(2) for m in re.finditer(r'\[(\d+)\]\((https?://[^\)]+)\)', line_clean)]
        
        score = 0
        if star == 'Gold':
            score += 100
        elif star == 'Silver':
            score += 50
        if is_4k:
            score += 20
        if is_1080p:
            score += 5

        sites.append({
            'title': title,
            'url': url,
            'mirrors': mirrors,
            'star': star,
            'is_4k': is_4k,
            'is_1080p': is_1080p,
            'score': score,
            'raw': line_clean
        })

# Deduplicate by url domain
seen = set()
unique_sites = []
for s in sorted(sites, key=lambda x: x['score'], reverse=True):
    from urllib.parse import urlparse
    domain = urlparse(s['url']).netloc.lower()
    if domain not in seen:
        seen.add(domain)
        unique_sites.append(s)

with open('research/ranked_sites.json', 'w', encoding='utf-8') as f:
    json.dump(unique_sites, f, indent=2, ensure_ascii=False)

print(f"Total unique streaming sites (>=1080p): {len(unique_sites)}")
print("\n--- TOP RANKED 4K SITES ---")
k4_count = 0
for idx, s in enumerate(unique_sites, 1):
    if s['is_4k']:
        k4_count += 1
        print(f"#{k4_count} [Score: {s['score']} | {s['star']}] {s['title']} -> {s['url']}")
        if s['mirrors']:
            print(f"   Mirrors: {', '.join(s['mirrors'][:2])}")
