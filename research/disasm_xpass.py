import zipfile, struct

z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')

string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
proto_ids_size, proto_ids_off = struct.unpack_from('<II', dex, 72)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)

def get_string(idx):
    if idx >= string_ids_size: return f"str_out_of_bounds({idx})"
    off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    length = 0; shift = 0; p = off
    while True:
        b = dex[p]; p += 1
        length |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return dex[p:p+length].decode('utf-8', errors='ignore')

def get_type(idx):
    desc_idx = struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0]
    return get_string(desc_idx)

def get_method(idx):
    if idx >= method_ids_size: return f"method_out_of_bounds({idx})"
    class_idx, proto_idx, name_idx = struct.unpack_from('<HHI', dex, method_ids_off + idx * 8)
    return f"{get_type(class_idx)}->{get_string(name_idx)}"

code_off = 2002292
registers_size, ins_size, outs_size, tries_size, debug_info_off, insns_size = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16 : code_off+16 + insns_size*2]

print(f"Insns size: {insns_size} words ({len(insns)} bytes)")

# Scan 16-bit units
i = 0
while i < len(insns):
    op = insns[i]
    if op == 0x1a: # const-string
        reg = insns[i+1]
        str_idx = struct.unpack_from('<H', insns, i+2)[0]
        s = get_string(str_idx)
        print(f"{i//2:04x}: const-string v{reg}, \"{s}\"")
        i += 4
    elif op == 0x1b: # const-string/jumbo
        reg = insns[i+1]
        str_idx = struct.unpack_from('<I', insns, i+2)[0]
        s = get_string(str_idx)
        print(f"{i//2:04x}: const-string/jumbo v{reg}, \"{s}\"")
        i += 6
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72): # invoke-kind
        mid = struct.unpack_from('<H', insns, i+2)[0]
        m = get_method(mid)
        if any(term in m for term in ['Cipher', 'SecretKey', 'Base64', 'decrypt', 'byte', 'String', 'replace', 'split', 'json', 'Json']):
            print(f"{i//2:04x}: invoke {m}")
        i += 6
    elif op in (0x74, 0x75, 0x76, 0x77, 0x78): # invoke-kind/range
        mid = struct.unpack_from('<H', insns, i+2)[0]
        m = get_method(mid)
        if any(term in m for term in ['Cipher', 'SecretKey', 'Base64', 'decrypt', 'byte', 'String', 'replace', 'split', 'json', 'Json']):
            print(f"{i//2:04x}: invoke/range {m}")
        i += 6
    else:
        i += 2
