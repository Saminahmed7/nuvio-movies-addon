import httpx
import time
from urllib.parse import urljoin

urls = {
    'Aphrodite': 'https://totallyacdn.org/m3u8-proxy?payload=z3LXLpXMbV2cHXBK.EruZCPz4n516zFRx1wCgIk9YT88odAm3A5x1wZ3lStUhi6j5veP3VIjrBjXfZ2Gg2_0gCY7VNAlNa0C6gJYiDtfbzUA088M',
    'Artemis': 'https://peraspera.nbsycfzrpa4.workers.dev/m3u8-proxy?payload=ifOB4N3dYil6pofS.K3C16biWactliyQ9cCNmTCwhjfF1vlplDZcoA0_S5VUHwurXm55Bms6KSFIeQuur5xMw5sqgcrdsBGv8JwxU1vaiJg2Vvg'
}

for name, u in urls.items():
    print(f"\n=================== TESTING {name} ===================")
    r = httpx.get(u, follow_redirects=True, timeout=12)
    print(f"Master playlist status: {r.status_code}")
    print(r.text[:600])

    lines = [l.strip() for l in r.text.splitlines() if l.strip()]
    variants = []
    for idx, l in enumerate(lines):
        if l.startswith('#EXT-X-STREAM-INF'):
            variants.append((l, lines[idx+1]))
    
    print(f"Total stream variants: {len(variants)}")
    for inf, v_url in variants:
        print(" ", inf)
        print("  ->", v_url[:80])
    
    # Pick highest variant
    if variants:
        best_inf, best_url = variants[-1]
        best_full = urljoin(str(r.url), best_url)
        print(f"\nFetching highest variant playlist: {best_full[:80]}...")
        r_var = httpx.get(best_full, follow_redirects=True, timeout=10)
        var_lines = [l.strip() for l in r_var.text.splitlines() if l.strip()]
        segments = [l for l in var_lines if not l.startswith('#')]
        print(f"Total segments: {len(segments)}")

        if segments:
            seg_full = urljoin(str(r_var.url), segments[0])
            print(f"Benchmarking segment download: {seg_full[:80]}...")
            t0 = time.time()
            resp_seg = httpx.get(seg_full, follow_redirects=True, timeout=15)
            dt = time.time() - t0
            nbytes = len(resp_seg.content)
            mbps = (nbytes * 8) / (dt * 1_000_000)
            print(f"Segment 1: {nbytes} bytes ({nbytes/1024/1024:.2f} MB) in {dt:.3f}s -> SPEED = {mbps:.2f} Mbps!")
            
            # Download 2nd segment
            if len(segments) > 1:
                seg_full2 = urljoin(str(r_var.url), segments[1])
                t0 = time.time()
                resp_seg2 = httpx.get(seg_full2, follow_redirects=True, timeout=15)
                dt2 = time.time() - t0
                nbytes2 = len(resp_seg2.content)
                mbps2 = (nbytes2 * 8) / (dt2 * 1_000_000)
                print(f"Segment 2: {nbytes2} bytes ({nbytes2/1024/1024:.2f} MB) in {dt2:.3f}s -> SPEED = {mbps2:.2f} Mbps!")
