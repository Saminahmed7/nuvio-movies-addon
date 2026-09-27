import requests
import json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
headers = {"User-Agent": UA}

print("=== 1. vadapav.mov ===")
try:
    r = requests.get("https://stremio.vadapav.mov/stream/movie/tt0137523.json", headers=headers, timeout=5)
    print("vadapav movie:", r.status_code)
    if r.status_code == 200:
        print(r.json().get("streams", [])[:2])
except Exception as e:
    print("vadapav error:", e)

print("\n=== 2. febapi.nuvioapp.space ===")
try:
    r = requests.get("https://febapi.nuvioapp.space/api/media/movie/550", headers=headers, timeout=5)
    print("febapi status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("febapi error:", e)

print("\n=== 3. api.wecollege.net ===")
try:
    r = requests.get("https://api.wecollege.net/seed?mediaId=550", headers=headers, timeout=5)
    print("wecollege status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("wecollege error:", e)

print("\n=== 4. player.vidzee.wtf ===")
try:
    r = requests.get("https://player.vidzee.wtf/api/server?id=550", headers=headers, timeout=5)
    print("vidzee status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("vidzee error:", e)

print("\n=== 5. vidhawk.buzz ===")
try:
    r = requests.get("https://vidhawk.buzz/api/stream/race?id=550", headers=headers, timeout=5)
    print("vidhawk status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("vidhawk error:", e)

print("\n=== 6. www.rivestream.app ===")
try:
    r = requests.get("https://www.rivestream.app/api/backendfetch?id=550", headers=headers, timeout=5)
    print("rivestream status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("rivestream error:", e)

print("\n=== 7. play.xpass.top ===")
try:
    r = requests.get("https://play.xpass.top/e/movie/550", headers=headers, timeout=5)
    print("xpass status:", r.status_code)
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print("xpass error:", e)
