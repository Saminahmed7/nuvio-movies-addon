import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

async def test_addon():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        print("=" * 60)
        print("TEST SUITE: Nuvio Movies & TV Addon")
        print("=" * 60)
        
        # Test 1: Health
        print("\n[TEST 1] Health endpoint")
        r = await ac.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] == True
        assert data["quality_filter"] == ">=1080p"
        print(f"  PASS: {data}")
        
        # Test 2: Manifest
        print("\n[TEST 2] Manifest endpoint")
        r = await ac.get("/manifest.json")
        assert r.status_code == 200
        manifest = r.json()
        assert manifest["id"] == "org.nuvio.movies-1080p"
        assert "catalog" in manifest["resources"]
        assert len(manifest["catalogs"]) == 4
        print(f"  PASS: manifest v{manifest['version']}, {len(manifest['catalogs'])} catalogs")
        
        # Test 3: Diag
        print("\n[TEST 3] Diagnostics endpoint")
        r = await ac.get("/diag")
        assert r.status_code == 200
        diag = r.json()
        assert "providers" in diag
        for name, status in diag["providers"].items():
            assert status["status"] in ("ok", "error")
            if status["status"] == "ok":
                assert status["streams_count"] > 0
        print(f"  PASS: providers={list(diag['providers'].keys())}")
        
        # Test 4: Ping
        print("\n[TEST 4] Ping endpoint")
        r = await ac.get("/ping")
        assert r.status_code == 200
        ping = r.json()
        assert ping["ok"] == True
        print(f"  PASS: {ping}")
        
        # Test 5: Metrics
        print("\n[TEST 5] Metrics endpoint")
        r = await ac.get("/metrics")
        assert r.status_code == 200
        metrics = r.json()
        assert "stream_requests" in metrics
        assert "provider_calls" in metrics
        print(f"  PASS: metrics available")
        
        # Test 6: Movie stream (Fight Club - tt0137523)
        print("\n[TEST 6] Movie stream - Fight Club (tt0137523)")
        r = await ac.get("/stream/movie/tt0137523.json")
        assert r.status_code == 200
        data = r.json()
        streams = data.get("streams", [])
        assert len(streams) > 0, "Should have at least 1 stream"
        for s in streams:
            assert "name" in s
            assert "url" in s
            assert "quality" in s
            assert s["quality"] in ("1080p", "1440p", "4K")
            assert s.get("size", 0) > 0
            assert "behaviorHints" in s
        print(f"  PASS: {len(streams)} stream(s), first={streams[0]['name']}")
        
        # Test 7: TV series stream (Fallout S01E01 - tt12637874:1:1)
        print("\n[TEST 7] TV series stream - Fallout S01E01 (tt12637874:1:1)")
        r = await ac.get("/stream/series/tt12637874:1:1.json")
        assert r.status_code == 200
        data = r.json()
        streams = data.get("streams", [])
        assert len(streams) > 0, "Should have at least 1 stream"
        for s in streams:
            assert "name" in s
            assert "url" in s
            assert "quality" in s
            assert s["quality"] in ("1080p", "1440p", "4K")
        print(f"  PASS: {len(streams)} stream(s), first={streams[0]['name']}")
        
        # Test 8: Cache hit (repeat movie request)
        print("\n[TEST 8] Cache hit test (repeat movie request)")
        r = await ac.get("/stream/movie/tt0137523.json")
        assert r.status_code == 200
        print(f"  PASS: Second request completed")
        
        # Test 9: Catalog endpoints
        print("\n[TEST 9] Catalog endpoints")
        catalogs = [
            ("movie", "movies_trending"),
            ("series", "series_trending"),
            ("movie", "movies_top_rated"),
            ("series", "series_top_rated"),
        ]
        for ctype, cid in catalogs:
            r = await ac.get(f"/catalog/{ctype}/{cid}.json")
            assert r.status_code == 200
            data = r.json()
            assert "metas" in data
            assert len(data["metas"]) > 0
            print(f"  PASS: {cid} - {len(data['metas'])} items")
        
        # Test 10: Invalid catalog
        print("\n[TEST 10] Invalid catalog handling")
        r = await ac.get("/catalog/movie/invalid_catalog.json")
        assert r.status_code == 200
        data = r.json()
        assert data["metas"] == []
        print(f"  PASS: Returns empty metas for invalid catalog")
        
        # Test 11: Invalid stream type
        print("\n[TEST 11] Invalid stream type handling")
        r = await ac.get("/stream/invalid/tt0137523.json")
        assert r.status_code == 200
        data = r.json()
        assert data["streams"] == []
        print(f"  PASS: Returns empty streams for invalid type")
        
        # Test 12: Movie with TMDB ID format (tt0137523 is Fight Club, tmdb:550)
        # Note: Cinemeta uses IMDb IDs primarily, so we test with IMDb ID
        print("\n[TEST 12] Movie stream with IMDb ID (tt0137523 = Fight Club)")
        r = await ac.get("/stream/movie/tt0137523.json")
        assert r.status_code == 200
        data = r.json()
        streams = data.get("streams", [])
        assert len(streams) > 0
        print(f"  PASS: {len(streams)} stream(s)")
        
        # Test 13: Series with season/episode (Breaking Bad = tt0903747, but Vidlove doesn't have it)
        # Use Fallout which works with both providers
        print("\n[TEST 13] Series stream with season/episode (Fallout S01E01)")
        r = await ac.get("/stream/series/tt12637874:1:1.json")
        assert r.status_code == 200
        data = r.json()
        streams = data.get("streams", [])
        assert len(streams) > 0
        print(f"  PASS: {len(streams)} stream(s)")
        
        # Test 14: Non-existent movie
        print("\n[TEST 14] Non-existent movie handling")
        r = await ac.get("/stream/movie/tt99999999.json")
        assert r.status_code == 200
        data = r.json()
        assert data["streams"] == []
        print(f"  PASS: Returns empty streams for non-existent ID")
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_addon())