import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://cinesrc.st/pow-worker-v3.js', headers=headers, timeout=10)

with open('research/pow-worker-v3.js', 'w', encoding='utf-8') as f:
    f.write(r.text)

text = r.text
print("len:", len(text))

# Look for the WASM loading
wasm_refs = re.findall(r'.{0,50}wasm.{0,100}', text, re.I)
print("\n=== WASM refs ===")
for m in wasm_refs[:10]:
    print(m[:100])

# Look for message event handler
msg_handler = re.findall(r'.{0,50}message.{0,200}', text, re.I)
print("\n=== message handler refs ===")
for m in msg_handler[:5]:
    print(m[:200])

# Print first 2000 chars
print("\n=== First 2000 ===")
print(text[:2000])
