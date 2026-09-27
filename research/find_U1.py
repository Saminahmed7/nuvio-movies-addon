import httpx
import re

# Check for U1 function in the bundle
with open('research/atlantic_bundle.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for U1 function
pos = text.find('U1=')
while pos != -1:
    end = min(len(text), pos + 500)
    print(text[pos:end])
    pos = text.find('U1=', pos + 1)
    if pos > 500000:
        break

# Also search for async function U1
pos = text.find('async function U1')
while pos != -1:
    end = min(len(text), pos + 500)
    print("\n--- async function U1 ---")
    print(text[pos:end])
    pos = text.find('async function U1', pos + 1)