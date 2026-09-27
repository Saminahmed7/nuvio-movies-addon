import re

with open('research/vidzee_bundle.js', encoding='utf-8') as f:
    text = f.read()

paths = set(re.findall(r'path:\s*["\']([^"\']+)["\']', text))
print("Paths:", paths)

# Search for route definitions
route_matches = set(re.findall(r'["\'](/[^"\']+)["\']', text))
interesting = [p for p in route_matches if '/' in p and len(p) < 40 and not p.startswith('//') and not p.startswith('/assets')]
print("All / paths:", sorted(interesting)[:50])
