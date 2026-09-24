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
        print(f"[{src}] HTTP {r.status_code:3} ({len(r.text)} bytes)")
        if r.status_code == 200:
            try:
                data = r.json()
                print("  Data keys:", list(data.keys()) if isinstance(data, dict) else type(data))
                print("  Snippet:", str(data)[:300])
            except Exception:
                print("  Non-JSON text:", r.text[:200])
    except Exception as e:
        print(f"[{src}] Error: {e}")
