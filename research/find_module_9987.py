import httpx
import re

for chunk in ['365-71c2a8238d040bc9.js', 'aaea2bcf-18613745c71632cf.js', '585-06626bce041c7708.js', '687-8e9f24493e814e00.js']:
    url = f'https://vidfast.vc/_next/static/chunks/{chunk}'
    text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    pos = text.find('9987:')
    if pos != -1:
        print(f"Found 9987 in {chunk} at {pos}!")
        print(text[pos: pos + 2500])
        break
else:
    print("9987: not found with colon, let's search for 9987")
