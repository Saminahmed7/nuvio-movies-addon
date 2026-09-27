import requests
import re
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# 1. Fetch Fight Club page
url = "https://play.xpass.top/e/movie/550"
headers = {
    "User-Agent": UA,
    "Referer": "https://play.xpass.top/"
}

r = requests.get(url, headers=headers)
html = r.text

m_data_url = re.search(r'var dataUrl="([^"]+)"', html)
if not m_data_url:
    print("dataUrl not found!")
    exit(1)

data_url = m_data_url.group(1)
print("Found dataUrl:", data_url)

# Extract data_path and token
data_path = data_url.split("?")[0]
m_token = re.search(r'token=([^&]+)', data_url)
token = m_token.group(1) if m_token else ""

print(f"data_path: {data_path}")
print(f"token: {token}")

# 2. Derive key:
BUILD_ID = "spv3-build-1787821613-50e5fc97c9dce367"
key_seed = f"spv3-data-response|{BUILD_ID}|{data_path}|{token}"
key = hashlib.sha256(key_seed.encode("utf-8")).digest()
print("Derived key (hex):", key.hex())

# 3. Fetch encrypted response
full_data_url = "https://play.xpass.top" + data_url
headers["Referer"] = url
headers["Origin"] = "https://play.xpass.top"

r_data = requests.get(full_data_url, headers=headers)
enc_text = r_data.text.strip()
print(f"Encrypted text length: {len(enc_text)}")

# Base64url decode
b64_str = enc_text.replace("-", "+").replace("_", "/")
b64_str += "=" * (-len(b64_str) % 4)
raw_bytes = base64.b64decode(b64_str)

iv = raw_bytes[:12]
ciphertext_and_tag = raw_bytes[12:]
ciphertext = ciphertext_and_tag[:-16]
tag = ciphertext_and_tag[-16:]

print(f"Raw bytes len: {len(raw_bytes)}, IV len: {len(iv)}, Ciphertext len: {len(ciphertext)}, Tag len: {len(tag)}")

aesgcm = AESGCM(key)
decrypted = aesgcm.decrypt(iv, ciphertext_and_tag, None)
print("DECRYPTED RESULT:")
print(decrypted.decode("utf-8"))
