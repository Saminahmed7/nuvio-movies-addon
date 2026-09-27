from curl_cffi import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://vidup.to/",
    "X-Requested-With": "XMLHttpRequest"
}

API = "https://enc-dec.app/api"

try:
    url = "https://vidup.to/movie/550/"
    r = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=8)
    print("Page status:", r.status_code)
    # search for token in page
    match = re.search(r'\"(?:en|token)\":\"(.*?)\"', r.text)
    if not match:
        # try without escaping
        match = re.search(r'(?:en|token)[\'\"]?\s*:\s*[\'\"]([^\'\"]+)[\'\"]', r.text)
    
    if match:
        text = match.group(1)
        print("Found text len:", len(text))
        enc_res = requests.get(f"{API}/enc-vidup?text={text}").json()
        print("enc-vidup:", enc_res)
        parts = enc_res.get("result", {})
        if parts:
            token = parts["token"]
            servers_url = parts["servers"]
            stream_base = parts["stream"]
            
            s_headers = dict(HEADERS)
            s_headers["X-CSRF-Token"] = token
            
            servers_enc = requests.post(servers_url, headers=s_headers).text
            dec_srv = requests.post(f"{API}/dec-vidup", json={"text": servers_enc}).json()
            print("Servers:", dec_srv)
            
            servers_list = dec_srv.get("result", [])
            for srv in servers_list[:3]:
                st_url = f"{stream_base}/{srv['data']}"
                st_enc = requests.post(st_url, headers=s_headers).text
                st_dec = requests.post(f"{API}/dec-vidup", json={"text": st_enc}).json()
                print(f"Stream [{srv.get('name')}]:", st_dec)
    else:
        print("No token found in page")
except Exception as e:
    print("Error:", e)
