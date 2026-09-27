import requests, re, hashlib, base64, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
url = "https://play.xpass.top/e/tv/106379/1/1"
headers = {"User-Agent": UA, "Referer": "https://play.xpass.top/"}

r = requests.get(url, headers=headers)
m_data_url = re.search(r'var dataUrl="([^"]+)"', r.text)
if m_data_url:
    data_url = m_data_url.group(1)
    data_path = data_url.split("?")[0]
    m_token = re.search(r'token=([^&]+)', data_url)
    token = m_token.group(1) if m_token else ""
    BUILD_ID = "spv3-build-1787821613-50e5fc97c9dce367"
    key = hashlib.sha256(f"spv3-data-response|{BUILD_ID}|{data_path}|{token}".encode()).digest()
    
    r_data = requests.get("https://play.xpass.top" + data_url, headers={"User-Agent": UA, "Referer": url, "Origin": "https://play.xpass.top"})
    b64_str = r_data.text.strip().replace("-", "+").replace("_", "/")
    b64_str += "=" * (-len(b64_str) % 4)
    raw = base64.b64decode(b64_str)
    dec = AESGCM(key).decrypt(raw[:12], raw[12:], None)
    servers = json.loads(dec.decode())
    print(f"Fallout S01E01 servers count: {len(servers)}")
    for s in servers[:5]:
        print(f"  {s['name']}: {s['url']}")
else:
    print("dataUrl not found for Fallout")
