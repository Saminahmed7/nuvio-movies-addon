import httpx
import re

url = 'https://vidfast.vc/_next/static/chunks/365-71c2a8238d040bc9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

matches = re.finditer(r'(?:[a-zA-Z0-9_]+\.en\b|\ben:|\{en:|\{en,|\(en\))', text)
for m in matches:
    start = max(0, m.start() - 150)
    end = min(len(text), m.end() + 250)
    print("--- CONTEXT .en ---")
    print(text[start:end])
