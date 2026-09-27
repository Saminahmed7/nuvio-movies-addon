import requests
import json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
headers = {
    "User-Agent": UA,
    "Referer": "https://play.xpass.top/e/movie/550",
    "Origin": "https://play.xpass.top"
}

endpoints = [
    "/mdata/H1eUJmm4rwiA2Tqzk3V5J7/1/playlist.json",
    "/vip/fChBGNWV-SGR3Y4u9hvFXW6yooNlqCaE4d_SiyxuU4dR8I0kKsmZWOlQtcl2Ipp6lN5ong/1/playlist.json",
    "/mdata/MLU2BYxuabeEswWgaeT6Nw/0/playlist.json",
    "/vxr/movie/550/playlist.json",
    "/vrk/movie/550/playlist.json",
    "/mvid/H1eUJmm4rwiA2Tqzk3V5J7/1/playlist.json"
]

for ep in endpoints:
    url = "https://play.xpass.top" + ep
    r = requests.get(url, headers=headers)
    print(f"=== {ep} (Status: {r.status_code}) ===")
    if r.status_code == 200:
        print(r.text[:300])
