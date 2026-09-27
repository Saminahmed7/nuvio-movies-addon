import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# The WASM only exports memory, __data_end, __heap_base and has encrypted/obfuscated function names
# The worker uses it via: gBhNBaT[A6aLoqc[0x15]](Vt6kXkC[MF0BgU(A6aLoqc[0x18])])
# A6aLoqc[0x15] = 0x64 = 100 -> "a" (from the array: ["a"])
# Let me try a simpler approach: the enc-dec.app POST endpoint

# Based on the error message: POST: { url, agent, challenge_data: { 'stage1': stage1_object, 'stage2': stage2_object } }
# The stage1_object and stage2_object come from the PoW worker

# Let's see what happens if we send dummy challenge data
# Maybe enc-dec.app can do the PoW itself?

import json

test_payload = {
    "url": "https://cinesrc.st/embed/movie/550",
    "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "challenge_data": {
        "stage1": {"test": "dummy"},
        "stage2": {"test": "dummy2"}
    }
}

r = requests.post(
    'https://enc-dec.app/api/enc-cinesrc',
    json=test_payload,
    timeout=30
)
print(f"enc-cinesrc POST: {r.status_code}")
print(r.text[:500])
