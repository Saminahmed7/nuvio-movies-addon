import re

with open('research/pow-worker-v3.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for "solve", "gc", "onmessage", "postMessage"
print("=== Interesting function refs ===")
for m in re.finditer(r'.{0,100}(?:onmessage|postMessage|solve|gc\(|challenge|sha256|SHA256|crypto|digest).{0,200}', text, re.I):
    print(m.group(0)[:250])
    print("---")
