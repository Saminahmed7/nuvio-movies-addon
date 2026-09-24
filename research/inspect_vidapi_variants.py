from curl_cffi import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

# Test on 27205 (Inception)
r = requests.get("https://api.vidlove.cc/movie?id=27205&mode=json&sources=vidapi", headers=headers, impersonate='chrome133a')
data = r.json()
stream_url = data.get("source", {}).get("url")
print("Stream URL:", stream_url)

m_resp = requests.get(stream_url, headers=headers, impersonate='chrome133a')
print("Master playlist first 1500 chars:")
print(m_resp.text[:1500])
