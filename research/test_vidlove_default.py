from curl_cffi import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

r = requests.get("https://api.vidlove.cc/movie?id=27205&mode=json", headers=headers, impersonate='chrome133a')
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Keys:", list(data.keys()))
    print("Source:", data.get("source"))
