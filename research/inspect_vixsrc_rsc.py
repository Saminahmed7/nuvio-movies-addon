import re
import json

with open('research/vixsrc_27205.html', 'r', encoding='utf-8') as f:
    text = f.read()

pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*)"\]\)', text)
full = "".join(pushes)
try:
    unescaped = bytes(full, 'utf-8').decode('unicode_escape')
except Exception:
    unescaped = full

print("Vixsrc RSC length:", len(unescaped))
# Search for JSON objects or props
for m in re.finditer(r'\{[^{}]*"(?:stream|url|source|token|hls|m3u8|id)"[^{}]*\}', unescaped):
    print("Found JSON prop:", m.group(0))

urls = re.findall(r'https?://[^\s"\'\\<>]+', unescaped)
print("\nURLs in Vixsrc RSC:")
for u in set(urls):
    print(" ", u)
