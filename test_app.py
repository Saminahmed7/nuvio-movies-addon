import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

async def test_addon():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Test 1: Health
        r = await ac.get("/health")
        print("Health:", r.status_code, r.json())

        # Test 2: Diag
        r = await ac.get("/diag")
        print("Diag:", r.status_code, r.json())

        # Test 3: Movie stream (Fight Club - tt0137523)
        print("\nQuerying movie stream tt0137523 (Fight Club)...")
        r = await ac.get("/stream/movie/tt0137523.json")
        print("Status:", r.status_code)
        streams = r.json().get("streams", [])
        print(f"Streams found: {len(streams)}")
        for s in streams:
            print(f"  [{s['name']}]")
            print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
            print(f"  URL: {s['url'][:70]}...")
            print(f"  Size: {s.get('size')} bytes")
            print(f"  Subtitles count: {len(s.get('subtitles', []))}")

        # Test 4: TV series stream (Fallout S01E01 - tt12637874:1:1)
        print("\nQuerying TV series stream tt12637874:1:1 (Fallout)...")
        r = await ac.get("/stream/series/tt12637874:1:1.json")
        print("Status:", r.status_code)
        tv_streams = r.json().get("streams", [])
        print(f"TV Streams found: {len(tv_streams)}")
        for s in tv_streams:
            print(f"  [{s['name']}]")
            print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
            print(f"  URL: {s['url'][:70]}...")

if __name__ == "__main__":
    asyncio.run(test_addon())
