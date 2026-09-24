import httpx
import json

base = "https://nuvio-movies-addon.vercel.app"

# Test 1: Fight Club (Movie)
r_movie = httpx.get(f"{base}/stream/movie/tt0137523.json", timeout=15)
print("=== Fight Club (Movie) ===")
print("Status:", r_movie.status_code)
movie_streams = r_movie.json().get("streams", [])
print(f"Streams found: {len(movie_streams)}")
for s in movie_streams:
    print(f"  Name: {s['name']}")
    print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
    print(f"  URL: {s['url'][:70]}...")
    print(f"  Size: {s.get('size')}")

# Test 2: Fallout S01E01 (Series)
r_series = httpx.get(f"{base}/stream/series/tt12637874:1:1.json", timeout=15)
print("\n=== Fallout S01E01 (Series) ===")
print("Status:", r_series.status_code)
series_streams = r_series.json().get("streams", [])
print(f"Streams found: {len(series_streams)}")
for s in series_streams:
    print(f"  Name: {s['name']}")
    print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
    print(f"  URL: {s['url'][:70]}...")
    print(f"  Size: {s.get('size')}")
