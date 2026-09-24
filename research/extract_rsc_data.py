import re
import json

with open('research/vidfast_27205.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all self.__next_f pushes
pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*)"\]\)', html)
print(f"Total Next.js server components chunks: {len(pushes)}")

for idx, p in enumerate(pushes):
    # Unescape JSON string
    try:
        unescaped = bytes(p, 'utf-8').decode('unicode_escape')
    except Exception:
        unescaped = p
    
    # Search for stream URLs, servers, sources, m3u8, mp4
    matches = re.findall(r'(https?://[^\s"\'\\<>]+|\b[a-zA-Z0-9_\-]+\.m3u8\b)', unescaped)
    if matches:
        print(f"Chunk {idx} matches:")
        for m in matches:
            if not any(k in m for k in ('nextjs', 'w3.org', 'google')):
                print("  ", m)
