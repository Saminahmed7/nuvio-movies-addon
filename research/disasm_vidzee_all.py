import zipfile, struct
z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')
import sys
sys.path.insert(0, 'research')
from parse_dex_methods import get_string, get_type, get_method, class_defs_size, class_defs_off

for c_idx in range(class_defs_size):
    class_type_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + c_idx * 32)
    cname = get_type(class_type_idx)
    if 'StreamPlayExtractor' in cname and 'Vidzee' in cname:
        print(f"Class: {cname}, class_data_off: {class_data_off}")
        if class_data_off == 0: continue
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
        sf_size = cur.read_uleb()
        if_size = cur.read_uleb()
        dm_size = cur.read_uleb()
        vm_size = cur.read_uleb()
        for _ in range(sf_size): cur.read_uleb(); cur.read_uleb()
        for _ in range(if_size): cur.read_uleb(); cur.read_uleb()
        
        cur_mid = 0
        for _ in range(dm_size):
            cur_mid += cur.read_uleb()
            cur.read_uleb()
            code_off = cur.read_uleb()
            mname = get_method(cur_mid)
            if code_off > 0:
                print(f"  DM {mname} at {code_off}")
                # print strings
                reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                insns = dex[code_off+16:code_off+16+insns_sz*2]
                for i in range(0, len(insns), 2):
                    op = insns[i]
                    reg = insns[i+1]
                    if op == 0x1a:
                        s_idx = struct.unpack_from('<H', insns, i+2)[0]
                        try: print(f"    str: \"{get_string(s_idx)}\"")
                        except: pass
                    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                        mid = struct.unpack_from('<H', insns, i+2)[0]
                        try:
                            m = get_method(mid)
                            if any(x in m[1] for x in ['get', 'post', 'url', 'Url', 'decrypt', 'Vidzee', 'Key']):
                                print(f"    call: {m[0]}->{m[1]}")
                        except: pass

        cur_mid = 0
        for _ in range(vm_size):
            cur_mid += cur.read_uleb()
            cur.read_uleb()
            code_off = cur.read_uleb()
            mname = get_method(cur_mid)
            if code_off > 0:
                print(f"  VM {mname} at {code_off}")
                reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                insns = dex[code_off+16:code_off+16+insns_sz*2]
                for i in range(0, len(insns), 2):
                    op = insns[i]
                    reg = insns[i+1]
                    if op == 0x1a:
                        s_idx = struct.unpack_from('<H', insns, i+2)[0]
                        try: print(f"    str: \"{get_string(s_idx)}\"")
                        except: pass
                    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                        mid = struct.unpack_from('<H', insns, i+2)[0]
                        try:
                            m = get_method(mid)
                            if any(x in m[1] for x in ['get', 'post', 'url', 'Url', 'decrypt', 'Vidzee', 'Key']):
                                print(f"    call: {m[0]}->{m[1]}")
                        except: pass
