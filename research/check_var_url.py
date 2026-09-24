from curl_cffi import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

r = requests.get("https://api.vidlove.cc/movie?id=27205&mode=json", headers=headers, impersonate='chrome133a')
source = r.json().get("source", {})
manifest = source.get("manifest", "")

lines = manifest.splitlines()
for i, line in enumerate(lines):
    if "1920x" in line:
        var_url = lines[i+1]
        print(f"Variant 1080p URL: {var_url}")
        vr = requests.get(var_url, headers=headers, impersonate='chrome133a')
        print(f"Status: {vr.status_code}")
        print(f"Content-type: {vr.headers.get('content-type')}")
        print(f"Text snippet:\n{vr.text[:400]}")
        break
