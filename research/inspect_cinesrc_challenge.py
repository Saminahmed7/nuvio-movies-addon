import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

r = requests.get('https://cinesrc.st/_next/static/chunks/7d3e9216f4741c06.js', headers=headers, timeout=15)
text = r.text

with open('research/cinesrc_main.js', 'w', encoding='utf-8') as f:
    f.write(text)

# Search around bootstrap/challenge-related endpoints
print("=== /api/c/bootstrap context ===")
for m in re.finditer(r'.{0,200}/api/c/bootstrap.{0,400}', text):
    print(m.group(0)[:500])
    print("---")

print("\n=== /api/c/stage2 context ===")
for m in re.finditer(r'.{0,200}/api/c/stage2.{0,400}', text):
    print(m.group(0)[:500])
    print("---")

print("\n=== /api/c/issue context ===")
for m in re.finditer(r'.{0,100}/api/c/issue.{0,400}', text):
    print(m.group(0)[:500])
    print("---")

print("\n=== SHA256 context ===")
for m in re.finditer(r'.{0,100}sha.?256.{0,300}', text, re.I):
    print(m.group(0)[:400])
    print("---")
