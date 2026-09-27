import requests

token = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzc1eq9nunT0FXXlcSD5_gMWGCP5NQFZzYI50"
headers = {
    "Referer": "https://vidlink.pro/",
    "Origin": "https://vidlink.pro",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Try different API paths
paths = [
    f"https://vidlink.pro/api/b/movie/550/{token}",
    f"https://vidlink.pro/api/b/movie/550?token={token}",
    f"https://vidlink.pro/api/movie/550/{token}",
    f"https://vidlink.pro/api/movie/550?token={token}",
    f"https://vidlink.pro/api/b/movie/{token}/550",
    f"https://vidlink.pro/api/v1/movie/550/{token}",
    f"https://vidlink.pro/api/v2/movie/550/{token}",
]

for url in paths:
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"{r.status_code} - {url}")
        if r.status_code == 200:
            print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"ERROR - {url}: {e}")