import asyncio
import sys
sys.path.insert(0, r'F:\nuvio-movies-addon')

from providers import atlantic

async def test():
    print("Testing Atlantic provider...")
    # Test Inception (tmdb: 27205)
    s_movie = await atlantic.resolve(27205, ctype="movie", title="Inception", year=2010)
    print(f"Got {len(s_movie)} movie streams:")
    for s in s_movie:
        print(f"  Name: {s['name']}")
        print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
        print(f"  URL: {s['url'][:80]}...")
        print(f"  Size: {s.get('size')} bytes")

    # Test Breaking Bad (tmdb: 1396) S1E1
    print("\nTesting Breaking Bad (series)...")
    s_tv = await atlantic.resolve(1396, ctype="series", season=1, episode=1, title="Breaking Bad", year=2008)
    print(f"Got {len(s_tv)} TV streams:")
    for s in s_tv:
        print(f"  Name: {s['name']}")
        print(f"  Title: {s['title'].replace(chr(10), ' | ')}")
        print(f"  URL: {s['url'][:80]}...")

if __name__ == "__main__":
    asyncio.run(test())