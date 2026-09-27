import asyncio
import sys
sys.path.insert(0, r'F:\nuvio-movies-addon')

from providers import videasy

# Patch to only test Neon server
original_priority = videasy.SERVER_PRIORITY
videasy.SERVER_PRIORITY = ["Neon"]

async def test():
    print("Testing VideoEasy provider (single server: Neon)...")
    # Test Inception (tmdb: 27205)
    s_movie = await videasy.resolve(27205, ctype="movie", title="Inception", year=2010)
    print(f"Got {len(s_movie)} movie streams:")
    for s in s_movie[:5]:
        print(f"  Name: {s['name']}")
        print(f"  Title: {s['title']}")
        print(f"  URL: {s['url'][:80]}...")
        print(f"  Quality: {s['quality']}")
        print()

if __name__ == "__main__":
    asyncio.run(test())
    videasy.SERVER_PRIORITY = original_priority