import re

with open('research/movy_27205.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for embed, server, stream, player URLs
urls = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+', text)
clean = set()
for u in urls:
    if not any(k in u for k in ('w3.org', 'schema.org', 'google', 'twitter', 'react', 'tmdb.org')):
        clean.add(u)

print("Non-standard URLs in Movy:")
for u in sorted(clean):
    print(" ", u)

# Search for /api/ routes
apis = re.findall(r'["\'`](/(?:api|embed|player|stream|source)[^"\'`\s]+)["\'`]', text)
print("\nAPIs in Movy HTML:")
for a in set(apis):
    print(" ", a)
