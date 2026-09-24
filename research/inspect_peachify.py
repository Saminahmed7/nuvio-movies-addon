from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://peachify.top/embed/movie/27205?autoPlay=true'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.rivestream.app/'
}

r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
soup = BeautifulSoup(r.text, 'lxml')
print("Peachify title:", soup.title.string if soup.title else None)

# Print inline scripts or interesting attributes
for s in soup.find_all('script'):
    if s.get('src'):
        print("Script src:", s.get('src'))
    elif s.string:
        print("Script text snippet:", s.string[:250])
