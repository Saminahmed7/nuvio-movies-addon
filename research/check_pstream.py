import httpx
from bs4 import BeautifulSoup

for u in ['https://docs.pstream.cfd/', 'https://pstream.cfd/']:
    try:
        r = httpx.get(u, headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True, timeout=10)
        print(f"=== {u} (HTTP {r.status_code}, {len(r.text)} bytes) ===")
        soup = BeautifulSoup(r.text, 'lxml')
        print("  Title:", soup.title.string if soup.title else None)
        text = soup.get_text('\n', strip=True)
        print("  Text snippet:\n", text[:500])
    except Exception as e:
        print(f"=== {u} ERROR: {e} ===")
