from curl_cffi import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

r = requests.get("https://api.vidlove.cc/movie?id=27205&mode=json", headers=headers, impersonate='chrome133a')
source = r.json().get("source", {})
master_url = source.get("url")

mr = requests.get(master_url, headers=headers, impersonate='chrome133a')
print("Status:", mr.status_code)
print("Content-Type:", mr.headers.get("content-type"))
print("First 500 chars:\n", mr.text[:500])
