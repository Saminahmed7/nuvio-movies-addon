import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

r = requests.get("https://player.vidzee.wtf/embed/movie/550", headers=headers, timeout=10)
print("status:", r.status_code)
print("HTML len:", len(r.text))

# Let's save it to inspect
with open("research/vidzee_embed.html", "w", encoding="utf-8") as f:
    f.write(r.text)

# Check scripts
scripts = re.findall(r'src=["\']([^"\']+)["\']', r.text)
print("Scripts on embed page:", scripts)

# Check preloads
preloads = re.findall(r'href=["\'](/assets/[^"\']+)["\']', r.text)
print("Preloads:", preloads)

# Check any data embedded in HTML
for m in re.finditer(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL):
    s = m.group(1)
    if 'tsr' in s or 'data' in s or 'server' in s:
        print("Inline script snippet:", s[:300])
