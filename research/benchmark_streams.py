import httpx
import time
from urllib.parse import urljoin

test_urls = {
    "Vidrock_Atlas": "https://cdn1.ngcorp.dad/e/DwYRNhFGRkRQWVI/master.m3u8",
    "Vidrock_Luna": "https://dreadnought.flamingo-e55.workers.dev/gDvIZoooCd2bTLsWnfRbOZeTccZt9Nyl4Z4s-kXV2Sb6G6gNgiwhA-QIVlOVXCKTre2bUWWwgoM-Q0VTtBgN_Q4xtlcvdpXgVzw-ww0xMXduq9fIw-Qg4u9snC7me9mLyknXE37ArxbO1f8giJdyPKGc5fNryslxMPYIiqhSWs5x9svYJUJHjBQlvrCw5J8uCyFqYbkxYIheIvCwn3i5hPR5jAXt0oR9L0IeqHg58oyg_F9KgZqDtt-hOF4HQjY0nwalRGaEg-Zhr5ikJdM8okuhJbjbaExIvRA0VxHTnEaflOJR9CetrTCU7z1nvJ4Dv-wu9O0AqVTUi2V2dBgk0NniALP1dBN8jkCWj0QiH6h6tbrgGDpgzxMdcVZNYmSUerg_hg3NYmtKCT1_wNTjempaz6GxgMBtVt5lia12qX32eJ4AbuBCcYY-H4gJBEZakjTjjGfh4AV-Hzgsz-gwnVK4OhGyGlAQ7gLM-pk3_eab5Te4y7cxb50ulHEm2RQY2PbE6JmJv-xpjkWbf7xXhMVldTePyqbJjrvLkub8i8RlLcySGi01oSjQh-nvDlS6nFbj3DDB38x6j3DJFV0RMbwLRLu4pkNVmeUo19rZ7TPO",
    "Vidrock_Orion": "https://shadowmoonwanderer.lol/file3/MGY1ZGMxOTMyMDliYzAxNDNiYTNlMjQ0ZTFlNzcxOWYxNzg5NjQyMDE1NTQ4OTM/master.m3u8",
    "Vidlove_VidAPI": "https://d.whysosigmabro.cfd/api?d=hCl9XkyuGIfGEct6G19k5H-o6gGqIUW0Wrh44I4nqLiKuNiMoYJ10wSDzW5FIAFxu4E8hy6doZA97lAsxSn5KrSD9ANB9Mm2Za7GtHANZp86kAUw4mSksfHZ_wCYldrLt8rjGjvwR-WgSLu9vz-UFZIaRa5VZTu8SKshNFH7o4RtJQJLkwc_xQHAgdO_LwOj4BFidHS6gF5_PyXMOyICSSctrqn6dTSsdstSUCjzi5MZj4-1m4YWiaYnnvhMhsdmhUKIuHVp48K6Pyzj_PGV6feTPFtIctOZ08Z9NmmRhtmL7js4qIAbGVx37_oSllcQW9l20Uha_A9YGBbDgSQLL8mQ2K0slT5zDukEnoN95S6O0lU8ARTHm0UsWGn_taQxnRJdZL1a88-nG_DCHldES46WoK-YiXkkMZ5JHW82wWk_Zw0Q5zdpLyQglEViqCWpxMC_4Z8d50tHpB0YVBIiRMqZo0T_FBJY-Ya3oxmxcgQFmLvjjYigVwHcawVktZ68c_WhUPsL1nWQuUzRNLE8Uwo7xM3jMPFBoXMR3qVtlJLNKSXeiy_VYI6aP4Z_"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://vidrock.net/'
}

for name, m3u8_url in test_urls.items():
    print(f"\n==================== Testing {name} ====================")
    h = dict(headers)
    if "Vidlove" in name:
        h['Referer'] = 'https://player.vidlove.cc/'
    try:
        r = httpx.get(m3u8_url, headers=h, follow_redirects=True, timeout=10)
        print(f"Master playlist status: {r.status_code}, length: {len(r.text)} chars")
        if r.status_code != 200:
            print("FAILED master playlist fetch")
            continue
        
        # Check master variants
        lines = [l.strip() for l in r.text.splitlines() if l.strip()]
        variant_urls = []
        for i, l in enumerate(lines):
            if l.startswith("#EXT-X-STREAM-INF"):
                print(f"  Variant info: {l}")
                if i + 1 < len(lines):
                    v_url = lines[i+1]
                    variant_urls.append(urljoin(str(r.url), v_url))
        
        # If no STREAM-INF, maybe this is already a media playlist
        if not variant_urls:
            segments = [urljoin(str(r.url), l) for l in lines if not l.startswith('#')]
            print(f"  Direct media playlist with {len(segments)} segments")
            test_seg = segments[0] if segments else None
        else:
            # Pick highest variant (usually last or has 1080)
            target_var = variant_urls[-1]
            print(f"  Fetching variant playlist: {target_var[:80]}...")
            vr = httpx.get(target_var, headers=h, follow_redirects=True, timeout=10)
            print(f"  Variant playlist status: {vr.status_code}")
            vlines = [l.strip() for l in vr.text.splitlines() if l.strip()]
            segments = [urljoin(str(vr.url), l) for l in vlines if not l.startswith('#')]
            print(f"  Variant has {len(segments)} segments")
            test_seg = segments[0] if segments else None
            
        if test_seg:
            print(f"  Downloading test segment: {test_seg[:80]}...")
            t0 = time.time()
            s_resp = httpx.get(test_seg, headers=h, follow_redirects=True, timeout=15)
            dt = time.time() - t0
            nbytes = len(s_resp.content)
            if s_resp.status_code == 200 and dt > 0:
                mbps = (nbytes * 8) / (dt * 1_000_000)
                print(f"  --> SUCCESS: {nbytes} bytes ({nbytes/1024/1024:.2f} MB) in {dt:.2f}s -> {mbps:.2f} Mbps!")
            else:
                print(f"  --> FAILED: status {s_resp.status_code} in {dt:.2f}s")
    except Exception as e:
        print(f"Error testing {name}: {e}")
