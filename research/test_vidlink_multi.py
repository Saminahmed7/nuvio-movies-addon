import requests

headers = {
    "Referer": "https://vidlink.pro/",
    "Origin": "https://vidlink.pro",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

# Test with multiple TMDB IDs
tmdb_ids = [
    ("550", "Fight Club"),
    ("27205", "Inception"),
    ("1396", "Breaking Bad S1E1"),
    ("1399", "Game of Thrones S1E1"),
    ("66732", "Stranger Things S1E1"),
    ("76479", "The Boys S1E1"),
    ("106379", "Fallout S1E1"),
]

for tmdb_id, name in tmdb_ids:
    # Get fresh token
    r = requests.get(f"https://enc-dec.app/api/enc-vidlink?text={tmdb_id}", timeout=10)
    if r.status_code != 200:
        print(f"{name}: Token failed - {r.status_code}")
        continue
    token = r.json().get("result", "")
    if not token:
        print(f"{name}: No token")
        continue

    # Try movie API
    url = f"https://vidlink.pro/api/b/movie/{tmdb_id}?token={token}"
    r2 = requests.get(url, headers=headers, timeout=10)
    if r2.status_code == 200:
        data = r2.json()
        if data and "stream" in data:
            stream = data["stream"]
            qualities = stream.get("qualities", {})
            print(f"{name} (tmdb:{tmdb_id}): {list(qualities.keys())}")
        else:
            print(f"{name} (tmdb:{tmdb_id}): null response")
    else:
        print(f"{name} (tmdb:{tmdb_id}): HTTP {r2.status_code}")

    # Try TV API for series
    if tmdb_id in ["1396", "1399", "66732", "76479", "106379"]:
        r3 = requests.get(f"https://enc-dec.app/api/enc-vidlink?text={tmdb_id}", timeout=10)
        tv_token = r3.json().get("result", "")
        tv_url = f"https://vidlink.pro/api/b/tv/{tmdb_id}/1/1?token={tv_token}"
        r4 = requests.get(tv_url, headers=headers, timeout=10)
        if r4.status_code == 200:
            data = r4.json()
            if data and "stream" in data:
                stream = data["stream"]
                qualities = stream.get("qualities", {})
                print(f"  TV: {list(qualities.keys())}")
            else:
                print(f"  TV: null response")
        else:
            print(f"  TV: HTTP {r4.status_code}")