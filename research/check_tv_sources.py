from curl_cffi import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

u1 = "https://api.vidlove.cc/tv?id=1396&season=1&episode=1&mode=json"
r1 = requests.get(u1, headers=headers, impersonate='chrome133a')
print("Without sources=vidapi:", r1.status_code, r1.json().get('source'))

u2 = "https://api.vidlove.cc/tv?id=1396&season=1&episode=1&mode=json&sources=vidapi"
r2 = requests.get(u2, headers=headers, impersonate='chrome133a')
print("With sources=vidapi:", r2.status_code, r2.json().get('source', {}).get('label'))
print("Manifest snippet:", r2.json().get('source', {}).get('manifest'))
