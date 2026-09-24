from curl_cffi import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/',
    'Origin': 'https://player.vidlove.cc'
}

sources = ["megaknight", "warden", "cinefreak", "moviebox2", "ipcloud", "tcloud", "vidapi"]

for src in sources:
    url = f"https://api.vidlove.cc/movie?id=27205&mode=json&sources={src}"
    try:
        r = requests.get(url, headers=headers, impersonate='chrome133a', timeout=10)
        if r.status_code == 200:
            data = r.json()
            source = data.get("source", {})
            print(f"=== [{src}] ===")
            print(json.dumps(source, indent=2)[:500])
    except Exception as e:
        print(f"[{src}] Error: {e}")
