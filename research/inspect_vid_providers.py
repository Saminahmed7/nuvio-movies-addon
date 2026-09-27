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
        sf_size = cur.read_uleb(); if_size = cur.read_uleb(); dm_size = cur.read_uleb(); vm_size = cur.read_uleb()
        for _ in range(sf_size): cur.read_uleb(); cur.read_uleb()
        for _ in range(if_size): cur.read_uleb(); cur.read_uleb()
        
        methods = []
        cur_mid = 0
        for _ in range(dm_size):
            cur_mid += cur.read_uleb(); cur.read_uleb(); code_off = cur.read_uleb()
            methods.append((cur_mid, code_off))
        cur_mid = 0
        for _ in range(vm_size):
            cur_mid += cur.read_uleb(); cur.read_uleb(); code_off = cur.read_uleb()
            methods.append((cur_mid, code_off))

        for mid, code_off in methods:
            mname = get_method(mid)
            if 'invokevidfast' in mname.lower() or 'invokevidlink' in mname.lower() or 'invokerivestream' in mname.lower():
                print(f"\n==========================================")
                print(f"Method #{mid}: {mname} at {code_off}")
                print(f"==========================================")
                if code_off == 0: continue
                reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                insns = dex[code_off+16:code_off+16+insns_sz*2]
                for i in range(0, len(insns), 2):
                    op = insns[i]
                    if op == 0x1a:
                        s_idx = struct.unpack_from('<H', insns, i+2)[0]
                        try: print(f"  str: \"{get_string(s_idx)}\"")
                        except: pass
                    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                        mid_ref = struct.unpack_from('<H', insns, i+2)[0]
                        try:
                            m = get_method(mid_ref)
                            if not any(k in m for k in ['Intrinsics', 'Boxing', 'Spilling']):
                                print(f"  call: {m}")
                        except: pass
