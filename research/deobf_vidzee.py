import base64
import urllib.parse

# 1. Extract array
with open("research/vidzee_player_component.js", "r", encoding="utf-8") as f:
    code = f.read()

# Let's extract the array elements from _0x4d2b
import re
m_arr = re.search(r'function _0x4d2b\(\)\{const _0x5cb19f=(\[.*?\]);_0x4d2b=', code)
arr = eval(m_arr.group(1))

# Now the rotation loop:
# (function(_0x445fb7,_0x23ca83){ ... }(_0x4d2b, 0x11*-0x16fe+-0xe5*-0x41+-0x3918b*-0x1))
# Target value:
target = 0x11 * -0x16fe + -0xe5 * -0x41 + -0x3918b * -0x1
print("Target:", target)

def b64_rc4_decode(s, key):
    # JavaScript b64 decode with custom chars
    table = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
    raw_b64 = base64.b64decode(s)
    # RC4
    sbox = list(range(256))
    j = 0
    key_bytes = key.encode('utf-8')
    for i in range(256):
        j = (j + sbox[i] + key_bytes[i % len(key_bytes)]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
    
    i = 0
    j = 0
    res = []
    for b in raw_b64:
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        res.append(b ^ sbox[(sbox[i] + sbox[j]) % 256])
    return bytes(res).decode('utf-8', errors='ignore')

def make_getter(arr):
    cache = {}
    def get_str(idx, key):
        real_idx = idx - (0x1b25 + 0x1997 - 0x330f)
        cache_key = f"{real_idx}_{key}"
        if cache_key in cache:
            return cache[cache_key]
        val = arr[real_idx]
        dec = b64_rc4_decode(val, key)
        cache[cache_key] = dec
        return dec
    return get_str

# Test rotation
# The rotation loop calculates an integer expression and shifts arr
# Let's rotate until match
getter = make_getter(arr)
def a93f44(a, b):
    return getter(a - -0x36f, b)

while True:
    try:
        val = int(a93f44(-0x11e,'YQLY')) // (-0x665*0x5+-0xb*0x25f+-0xa7*-0x59) \
            + -int(a93f44(-0x18f,'Fm9p')) // (-0xcac+0x17*0x95+-0xb5) * (-int(a93f44(-0xfc,'r5)D')) // (-0x1a94+-0xa8b*0x2+0x2fad)) \
            + int(a93f44(-0x19a,'ifua')) // (-0xfcf*0x2+-0x13b8+-0x335a*-0x1) \
            + -int(a93f44(-0x1ab,'ygwE')) // (0x7*-0x515+0x860*0x4+0x10c*0x2) \
            + -int(a93f44(-0x161,'Q9gG')) // (-0x19f2+0xc67+0x17*0x97) * (int(a93f44(-0x116,'x8RK')) // (0x1db7+-0x6f*0x49+0x1f7)) \
            + int(a93f44(-0x17a,'th5#')) // (-0x1b50+0x1e10*-0x1+-0x2*-0x1cb4) * (-int(a93f44(-0x77,'EQJp')) // (0x14*0x1f+-0x2404+0x1*0x21a1)) \
            + -int(a93f44(-0x162,'ncEk')) // (-0x2610+-0x1601+0x3*0x1409) * (-int(a93f44(-0x1ac,'5r4V')) // (-0x1556*-0x1+0xfe+0x475*-0x5))
        if val == target:
            print("Successfully rotated array!")
            break
        else:
            arr.append(arr.pop(0))
    except Exception:
        arr.append(arr.pop(0))

# Now decode re and I:
# const re=_0x4099ec(-0x13e,'ygwE'),I=_0x4099ec(-0x2b,'a9$z');
# function _0x4099ec(_0x2bf3c4,_0x488e97){return _0x3103(_0x2bf3c4- -0x32f,_0x488e97);}
def _0x4099ec(a, b):
    return getter(a - -0x32f, b)

re_val = _0x4099ec(-0x13e, 'ygwE')
I_val = _0x4099ec(-0x2b, 'a9$z')
print("re:", re_val)
print("I:", I_val)
