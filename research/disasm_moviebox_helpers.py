import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
from parse_dex_methods import class_defs_size, class_defs_off, get_type
import struct

target_methods = [
    'buildMovieBoxCanonicalString',
    'buildMovieBoxHeaders',
    'getMovieBoxToken',
    'persistMovieBoxTokenFromXUser',
    'getMovieBoxHighestQuality'
]

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
        sf_size = cur.read_uleb()
        if_size = cur.read_uleb()
        dm_size = cur.read_uleb()
        vm_size = cur.read_uleb()
        for _ in range(sf_size): cur.read_uleb(); cur.read_uleb()
        for _ in range(if_size): cur.read_uleb(); cur.read_uleb()
        
        methods = []
        cur_mid = 0
        for _ in range(dm_size):
            cur_mid += cur.read_uleb()
            cur.read_uleb()
            code_off = cur.read_uleb()
            methods.append((cur_mid, code_off))
        cur_mid = 0
        for _ in range(vm_size):
            cur_mid += cur.read_uleb()
            cur.read_uleb()
            code_off = cur.read_uleb()
            methods.append((cur_mid, code_off))

        for mid, code_off in methods:
            mname = get_method(mid)
            for tm in target_methods:
                if tm in mname:
                    print(f"\n==========================================")
                    print(f"Method: {mname} at {code_off}")
                    print(f"==========================================")
                    if code_off == 0:
                        continue
                    reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                    insns = dex[code_off+16:code_off+16+insns_sz*2]
                    for i in range(0, len(insns), 2):
                        op = insns[i]
                        reg = insns[i+1]
                        addr = i // 2
                        if op == 0x1a:
                            s_idx = struct.unpack_from('<H', insns, i+2)[0]
                            try: print(f"  {addr:04x}: const-string v{reg}, \"{get_string(s_idx)}\"")
                            except: pass
                        elif op == 0x1b:
                            s_idx = struct.unpack_from('<I', insns, i+2)[0]
                            try: print(f"  {addr:04x}: const-string/jumbo v{reg}, \"{get_string(s_idx)}\"")
                            except: pass
                        elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                            mid = struct.unpack_from('<H', insns, i+2)[0]
                            try:
                                m = get_method(mid)
                                print(f"  {addr:04x}: invoke {m}")
                            except: pass
                        elif op == 0x12:
                            val = (reg >> 4) & 0xf
                            r = reg & 0xf
                            if val & 8: val = val - 16
                            print(f"  {addr:04x}: const/4 v{r}, {val}")
                        elif op == 0x13:
                            val = struct.unpack_from('<h', insns, i+2)[0]
                            print(f"  {addr:04x}: const/16 v{reg}, {val}")
