import sys
import httpx
import time

sys.stdout.reconfigure(encoding='utf-8')

base = "https://nuvio-movies-addon.vercel.app"
print(f"Auditing Movies Addon at {base} ...", flush=True)

# Test 1: Ping
t0 = time.time()
r_ping = httpx.get(f"{base}/ping", timeout=10)
print(f"Ping: HTTP {r_ping.status_code} in {time.time()-t0:.2f}s -> {r_ping.text}", flush=True)

# Test 2: Movie stream (Fight Club)
t0 = time.time()
r = httpx.get(f"{base}/stream/movie/tt0137523.json", timeout=12)
dt = time.time() - t0
streams = r.json().get("streams", [])
print(f"[Fight Club] HTTP {r.status_code} in {dt:.2f}s | Found {len(streams)} streams", flush=True)
for s in streams:
    print(f"   Name: {s['name']} | Title: {s['title'].replace(chr(10), ' | ')}", flush=True)

# Test 3: TV series stream (Fallout)
t0 = time.time()
r = httpx.get(f"{base}/stream/series/tt12637874:1:1.json", timeout=12)
dt = time.time() - t0
streams = r.json().get("streams", [])
print(f"[Fallout S1E1] HTTP {r.status_code} in {dt:.2f}s | Found {len(streams)} streams", flush=True)
for s in streams:
    print(f"   Name: {s['name']} | Title: {s['title'].replace(chr(10), ' | ')}", flush=True)
