import httpx
from bs4 import BeautifulSoup

for p in ['/backend/introduction', '/proxy/introduction']:
    url = f'https://docs.pstream.cfd{p}'
    r = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.get_text('\n', strip=True)
    print(f"=== {p} ===")
    print(text[:1500])
