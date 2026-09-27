import base64
import json
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b"A7kP9xM2Qv8Lr4Nz1Ht6Yc3Bw5Jf0DsU"

def vidzee_decrypt(encrypted_str: str) -> str:
    try:
        # Step 1: Base64 decode the outer string
        raw_b64 = base64.b64decode(encrypted_str).decode("utf-8")
        parts = raw_b64.split(":")
        if len(parts) != 2:
            return f"Error: expected 2 parts, got {len(parts)}"
        iv = base64.b64decode(parts[0])
        ciphertext = base64.b64decode(parts[1])
        
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # PKCS7 unpadding
        pad_len = padded[-1]
        return padded[:-pad_len].decode("utf-8")
    except Exception as e:
        return f"Decrypt error: {e}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Referer": "https://player.vidzee.wtf/",
    "Origin": "https://player.vidzee.wtf",
    "Accept": "*/*"
}

# Test Movie: Fight Club (550) or Avatar 2 (76600)
for sr in range(1, 9):
    url = f"https://player.vidzee.wtf/api/server?id=550&sr={sr}"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"Server {sr}: status {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print("  Raw response keys:", list(data.keys()))
            for item in data.get("sources", data.get("data", [])) if isinstance(data, dict) else data:
                if isinstance(item, dict):
                    link = item.get("link") or item.get("url")
                    name = item.get("name")
                    print(f"  Item name: {name}, link: {link[:50] if link else None}")
                    if link:
                        dec = vidzee_decrypt(link)
                        print(f"    DECRYPTED: {dec}")
    except Exception as e:
        print(f"Server {sr} error: {e}")
