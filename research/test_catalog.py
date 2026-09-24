import asyncio
import sys
sys.path.insert(0, r'F:\nuvio-movies-addon')

from httpx import AsyncClient, ASGITransport
from main import app

async def test_catalog():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Test movies catalog
        print("Testing Movies Trending catalog...")
        r = await ac.get("/catalog/movie/movies_trending.json")
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Metas count: {len(data.get('metas', []))}")
        for m in data.get('metas', [])[:5]:
            print(f"  {m['name']} ({m.get('year', 'N/A')}) - ID: {m['id']}")
        
        # Test series catalog
        print("\nTesting Series Trending catalog...")
        r = await ac.get("/catalog/series/series_trending.json")
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Metas count: {len(data.get('metas', []))}")
        for m in data.get('metas', [])[:5]:
            print(f"  {m['name']} ({m.get('year', 'N/A')}) - ID: {m['id']}")

        # Test top rated movies
        print("\nTesting Movies Top Rated catalog...")
        r = await ac.get("/catalog/movie/movies_top_rated.json")
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Metas count: {len(data.get('metas', []))}")

        # Test top rated series
        print("\nTesting Series Top Rated catalog...")
        r = await ac.get("/catalog/series/series_top_rated.json")
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Metas count: {len(data.get('metas', []))}")

if __name__ == "__main__":
    asyncio.run(test_catalog())