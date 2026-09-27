from curl_cffi import requests
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://vidcore.io/",
    "X-Requested-With": "XMLHttpRequest"
}

try:
    r = requests.get("https://vidcore.io/movie/550/", headers=headers, impersonate="chrome120", timeout=8)
    print("vidcore status:", r.status_code, len(r.text))
    match = re.search(r'\"(?:en|token)\":\"(.*?)\"', r.text)
    if match:
        text = match.group(1)
        print("token text found, len:", len(text))
        enc = requests.get(f"https://enc-dec.app/api/enc-vidcore?text={text}").json()
        print("enc-vidcore:", enc)
        parts = enc.get("result")
        if parts:
            headers["X-CSRF-Token"] = parts["token"]
            srv_enc = requests.post(parts["servers"], headers=headers).text
            srv_dec = requests.post("https://enc-dec.app/api/dec-vidcore", json={"text": srv_enc}).json()
            print("servers:", srv_dec)
            for s in srv_dec.get("result", []):
                stream_url = f"{parts['stream']}/{s['data']}"
                st_enc = requests.post(stream_url, headers=headers).text
                st_dec = requests.post("https://enc-dec.app/api/dec-vidcore", json={"text": st_enc}).json()
                print("stream res for", s.get("name"), ":", st_dec)
    else:
        print("no token match. Page sample:", r.text[:400])
except Exception as e:
    print("error:", e)