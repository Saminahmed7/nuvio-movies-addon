import requests
import json

# Step 1: Get token from enc-dec.app
print("=== Step 1: Get token from enc-dec.app ===")
token_url = "https://enc-dec.app/api/enc-vidlink?text=550"
r = requests.get(token_url, timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")

if r.status_code != 200:
    print("FAILED to get token")
    exit(1)

token_data = r.json()
token = token_data.get("result", "")
print(f"Token: {token}")

if not token:
    print("No token in response")
    exit(1)

# Step 2: Call vidlink.pro movie API
print("\n=== Step 2: Call vidlink.pro movie API ===")
movie_url = f"https://vidlink.pro/api/b/movie/550/{token}"
headers = {
    "Referer": "https://vidlink.pro/",
    "Origin": "https://vidlink.pro",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
r2 = requests.get(movie_url, headers=headers, timeout=10)
print(f"Status: {r2.status_code}")
print(f"Response: {r2.text[:500]}")

if r2.status_code == 200:
    data = r2.json()
    print(f"\nResponse keys: {list(data.keys())}")
    if "stream" in data:
        stream = data["stream"]
        print(f"Stream keys: {list(stream.keys())}")
        if "qualities" in stream:
            print(f"Qualities: {list(stream['qualities'].keys())}")
            for quality, info in stream["qualities"].items():
                print(f"  {quality}: {info}")
else:
    print(f"Failed with status {r2.status_code}")