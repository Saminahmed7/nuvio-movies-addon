import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# Download pow-v3.wasm
r = requests.get('https://cinesrc.st/pow-v3.wasm', headers=headers, timeout=10)
print('WASM status:', r.status_code, 'len:', len(r.content))

with open('research/pow-v3.wasm', 'wb') as f:
    f.write(r.content)

# Parse WASM module to find exported functions
magic = r.content[:4]
print('Magic:', magic.hex())  # Should be 00 61 73 6d for WASM

# Look for function name strings
text_bytes = r.content
strings = re.findall(b'[\x20-\x7e]{4,}', text_bytes)
print("\nReadable strings in WASM:")
for s in strings[:50]:
    print(" ", s.decode('ascii', errors='ignore'))
