import httpx
import re

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

pos = text.find('91446:')
if pos != -1:
    print("Found 91446:")
    print(text[pos: pos + 4000])
else:
    print("91446: not found directly, let's search for 91446")
    for m in re.finditer(r'91446', text):
        print("At", m.start(), text[m.start()-50:m.start()+100])
