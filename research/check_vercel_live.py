import httpx
import time

url = "https://nuvio-movies-addon.vercel.app"
print("Pinging Vercel deployment...")

for endpoint in ["/ping", "/health", "/manifest.json", "/diag"]:
    try:
        r = httpx.get(f"{url}{endpoint}", timeout=10)
        print(f"[{endpoint}] Status: {r.status_code}")
        print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"[{endpoint}] Error: {e}")
