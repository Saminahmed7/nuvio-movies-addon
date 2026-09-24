import httpx
import time
import re

english_stream_url = "https://i-arch-400.irada438esc.com/stream2/i-arch-400/9e34436d99ab5ed13be3eea6b2202e7f/MJTMsp1RshGTygnMNRUR2N2MSlnWXZEdMNDZzQWe5MDZzMmdZJTO1R2RWVHZDljekhkSsl1VwYnWtx2cihVT2p1RRdXWqNGeOR1ZwoFRKhWTUlEeZ1WR10ERJBTTXF1dNp2Yx0kaWpWWXFVP:1790216969:50.7.41.247:433f3e1b19bf3790eced904b0755390b36481d4ef7addda36b4d902c64d5050c:==gTUFUdOlHNw00U0knTENWP/index.m3u8"

headers = {
    "origin": "https://laika422mon.com",
    "referer": "https://laika422mon.com//play/tt1375666",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

print("Fetching master playlist...")
r = httpx.get(english_stream_url, headers=headers, timeout=10)
print(f"Master playlist status: {r.status_code}")
print(r.text)

# Also test fetching without headers (can media players like VLC / Stremio play it bare?)
r_bare = httpx.get(english_stream_url, timeout=10)
print(f"Master playlist bare (no referer) status: {r_bare.status_code}")
