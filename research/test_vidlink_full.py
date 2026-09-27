import requests
import json

headers = {
    "Referer": "https://vidlink.pro/",
    "Origin": "https://vidlink.pro",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Get fresh token
r = requests.get("https://enc-dec.app/api/enc-vidlink?text=550", timeout=10)
token = r.json()["result"]
print(f"Fresh token: {token}")

# Call movie API with ?token= query param
url = f"https://vidlink.pro/api/b/movie/550?token={token}"
r2 = requests.get(url, headers=headers, timeout=10)
print(f"Movie API status: {r2.status_code}")
print(f"Response: {r2.text[:500]}")

if r2.status_code == 200:
    data = r2.json()
    if data:
        print(f"\nKeys: {list(data.keys())}")
        if "stream" in data:
            stream = data["stream"]
            print(f"Stream keys: {list(stream.keys())}")
            if "qualities" in stream:
                for q, info in stream["qualities"].items():
                    print(f"  {q}: {info}")
            if "captions" in stream:
                print(f"  Captions: {len(stream['captions'])} available")
    else:
        print("Response was null")

# Also test TV API
print("\n=== TV API Test ===")
r3 = requests.get("https://enc-dec.app/api/enc-vidlink?text=1396", timeout=10)
tv_token = r3.json()["result"]
print(f"TV token: {tv_token}")

tv_url = f"https://vidlink.pro/api/b/tv/1396/1/1?token={tv_token}"
r4 = requests.get(tv_url, headers=headers, timeout=10)
print(f"TV API status: {r4.status_code}")
print(f"Response: {r4.text[:500]}")