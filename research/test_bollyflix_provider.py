import asyncio
import sys
sys.path.insert(0, r'F:\nuvio-movies-addon')

from providers import bollyflix

async def test():
    print("Testing Bollyflix provider...")
    # Test with Fight Club
    streams = await bollyflix.resolve(550, ctype="movie", title="Fight Club", year=1999)
    print(f"Got {len(streams)} streams:")
    for s in streams[:5]:
        print(f"  Name: {s['name']}")
        print(f"  URL: {s['url'][:80]}...")
        print()

    # Test with Inception
    print("\nTesting Inception...")
    streams2 = await bollyflix.resolve(27205, ctype="movie", title="Inception", year=2010)
    print(f"Got {len(streams2)} streams:")
    for s in streams2[:5]:
        print(f"  Name: {s['name']}")
        print(f"  URL: {s['url'][:80]}...")

if __name__ == "__main__":
    asyncio.run(test())