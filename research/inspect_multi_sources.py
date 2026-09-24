import base64
import json
import httpx
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_BYTES = bytes.fromhex("d8f2a1b5e9c470814f6b2c3a5d8e7f901a2b3c4d5e3f7a8b9c0d1e2f3a4d5c6d")

def b64_url_decode(s: str) -> bytes:
    s = s.replace('-', '+').replace('_', '/')
    padding = len(s) % 4
    if padding:
        s += '=' * (4 - padding)
    return base64.b64decode(s)

def decrypt_payload(enc_data: str) -> dict:
    parts = enc_data.split('.')
    iv = b64_url_decode(parts[0])
    ciphertext = b64_url_decode(parts[1])
    tag = b64_url_decode(parts[2])
    aesgcm = AESGCM(KEY_BYTES)
    decrypted = aesgcm.decrypt(iv, ciphertext + tag, None)
    return json.loads(decrypted.decode('utf-8'))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://peachify.top/',
    'Origin': 'https://peachify.top'
}

r = httpx.get("https://x.eat-peach.sbs/multi/movie/27205", headers=headers, timeout=10)
data = r.json()
dec = decrypt_payload(data['data'])
print(json.dumps(dec, indent=2))
