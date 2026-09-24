import base64
import json
import httpx
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_HEX = "d8f2a1b5e9c470814f6b2c3a5d8e7f901a2b3c4d5e3f7a8b9c0d1e2f3a4d5c6d"
KEY_BYTES = bytes.fromhex(KEY_HEX)

def b64_url_decode(s: str) -> bytes:
    s = s.replace('-', '+').replace('_', '/')
    padding = len(s) % 4
    if padding:
        s += '=' * (4 - padding)
    return base64.b64decode(s)

def decrypt_payload(enc_data: str) -> dict:
    parts = enc_data.split('.')
    if len(parts) != 3:
        raise ValueError(f"Expected 3 parts, got {len(parts)}")
    iv = b64_url_decode(parts[0])
    ciphertext = b64_url_decode(parts[1])
    tag = b64_url_decode(parts[2])
    
    aesgcm = AESGCM(KEY_BYTES)
    decrypted = aesgcm.decrypt(iv, ciphertext + tag, None)
    return json.loads(decrypted.decode('utf-8'))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://peachify.top/',
    'Origin': 'https://peachify.top'
}

for path in ['air', 'holly', 'multi', 'moviebox']:
    url = f"https://x.eat-peach.sbs/{path}/movie/27205"
    try:
        r = httpx.get(url, headers=headers, timeout=10)
        print(f"[{path}] HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if data.get('isEncrypted'):
                dec = decrypt_payload(data['data'])
                print(f"  DECRYPTED {path} successfully!")
                sources = dec.get('sources', [])
                print(f"  Sources count: {len(sources)}")
                for s in sources[:3]:
                    print("   -", s.get('quality'), s.get('resolution'), s.get('url')[:80] if s.get('url') else s)
            else:
                print(f"  Unencrypted response: {data}")
    except Exception as e:
        print(f"[{path}] Error: {e}")
