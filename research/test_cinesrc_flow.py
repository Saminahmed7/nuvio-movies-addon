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
    s = s.replace('-', '+').replace('_', '/')
    s += '=' * (-len(s) % 4)
    return base64.b64decode(s)

def make_x_cs_q(media_type, tmdb_id, season=None, episode=None):
    data = json.dumps([media_type, tmdb_id, season, episode])
    return b64url_encode(data.encode('utf-8'))

def cinesrc_get_stream(media_type, tmdb_id, season=None, episode=None):
    session = requests.Session()
    session.headers.update({
        'User-Agent': UA,
        'Referer': f'https://cinesrc.st/embed/{media_type}/{tmdb_id}',
        'Origin': 'https://cinesrc.st',
    })
    
    # 1. Load embed page (get cookies)
    if media_type == 'tv':
        embed_url = f'https://cinesrc.st/embed/tv/{tmdb_id}?s={season}&e={episode}'
    else:
        embed_url = f'https://cinesrc.st/embed/movie/{tmdb_id}'
    
    r0 = session.get(embed_url, timeout=10)
    print(f"[1] Embed page: {r0.status_code}")
    
    # 2. Build x-cs-q
    x_cs_q = make_x_cs_q(media_type, tmdb_id, season, episode)
    print(f"[2] x-cs-q: {x_cs_q}")
    
    # 3. Bootstrap - get challenge parameters
    r1 = session.post(
        'https://cinesrc.st/api/c/bootstrap',
        headers={
            'x-cs-q': x_cs_q,
            'Cache-Control': 'no-store',
            'Content-Type': 'application/json',
        },
        timeout=10
    )
    print(f"[3] Bootstrap: {r1.status_code} -> {r1.text[:200]}")
    
    if not r1.ok:
        return None
    
    boot_data = r1.json()
    # r = signed session token, p = PoW challenge
    x_cs_r = boot_data.get('r', '')
    x_cs_p = boot_data.get('p', '')
    
    print(f"    x-cs-r: {x_cs_r[:50]}...")
    print(f"    x-cs-p: {x_cs_p[:80]}...")
    
    # 4. Decode the PoW challenge from x-cs-p
    # x-cs-p is JWT-like: base64url_header.base64url_payload.base64url_sig
    p_parts = x_cs_p.split('.')
    if len(p_parts) >= 2:
        payload = json.loads(b64url_decode(p_parts[1]))
        print(f"[4] PoW challenge payload: {payload}")
        
        # Standard PoW: find nonce such that SHA256(n + nonce) starts with leading zeros
        # n = nonce seed, t = difficulty target (typically leading zero bits)
        nonce_seed = payload.get('n', '')
        difficulty = payload.get('t', 100000)  # default
        print(f"    nonce_seed={nonce_seed}, difficulty={difficulty}")
        
        # SHA256 PoW solve
        print("    Solving PoW...")
        start = time.time()
        nonce = 0
        while True:
            candidate = f"{nonce_seed}{nonce}"
            h = hashlib.sha256(candidate.encode()).hexdigest()
            # Check if starts with difficulty zeros in decimal equivalent
            # (compare hash int value against target)
            # or just check leading zero bytes 
            # Let's try both: hash < difficulty or hash[:N] == '0' * N
            hash_int = int(h, 16)
            if hash_int < (2**256 // difficulty):
                break
            nonce += 1
            if nonce > 5000000:
                print("    PoW too hard, giving up")
                break
        
        elapsed = time.time() - start
        print(f"    PoW solved! nonce={nonce} in {elapsed:.2f}s")
        
        # Build gc() result = stage1 PoW result
        stage1_result = b64url_encode(json.dumps({
            "n": nonce_seed,
            "v": nonce,
            "t": difficulty
        }).encode())
        print(f"    stage1_result={stage1_result[:60]}...")
    
    # 5. Now POST to /api/c/issue with x-cs-r, x-cs-q, x-cs-p headers
    # The actual stream URL comes from /api/c/issue
    r2 = session.post(
        'https://cinesrc.st/api/c/issue',
        headers={
            'x-cs-q': x_cs_q,
            'x-cs-r': x_cs_r,
            'x-cs-p': x_cs_p,
            'Content-Type': 'application/json',
        },
        json={},
        timeout=10
    )
    print(f"[5] Issue: {r2.status_code} -> {r2.text[:400]}")
    
    return r2.json() if r2.ok else None


result = cinesrc_get_stream('movie', '550')
print("\nFinal result:", result)
