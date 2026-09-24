from curl_cffi import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

r = requests.get("https://aether.ist/config.js", headers=headers, impersonate='chrome133a')
print("config.js:")
print(r.text)
