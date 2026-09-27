import re

with open('research/pow-worker-v3.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("len:", len(text))
print("\n=== First 3000 chars ===")
print(text[:3000])

print("\n=== Searching for SHA/hash patterns ===")
for m in re.finditer(r'.{0,50}(?:sha|hash|digest|module|wasm|solve|nonce|proof).{0,100}', text, re.I):
    print(m.group(0)[:150])
    print("---")
