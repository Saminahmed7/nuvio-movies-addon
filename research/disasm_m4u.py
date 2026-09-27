import zipfile, struct

z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')

string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)

def get_string(idx):
    if idx >= string_ids_size: return f"str({idx})"
    off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    length = 0; shift = 0; p = off
    while True:
        b = dex[p]; p += 1
        length |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return dex[p:p+length].decode('utf-8', errors='ignore')

def get_type(idx):
    return get_string(struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0])

def get_method(idx):
    class_idx, proto_idx, name_idx = struct.unpack_from('<HHI', dex, method_ids_off + idx * 8)
    return f"{get_type(class_idx)}->{get_string(name_idx)}"

for c_idx in range(class_defs_size):
    class_type_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + c_idx * 32)
    cname = get_type(class_type_idx)
    if cname == 'Lcom/phisher98/StreamPlayExtractor;':
        class Cursor:
            def __init__(self, pos): self.p = pos
            def read_uleb(self):
                res = 0; shift = 0
                while True:
                    b = dex[self.p]; self.p += 1
                    res |= (b & 0x7f) << shift
                    if not (b & 0x80): break
                    shift += 7
                return res
        
        cur = Cursor(class_data_off)
        sf_size = cur.read_uleb(); if_size = cur.read_uleb()
        dm_size = cur.read_uleb(); vm_size = cur.read_uleb()
        for _ in range(sf_size): cur.read_uleb(); cur.read_uleb()
        for _ in range(if_size): cur.read_uleb(); cur.read_uleb()
        
        for is_vm, count in [(False, dm_size), (True, vm_size)]:
            cur_mid = 0
            for _ in range(count):
                mid_delta = cur.read_uleb(); cur_mid += mid_delta
                flags = cur.read_uleb(); code_off = cur.read_uleb()
                mname = get_method(cur_mid)
                if 'm4uhd' in mname.lower():
                    print(f"\nMethod {mname}: code_off={code_off}")
                    if code_off:
                        reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                        insns = dex[code_off+16:code_off+16+insns_sz*2]
                        for i in range(0, len(insns), 2):
                            op = insns[i]
                            if op == 0x1a:
                                s_idx = struct.unpack_from('<H', insns, i+2)[0]
                                print(f"  const-string: \"{get_string(s_idx)}\"")
                            elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                                mid = struct.unpack_from('<H', insns, i+2)[0]
                                m = get_method(mid)
                                if any(t in m for t in ['get', 'post', 'Regex', 'search', 'find', 'replace']):
                                    print(f"  invoke: {m}")
