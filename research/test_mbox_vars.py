import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
import json
import base64
import hashlib
import hmac
import urllib.parse
import requests

KEY_A = base64.b64decode("NzZpUmwwN3MweFNOOWpxbUVXQXQ3OUVCSlp1bElRSXNWNjRGWnIyTw==")
KEY_B = base64.b64decode("WHFuMm5uTzQxL0w5Mm8xaXVYaFNMSFRiWHZZNFo1Wlo2Mm04bVNMQQ==")

USER_AGENT = "com.community.mbox.in/50020130 (Linux; U; Android 14; en_IN; Pixel 8; Build/UD1A.230803.041; Cronet/145.0.7582.0)"

CLIENT_INFO = json.dumps({
    "package_name": "com.community.mbox.in",
    "version_name": "4.0.03.0920.03",
    "version_code": 50020130,
    "os": "android",
    "os_version": "14",
    "device_id": "8a7c6b5d4e3f2a1b",
    "install_store": "official",
    "gaid": "1b2212c1-dadf-43c3-a0c8-bd6ce48ae22d",
    "brand": "Google",
    "model": "Pixel 8",
    "system_language": "en",
    "net": "NETWORK_WIFI",
    "region": "IN",
    "timezone": "Asia/Calcutta",
    "sp_code": ""
}, separators=(',', ':'))

def md5_hex(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

def generate_x_client_token(ts: int) -> str:
    ts_str = str(ts)
    reversed_ts = ts_str[::-1]
    md5_reversed = md5_hex(reversed_ts.encode('utf-8'))
    return f"{ts_str},{md5_reversed}"

def generate_signature(canonical: str, key: bytes) -> str:
    h = hmac.new(key, canonical.encode('utf-8'), hashlib.md5)
    sig_b64 = base64.b64encode(h.digest()).decode('utf-8').replace('\n', '').replace('\r', '')
    return f"|2|{sig_b64}"

# Test variations of canonical string
urls = [
    "https://api3.aoneroom.com/wefeed-mobile-bff/tab/ranking-list?tabId=0&categoryType=4516404531735022304&page=1&perPage=1",
    "https://apig.inmoviebox.com/wefeed-mobile-bff/tab/ranking-list?tabId=0&categoryType=4516404531735022304&page=1&perPage=1"
]

ts = int(time.time() * 1000)
token = generate_x_client_token(ts)

# Let's try different combinations of canonical string lines
parsed = urllib.parse.urlparse(urls[0])
path = parsed.path
sorted_q = "categoryType=4516404531735022304&page=1&perPage=1&tabId=0"
canon_path = f"{path}?{sorted_q}"

variations = [
    # Var 1: GET, application/json, body_md5, path, token, ts
    ["GET", "application/json", "", canon_path, token, str(ts)],
    # Var 2: GET, application/json, token, body_len, ts, body_md5, path
    ["GET", "application/json", token, "", str(ts), "", canon_path],
    # Var 3: GET, application/json, "", token, str(ts), "", canon_path
    ["GET", "application/json", "", token, str(ts), "", canon_path],
    # Var 4: GET, "", "", canon_path, token, str(ts)
    ["GET", "", "", canon_path, token, str(ts)],
    # Var 5: url with host
    ["GET", "application/json", token, "", str(ts), "", urls[0]],
]

for var_idx, var_lines in enumerate(variations):
    canon = '\n'.join(var_lines)
    for key_name, key in [("KEY_B", KEY_B), ("KEY_A", KEY_A)]:
        sig = generate_signature(canon, key)
        headers = {
            "user-agent": USER_AGENT,
            "accept": "application/json",
            "content-type": "application/json",
            "connection": "keep-alive",
            "x-client-token": token,
            "x-tr-signature": sig,
            "x-client-info": CLIENT_INFO,
            "x-client-status": "0"
        }
        for u in urls[:1]:
            r = requests.get(u, headers=headers, timeout=5)
            if r.status_code == 200:
                print(f"\n>>> SUCCESS with Var {var_idx} and {key_name} on {u}! <<<")
                print("x-user header:", r.headers.get("x-user"))
                print("Response:", r.text[:200])
                sys.exit(0)
            else:
                pass
print("Finished testing basic variations.")
