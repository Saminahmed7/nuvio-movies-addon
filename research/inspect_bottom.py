import httpx

url = 'https://www.rivestream.app/_next/static/chunks/1446-59080e42f9a250d9.js'
text = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
print(text[-2000:])
