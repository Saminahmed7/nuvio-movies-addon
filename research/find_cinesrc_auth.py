import re

with open('research/cinesrc_main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the full challenge/bootstrap section - look for c_b, x-cs-q, x-cs-r, x-cs-p
print("=== x-cs-q header context (wider) ===")
idx = text.find('x-cs-q')
if idx != -1:
    print(text[max(0, idx-1000):idx+2000])
