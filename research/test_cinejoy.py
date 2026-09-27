import requests
import base64
from urllib.parse import quote

HEADERS = {
    "Accept": "*/*",
    "Origin": "https://cinejoy.pk",
    "Referer": "https://cinejoy.pk/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

API = "https://enc-dec.app/api"

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def base64url_decode(data):
    data += "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data)

title = "Fight Club"
type = "movie"
year = "1999"
imdb_id = "tt0137523"
tmdb_id = "550"

try:
    servers_res = requests.get("https://api.wing.st/servers", headers=HEADERS, timeout=5)
    servers = servers_res.json()["servers"]
    print("Available servers:", [s["name"] for s in servers])

    for s in servers:
        server_name = s["name"]
        print(f"\n--- Testing server: {server_name} ---")
        url = f"https://api.wing.st/?title={quote(title)}&type={type}&year={year}&imdb={imdb_id}&tmdb={tmdb_id}&server={server_name}"
        
        enc_cinejoy = f"{API}/enc-cinejoy?url={quote(url)}"
        resp = requests.get(enc_cinejoy, timeout=5).json()
        print("enc-cinejoy status:", resp.get("status"))
        if resp.get("status") != 200:
            print("enc-cinejoy error:", resp)
            continue
            
        enc = resp["result"]
        data = enc["data"]
        state = enc["state"]
        
        g_res = requests.post("https://api.wing.st/g", data=base64url_decode(data), headers=HEADERS, timeout=8)
        print("api.wing.st/g status:", g_res.status_code, "len:", len(g_res.content))
        
        if g_res.status_code == 200 and len(g_res.content) > 0:
            dec_resp = requests.post(f"{API}/dec-cinejoy", json={"text": base64url_encode(g_res.content), "state": state}, timeout=5).json()
            print("dec-cinejoy result:", dec_resp)
except Exception as e:
    print("Error:", e)
