import re

with open('research/cinesrc_main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Now find the pow-worker.js reference and stage 1 challenge logic
print("=== pow-worker context ===")
for m in re.finditer(r'.{0,200}pow.?worker.{0,400}', text, re.I):
    print(m.group(0)[:500])
    print("---")

print("\n=== d3, d4, d6 vars (the challenge script URIs) ===")
for m in re.finditer(r'(?:d3|d4|d6|d8)=["\']([^"\']+)["\']', text):
    print(m.group(0)[:100])

# Find the PoW solve function
print("\n=== gc() call context ===")
for m in re.finditer(r'.{0,50}\.gc\(\).{0,300}', text):
    print(m.group(0)[:300])
    print("---")

# Find challenge API responses
print("\n=== /api/c/issue context ===")
for m in re.finditer(r'.{0,100}/api/c/issue.{0,600}', text):
    print(m.group(0)[:600])
    print("---")
