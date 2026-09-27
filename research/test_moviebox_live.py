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

def build_canonical_string(url_str: str, method: str, content_type: str = "", body: str = "", client_token: str = "", ts: int = 0) -> str:
    parsed = urllib.parse.urlparse(url_str)
    path = parsed.path or "/"
    query = parsed.query
    
    if query:
        pairs = query.split('&')
        parsed_pairs = []
        for p in pairs:
            if '=' in p:
                k, v = p.split('=', 1)
            else:
                k, v = p, ''
            parsed_pairs.append((k, v))
        # Sort by key
        parsed_pairs.sort(key=lambda x: x[0])
        sorted_query = '&'.join(f"{k}={v}" for k, v in parsed_pairs)
        canonical_path = f"{path}?{sorted_query}"
    else:
        canonical_path = path

    # Body calculations
    if body:
        body_bytes = body.encode('utf-8')
        body_len_str = str(len(body_bytes))
        body_md5 = md5_hex(body_bytes[:102400])
    else:
        body_len_str = ""
        body_md5 = ""

    # The exact 7 parts:
    # 1. method.toUpperCase()
    # 2. contentType (or "")
    # 3. clientToken (or "")
    # 4. body_len_str (or "")
    # 5. timestamp (Long)
    # 6. body_md5 (or "")
    # 7. canonical_path (path with sorted query)
    lines = [
        method.upper(),
        content_type or "",
        client_token or "",
        body_len_str,
        str(ts),
        body_md5,
        canonical_path
    ]
    return '\n'.join(lines)

def generate_signature(canonical: str, key: bytes) -> str:
    h = hmac.new(key, canonical.encode('utf-8'), hashlib.md5)
    sig_b64 = base64.b64encode(h.digest()).decode('utf-8').replace('\n', '').replace('\r', '')
    return f"|2|{sig_b64}"

# Test!
url = "https://api3.aoneroom.com/wefeed-mobile-bff/tab/ranking-list?tabId=0&categoryType=4516404531735022304&page=1&perPage=1"
ts = int(time.time() * 1000)
token = generate_x_client_token(ts)

for key_name, key in [("KEY_B (default)", KEY_B), ("KEY_A", KEY_A)]:
    canonical = build_canonical_string(url, "GET", "application/json", "", token, ts)
    print(f"\n--- Testing with {key_name} ---")
    print("Canonical string:\n", repr(canonical))
    sig = generate_signature(canonical, key)
    print("Signature:", sig)
    
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
    
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        print("Response headers:", dict(r.headers))
        print("Response text:", r.text[:300])
        if "x-user" in r.headers:
            print("\n>>> SUCCESS! FOUND x-user HEADER! <<<")
            user_data = json.loads(r.headers["x-user"])
            print("User data:", user_data)
            break
    except Exception as e:
        print("Error:", e)
