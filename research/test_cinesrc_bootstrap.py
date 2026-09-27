import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

# Now let's try to use enc-dec.app to bypass CineSrc challenge
# The enc-dec.app needs: { url, agent, challenge_data }
# But first, we need challenge_data from /api/c/bootstrap

# Step 1: Get the x-cs-q token which is base64(JSON.stringify([type, id, season, episode]))
import base64
import json

media_type = "movie"
tmdb_id = "550"
season = None
episode = None

q_data = json.dumps([media_type, tmdb_id, season, episode])
q_bytes = q_data.encode('utf-8')
q_b64 = base64.b64encode(q_bytes).decode('utf-8')
q_b64_url = q_b64.replace('+', '-').replace('/', '_').rstrip('=')

print("x-cs-q token:", q_b64_url)

# Step 2: POST to /api/c/bootstrap with x-cs-q header
session = requests.Session()
session.headers.update({
    'User-Agent': headers['User-Agent'],
    'Referer': 'https://cinesrc.st/embed/movie/550',
    'Origin': 'https://cinesrc.st',
})

# First visit the page to get cookies
r0 = session.get('https://cinesrc.st/embed/movie/550', timeout=10)
print("Embed page status:", r0.status_code)
print("Cookies:", dict(session.cookies))

# Now bootstrap
r1 = session.post(
    'https://cinesrc.st/api/c/bootstrap',
    headers={
        'x-cs-q': q_b64_url,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store',
    },
    timeout=10
)
print("Bootstrap status:", r1.status_code)
print("Bootstrap response:", r1.text[:500])
