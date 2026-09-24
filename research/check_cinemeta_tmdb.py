import httpx
import json

r = httpx.get("https://v3-cinemeta.strem.io/meta/movie/tt0137523.json")
meta = r.json().get("meta", {})
print("Movie Cinemeta keys:", list(meta.keys()))
for k in ["moviedb_id", "tmdb_id", "id", "imdb_id"]:
    print(f"  {k}: {meta.get(k)}")

r2 = httpx.get("https://v3-cinemeta.strem.io/meta/series/tt0903747.json")
meta2 = r2.json().get("meta", {})
print("\nSeries Cinemeta keys:", list(meta2.keys()))
for k in ["moviedb_id", "tmdb_id", "id", "imdb_id"]:
    print(f"  {k}: {meta2.get(k)}")
