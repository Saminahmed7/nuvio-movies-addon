from curl_cffi import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

r = requests.get("https://aether.ist/movie/27205", headers=headers, impersonate='chrome133a')
soup = BeautifulSoup(r.text, 'lxml')
for s in soup.find_all('script'):
    print(s.get('src') or s.string)
