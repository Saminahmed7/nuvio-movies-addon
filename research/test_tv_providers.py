import asyncio
import sys
sys.path.insert(0, r'F:\nuvio-movies-addon')

from providers import vidlove
from providers import vidrock

async def test_tv_shows():
    # Test various TV shows
    shows = [
        ("Breaking Bad", 1396, 1, 1),  # S1E1
        ("Breaking Bad", 1396, 5, 16),  # S5E16 (finale)
        ("Game of Thrones", 1399, 1, 1),  # S1E1
        ("Stranger Things", 66732, 1, 1),  # S1E1
        ("The Boys", 76479, 1, 1),  # S1E1
        ("House of the Dragon", 94997, 1, 1),  # S1E1
        ("Fallout", 106379, 1, 1),  # S1E1
    ]
    
    for name, tmdb_id, season, episode in shows:
        print(f"\n{'='*60}")
        print(f"Testing {name} S{season}E{episode} (tmdb: {tmdb_id})")
        print(f"{'='*60}")
        
        # Test Vidlove
        print(f"\n--- Vidlove ---")
        try:
            s_vidlove = await vidlove.resolve(tmdb_id, ctype="series", season=season, episode=episode, title=name, year=2008)
            print(f"Got {len(s_vidlove)} streams:")
            for s in s_vidlove:
                print(f"  [{s['name']}] {s['title'].split(chr(10))[0]}")
                print(f"  URL: {s['url'][:80]}...")
                print(f"  Subtitles: {len(s.get('subtitles', []))}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test Vidrock
        print(f"\n--- Vidrock ---")
        try:
            s_vidrock = await vidrock.resolve(tmdb_id, ctype="series", season=season, episode=episode, title=name, year=2008)
            print(f"Got {len(s_vidrock)} streams:")
            for s in s_vidrock:
                print(f"  [{s['name']}] {s['title'].split(chr(10))[0]}")
                print(f"  URL: {s['url'][:80]}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_tv_shows())