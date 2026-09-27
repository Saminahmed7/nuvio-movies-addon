import base64
import json
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
STATIC_KEY = bytes.fromhex("a8f2a1b5e9c470814f6b2c3a5d8e7f9c1a2b3c4d5e3f7a8b8cad1e2d0a4d5c5b")

def b64url_decode(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * (-len(s) % 4)
    return base64.b64decode(s)

def peachify_decrypt(token: str) -> dict | None:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        iv = b64url_decode(parts[0])
        ciphertext = b64url_decode(parts[1])
        tag = b64url_decode(parts[2])
        aesgcm = AESGCM(STATIC_KEY)
        decrypted = aesgcm.decrypt(iv, ciphertext + tag, None)
        return json.loads(decrypted.decode("utf-8"))
    except Exception as e:
        print("Decrypt error:", e)
        return None

headers = {
    "User-Agent": UA,
    "Accept": "*/*",
    "Origin": "https://peachify.pro",
    "Referer": "https://peachify.pro/"
}

# Test Movie: Fight Club (550)
domains = ["https://peachify.pro", "https://peachify.top"]
servers = ["multi", "hr", "holly", "air", "moviebox"]

for base in domains:
    for s in servers:
        url = f"{base}/{s}/movie/550"
        try:
            r = requests.get(url, headers=headers, timeout=4)
            print(f"{url} -> status {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                enc_data = data.get("data")
                if enc_data:
                    dec = peachify_decrypt(enc_data)
                    print("  DECRYPTED SUCCESS:", dec)
                else:
                    print("  Plain data:", str(data)[:200])
        except Exception as e:
            print(f"{url} -> error: {e}")
