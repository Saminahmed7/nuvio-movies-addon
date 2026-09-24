import httpx
import time
from urllib.parse import urljoin

url_1080 = "https://d.whysosigmabro.cfd/api?d=hCl9XkyuGIfGEct6G19k5H-o6gGqIUW0Wrh44I4nqLiKuNiMoYJ10wSDzW5FIAFxu4E8hy6doZA97lAsxSn5KrSD9ANB9Mm2Za7GtHANZp86kAUw4mSksfHZ_wCYldrLt8rjGjvwR-WgSLu9vz-UFZIaRa5VZTu8SKshNFH7o4RtJQJLkwc_xQHAgdO_LwOj4BFidHS6gF5_PyXMOyICSSctrqn6dTSsdstSUCjzi5MZj4-1m4YWiaYnnvhMhsdmhUKIuHVp48K6Pyzj_PGV6feTPFtIctOZ08Z9NmmRhtmL7js4qIAbGVx37_oSllcQW9l20Uha_A9YGBbDgSQLL8mQ2K0slT5zDukEnoN95S6O0lU8ARTHm0UsWGn_taQxnRJdZL1a88-nG_DCHldES46WoK-YiXkkMZ5JHW82wWk_Zw0Q5zdpLyQglEViqCWpxMC_4Z8d50tHpB0YVBIiRMqZo0T_FBJY-Ya3oxmxcgQFmLvjjYigVwHcawVktZ68c_WhUPsL1nWQuUzRNLE8Uwo7xM3jMPFBoXMR3qVtlJLNKSXeiy_VYI6aP4Z_"

print("1. Testing bare GET on 1080p variant playlist...")
r = httpx.get(url_1080, follow_redirects=True, timeout=10)
print(f"Bare GET status: {r.status_code}")
print(r.text[:500])

lines = [l.strip() for l in r.text.splitlines() if l.strip()]
segments = [l for l in lines if not l.startswith('#')]
print(f"\nTotal 1080p segments: {len(segments)}")

if segments:
    seg_url = segments[0] if segments[0].startswith('http') else urljoin(str(r.url), segments[0])
    print(f"Testing segment 1 download: {seg_url[:80]}...")
    t0 = time.time()
    seg_resp = httpx.get(seg_url, follow_redirects=True, timeout=15)
    dt = time.time() - t0
    nbytes = len(seg_resp.content)
    mbps = (nbytes * 8) / (dt * 1_000_000)
    print(f"Segment 1: {nbytes} bytes ({nbytes/1024/1024:.2f} MB) in {dt:.3f}s -> SPEED = {mbps:.2f} Mbps!")

    if len(segments) > 1:
        seg_url2 = segments[1] if segments[1].startswith('http') else urljoin(str(r.url), segments[1])
        t0 = time.time()
        seg_resp2 = httpx.get(seg_url2, follow_redirects=True, timeout=15)
        dt2 = time.time() - t0
        nbytes2 = len(seg_resp2.content)
        mbps2 = (nbytes2 * 8) / (dt2 * 1_000_000)
        print(f"Segment 2: {nbytes2} bytes ({nbytes2/1024/1024:.2f} MB) in {dt2:.3f}s -> SPEED = {mbps2:.2f} Mbps!")
