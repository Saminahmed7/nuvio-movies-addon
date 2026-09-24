import httpx
import time
from urllib.parse import urljoin

base_url = 'https://cdn30091.irada438esc.com/stream2/i-arch-400/9e34436d99ab5ed13be3eea6b2202e7f/MJTMsp1RshGTygnMNRUR2N2MSlnWXZEdMNDZzQWe5MDZzMmdZJTO1R2RWVHZDljekhkSsl1VwYnWtx2cihVT2p1RRdXWqNGeOR1ZwoFRKhWTUlEeZ1WR10ERJBTTXF1dNp2Yx0kaWpWWXFVP:1790216969:50.7.41.247:433f3e1b19bf3790eced904b0755390b36481d4ef7addda36b4d902c64d5050c:==gTUFUdOlHNw00U0knTENWP/1080/index.m3u8'
headers = {
    'origin': 'https://laika422mon.com',
    'referer': 'https://laika422mon.com//play/tt1375666',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

r = httpx.get(base_url, headers=headers, follow_redirects=True)
lines = [l.strip() for l in r.text.splitlines() if l.strip()]
segments = [l for l in lines if not l.startswith('#')]
print(f"Total 1080p segments: {len(segments)}")

# Also check segment URLs without headers (are segments protected or bare?)
seg1_url = urljoin(base_url, segments[0])
print(f"Segment 1 URL: {seg1_url[:90]}...")

# Test segment bare
r_bare = httpx.get(seg1_url, timeout=10)
print(f"Segment bare status: {r_bare.status_code}")

# Download 3 segments with headers to benchmark bandwidth
speeds = []
for idx in range(min(3, len(segments))):
    seg_url = urljoin(base_url, segments[idx])
    t0 = time.time()
    resp = httpx.get(seg_url, headers=headers, timeout=15)
    dt = time.time() - t0
    nbytes = len(resp.content)
    mbps = (nbytes * 8) / (dt * 1_000_000)
    speeds.append(mbps)
    print(f"Segment {idx+1}: {nbytes} bytes ({nbytes/1024/1024:.2f} MB) in {dt:.3f}s -> {mbps:.2f} Mbps")

avg_speed = sum(speeds) / len(speeds)
print(f"\nAverage Throughput: {avg_speed:.2f} Mbps")
print(f"1080p Bitrate required: ~3.0 Mbps")
if avg_speed >= 10.0:
    print("PASS: High-speed CDN, smooth buffer-free streaming!")
else:
    print("WARNING: Slower throughput.")
