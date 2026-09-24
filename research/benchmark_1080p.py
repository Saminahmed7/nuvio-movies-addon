import httpx
import time
from urllib.parse import urljoin

base_url = "https://cdn30091.irada438esc.com/stream2/i-arch-400/9e34436d99ab5ed13be3eea6b2202e7f/MJTMsp1RshGTygnMNRUR2N2MSlnWXZEdMNDZzQWe5MDZzMmdZJTO1R2RWVHZDljekhkSsl1VwYnWtx2cihVT2p1RRdXWqNGeOR1ZwoFRKhWTUlEeZ1WR10ERJBTTXF1dNp2Yx0kaWpWWXFVP:1790216969:50.7.41.247:433f3e1b19bf3790eced904b0755390b36481d4ef7addda36b4d902c64d5050c:==gTUFUdOlHNw00U0knTENWP/index.m3u8"

url_1080 = urljoin(base_url, "./1080/index.m3u8")

print(f"Testing 1080p playlist: {url_1080}")
# 1. Bare GET (no custom headers)
r = httpx.get(url_1080, timeout=10)
print(f"Bare GET status: {r.status_code}")
lines = [l.strip() for l in r.text.splitlines() if l.strip()]
print(f"First 10 lines of 1080p playlist:")
for l in lines[:10]:
    print(" ", l)

# Find first segment
segments = [l for l in lines if not l.startswith('#')]
print(f"Total segments in 1080p: {len(segments)}")

if segments:
    seg_url = urljoin(url_1080, segments[0])
    print(f"\nBenchmarking segment download: {seg_url}")
    t0 = time.time()
    seg_resp = httpx.get(seg_url, timeout=10)
    dt = time.time() - t0
    seg_bytes = len(seg_resp.content)
    speed_mbps = (seg_bytes * 8) / (dt * 1_000_000)
    print(f"Segment downloaded: {seg_bytes} bytes in {dt:.3f}s -> SPEED = {speed_mbps:.2f} Mbps!")
    
    # Download 2nd segment
    if len(segments) > 1:
        seg_url2 = urljoin(url_1080, segments[1])
        t0 = time.time()
        seg_resp2 = httpx.get(seg_url2, timeout=10)
        dt2 = time.time() - t0
        speed_mbps2 = (len(seg_resp2.content) * 8) / (dt2 * 1_000_000)
        print(f"Segment 2 downloaded: {len(seg_resp2.content)} bytes in {dt2:.3f}s -> SPEED = {speed_mbps2:.2f} Mbps!")
