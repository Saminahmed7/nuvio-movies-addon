from curl_cffi import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://vidfast.vc/",
    "X-Requested-With": "XMLHttpRequest"
}

API = "https://enc-dec.app/api"

try:
    url = "https://vidfast.vc/movie/550/"
    # Try with curl_cffi
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, impersonate="chrome120", timeout=8)
    print("Page status:", r.status_code, "len:", len(r.text))
    # Look for token/en in page
    for pattern in [r'\"(?:en|token)\":\"(.*?)\"', r'(?:en|token)[\'\"]?\s*:\s*[\'\"]([^\'\"]+)[\'\"]']:
        m = re.search(pattern, r.text)
        if m:
            print("Found pattern:", pattern, "len:", len(m.group(1)))
            text = m.group(1)
            enc_res = requests.get(f"{API}/enc-vidfast?text={text}").json()
            print("enc-vidfast:", enc_res)
            parts = enc_res.get("result", {})
            if parts:
                token = parts["token"]
                servers_url = parts["servers"]
                stream_base = parts["stream"]
                s_headers = dict(HEADERS)
                s_headers["X-CSRF-Token"] = token
                servers_enc = requests.post(servers_url, headers=s_headers).text
                dec_srv = requests.post(f"{API}/dec-vidfast", json={"text": servers_enc}).json()
                print("Servers:", dec_srv)
                for srv in dec_srv.get("result", [])[:3]:
                    st_url = f"{stream_base}/{srv['data']}"
                    st_enc = requests.post(st_url, headers=s_headers).text
                    st_dec = requests.post(f"{API}/dec-vidfast", json={"text": st_enc}).json()
                    print(f"Stream [{srv.get('name')}]:", st_dec)
            break
    else:
        print("No token pattern matched in page. First 500 chars:", r.text[:500])
except Exception as e:
    print("Error:", e)
