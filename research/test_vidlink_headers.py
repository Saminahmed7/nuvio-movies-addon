import requests

# Get fresh token
r = requests.get("https://enc-dec.app/api/enc-vidlink?text=550", timeout=10)
token = r.json()["result"]
print(f"Token: {token}")

# Try with different header combinations
header_sets = [
    {
        "Referer": "https://vidlink.pro/",
        "Origin": "https://vidlink.pro",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    },
    {
        "Referer": "https://vidlink.pro/",
        "Origin": "https://vidlink.pro",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/144.0.7559.132 Safari/537.36",
        "Referer": "https://vidlink.pro/",
        "Origin": "https://vidlink.pro",
    },
]

for i, headers in enumerate(header_sets):
    url = f"https://vidlink.pro/api/b/movie/550?token={token}"
    r2 = requests.get(url, headers=headers, timeout=10)
    print(f"\nHeader set {i+1}:")
    print(f"  Status: {r2.status_code}")
    print(f"  Response headers: {dict(r2.headers)}")
    print(f"  Response body: {r2.text[:300]}")
    if r2.status_code == 200 and r2.json():
        data = r2.json()
        if data and "stream" in data:
            print(f"  >>> FOUND STREAM! <<<")
            break

# Also try the path format with fresh token
print("\n=== Path format ===")
url2 = f"https://vidlink.pro/api/b/movie/550/{token}"
r3 = requests.get(url2, headers=header_sets[0], timeout=10)
print(f"Status: {r3.status_code}")
print(f"Response: {r3.text[:300]}")