from curl_cffi import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import json

KEY_HEX = "7f3e9c2a8b5d1f4e6a9c3b7d2e5f8a1c4b6d9e2f5a8c1b4d7e9f2a5c8b1d4e7f"
key = bytes.fromhex(KEY_HEX)
aesgcm = AESGCM(key)

def decrypt_vidrock(enc_str: str) -> str:
    # base64url decode
    rem = len(enc_str) % 4
    if rem == 2: enc_str += "=="
    elif rem == 3: enc_str += "="
    raw = base64.urlsafe_b64decode(enc_str)
    if len(raw) < 28:
        raise ValueError("Ciphertext too short")
    iv = raw[:12]
    ciphertext_and_tag = raw[12:]
    dec = aesgcm.decrypt(iv, ciphertext_and_tag, None)
    return dec.decode("utf-8")

# Let's test on movie 27205 (Inception)
url = "https://vidrock.net/api/movie/27205"
r = requests.get(url, impersonate='chrome133a', headers={'Referer': 'https://vidrock.net/'})
print(f"Vidrock API response status: {r.status_code}")
data = r.json()
print("Vidrock servers:", list(data.keys()))

for name, sdata in data.items():
    if isinstance(sdata, dict) and 'url' in sdata:
        try:
            decrypted = decrypt_vidrock(sdata['url'])
            print(f"\nServer: {name} (type: {sdata.get('type')})")
            print(f"Decrypted URL: {decrypted}")
        except Exception as e:
            print(f"\nServer: {name} Decryption Failed: {e}")
