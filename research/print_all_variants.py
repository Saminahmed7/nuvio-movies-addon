from curl_cffi import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

r = requests.get("https://api.vidlove.cc/movie?id=27205&mode=json&sources=vidapi", headers=headers, impersonate='chrome133a')
stream_url = r.json().get("source", {}).get("url")

m_resp = requests.get(stream_url, headers=headers, impersonate='chrome133a')
lines = m_resp.text.splitlines()

for i, line in enumerate(lines):
    if line.startswith("#EXT-X-STREAM-INF"):
        print(f"Variant: {line}")
        if i + 1 < len(lines):
            print(f"  URL: {lines[i+1][:70]}...")
