import re

with open('research/pow-worker-v3.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for "ok" which is in the deobfuscated constant array
# and was present in A6aLoqc
# The worker likely uses WebAssembly (pow-v3.wasm)
# Let's look at what happens at the bottom/end of the file
print("=== Last 2000 chars ===")
print(text[-2000:])

# Look for WorkerGlobalScope, importScripts, addEventListener
print("\n=== Worker API refs ===")
for pattern in ['importScripts', 'addEventListener', 'WorkerGlobal', 'postMessage', 'onmessage']:
    idx = text.find(pattern)
    if idx != -1:
        print(f"{pattern} at {idx}:", text[max(0,idx-100):idx+200])
        print("---")
