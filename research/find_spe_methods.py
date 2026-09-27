import sys
sys.stdout.reconfigure(encoding='utf-8')
import zipfile, struct

z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')

string_ids_size, string_ids_off, type_ids_size, type_ids_off, proto_ids_size, proto_ids_off, field_ids_size, field_ids_off, method_ids_size, method_ids_off, class_defs_size, class_defs_off = struct.unpack_from('<IIIIIIIIIIII', dex, 0x38)

def get_string(idx):
    off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    p = off
    while dex[p] & 0x80: p += 1
    p += 1
    end = dex.find(b'\x00', p)
    return dex[p:end].decode('utf-8', errors='ignore')

def get_type(idx):
    desc_idx = struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0]
    return get_string(desc_idx)

def get_method(idx):
    c_idx, p_idx, n_idx = struct.unpack_from('<HHI', dex, method_ids_off + idx * 8)
    return f"{get_type(c_idx)}->{get_string(n_idx)}"

for mid in range(method_ids_size):
    m = get_method(mid)
    if 'StreamPlayExtractor' in m and any(k in m.lower() for k in ['fast', 'link', 'rive', 'vadapav', 'vegamovies']):
        print(f"Method #{mid}: {m}")
