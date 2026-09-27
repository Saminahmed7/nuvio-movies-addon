import requests
import json
import base64
import hashlib
import time
import re

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

def b64url_encode(data: bytes) -> str:
    return base64.b64encode(data).decode().replace('+', '-').replace('/', '_').rstrip('=')

def b64url_decode(s: str) -> bytes:
    s = s.replace('-', '+').replace('/', '/')
    s += '=' * (-len(s) % 4)
    return base64.b64decode(s)

def b64_decode_part(part: str) -> bytes:
    """Decode a base64url part (from JWT-like tokens)."""
    padded = part + '=' * (-len(part) % 4)
    try:
        return base64.b64decode(padded)
    except:
        # try urlsafe
        padded2 = part.replace('-', '+').replace('_', '/') + '=' * (-len(part) % 4)
        return base64.b64decode(padded2)

def make_x_cs_q(media_type, tmdb_id, season=None, episode=None):
    data = json.dumps([media_type, tmdb_id, season, episode])
    raw = data.encode('utf-8')
    # btoa equivalent: convert UTF-8 bytes to latin1 string
    latin1_str = ''.join(chr(b) for b in raw)
    b64 = base64.b64encode(latin1_str.encode('latin1')).decode()
    return b64.replace('+', '-').replace('/', '_').rstrip('=')

def solve_pow(nonce_seed: str, deadline_ms: int, max_iters=10000000) -> int:
    """SHA256 PoW: find nonce such that SHA256(seed+nonce) is minimal (lowest hash)."""
    # The deadline_ms is actually a Unix timestamp in milliseconds = when challenge expires
    # The real challenge might be: SHA256(n + str(nonce)).startswith('0' * difficulty)
    # Let's look at the JS more carefully.
    # From the decoded payload: {"v":1,"n":"AMhDiEifpDPgGWJS_dP5Lm3b","t":1790517624326}
    # t looks like a Unix ms timestamp = deadline
    # The actual PoW is in the pow-worker-v3.js / pow-v3.wasm
    # Without running the WASM, let's try common PoW patterns:
    
    # Try: SHA256(seed + nonce) < target_hex
    # Common default: leading zeros bits
    print(f"  Solving PoW: seed={nonce_seed}, deadline={deadline_ms}")
    
    # Let's try to just call /api/c/issue without solving PoW first
    # The challenge might be optional or the server might accept it anyway
    return 0  # skip for now


def cinesrc_get_stream(media_type, tmdb_id, season=None, episode=None):
    session = requests.Session()
    session.headers.update({
        'User-Agent': UA,
    })
    
    # 1. Load embed page (get cookies)
    if media_type == 'tv':
        embed_url = f'https://cinesrc.st/embed/tv/{tmdb_id}?s={season}&e={episode}'
    else:
        embed_url = f'https://cinesrc.st/embed/movie/{tmdb_id}'
    
    r0 = session.get(embed_url, timeout=10, headers={
        'Referer': 'https://cinesrc.st/'
    })
    print(f"[1] Embed page: {r0.status_code}")
    
    # 2. Build x-cs-q
    x_cs_q = make_x_cs_q(media_type, tmdb_id, season, episode)
    print(f"[2] x-cs-q: {x_cs_q}")
    
    # 3. Bootstrap
    r1 = session.post(
        'https://cinesrc.st/api/c/bootstrap',
        headers={
            'x-cs-q': x_cs_q,
            'Cache-Control': 'no-store',
            'Content-Type': 'application/json',
            'Referer': embed_url,
            'Origin': 'https://cinesrc.st',
        },
        timeout=10
    )
    print(f"[3] Bootstrap: {r1.status_code} -> {r1.text[:200]}")
    
    if not r1.ok:
        return None
    
    boot_data = r1.json()
    x_cs_r = boot_data.get('r', '')
    x_cs_p = boot_data.get('p', '')
    
    print(f"    x-cs-r: {x_cs_r[:50]}...")
    
    # Decode x-cs-p
    p_parts = x_cs_p.split('.')
    pow_payload = json.loads(b64_decode_part(p_parts[0]))
    print(f"[4] PoW challenge: {pow_payload}")
    
    nonce_seed = pow_payload.get('n', '')
    deadline_ms = pow_payload.get('t', 0)
    
    # 5. Try direct issue first (no PoW) - maybe the server is lenient
    print(f"\n[5] Trying direct /api/c/issue without PoW...")
    r2 = session.post(
        'https://cinesrc.st/api/c/issue',
        headers={
            'x-cs-q': x_cs_q,
            'x-cs-r': x_cs_r,
            'x-cs-p': x_cs_p,
            'Content-Type': 'application/json',
            'Referer': embed_url,
            'Origin': 'https://cinesrc.st',
        },
        json={},
        timeout=10
    )
    print(f"    Issue (no PoW): {r2.status_code} -> {r2.text[:400]}")
    
    if r2.ok:
        return r2.json()
    
    # 6. Try with enc-dec.app
    print(f"\n[6] Trying enc-dec.app as fallback...")
    enc_r = requests.get(
        'https://enc-dec.app/api/enc-cinesrc',
        params={'url': embed_url},
        timeout=15
    )
    print(f"    enc-dec.app GET: {enc_r.status_code} -> {enc_r.text[:300]}")
    
    return None


result = cinesrc_get_stream('movie', '550')
print("\nFinal result:", result)
