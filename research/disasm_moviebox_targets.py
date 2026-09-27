import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
from parse_dex_methods import class_defs_size, class_defs_off, get_type
import struct

target_mids = [9867, 9885, 9911, 9913, 9923, 10117, 9904]

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
            if mid in target_mids:
                mname = get_method(mid)
                print(f"\n==========================================")
                print(f"Method #{mid}: {mname} at {code_off}")
                print(f"==========================================")
                if code_off == 0:
                    continue
                reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                insns = dex[code_off+16:code_off+16+insns_sz*2]
                print(f"reg_sz={reg_sz}, ins_sz={ins_sz}, insns_sz={insns_sz}")
                i = 0
                while i < len(insns):
                    w = struct.unpack_from('<H', insns, i)[0]
                    op = w & 0xff
                    reg = (w >> 8) & 0xff
                    addr = i // 2
                    step = 2
                    extra = ""
                    if op in (0x1a, 0x1c, 0x1f, 0x22):
                        ref = struct.unpack_from('<H', insns, i+2)[0]
                        step = 4
                        if op == 0x1a:
                            try: extra = f'const-string "{get_string(ref)}"'
                            except: pass
                        elif op == 0x22:
                            try: extra = f"new-instance {get_type(ref)}"
                            except: pass
                    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
                        mid_ref = struct.unpack_from('<H', insns, i+2)[0]
                        step = 6
                        try: extra = f"invoke {get_method(mid_ref)}"
                        except: pass
                    elif op in (0x74, 0x75, 0x76, 0x77, 0x78):
                        mid_ref = struct.unpack_from('<H', insns, i+2)[0]
                        step = 6
                        try: extra = f"invoke/range {get_method(mid_ref)}"
                        except: pass
                    elif op == 0x12:
                        val = (reg >> 4) & 0xf
                        r = reg & 0xf
                        if val & 8: val = val - 16
                        extra = f"const/4 v{r}, {val}"
                    elif op == 0x13:
                        val = struct.unpack_from('<h', insns, i+2)[0]
                        step = 4
                        extra = f"const/16 v{reg}, {val}"
                    elif op in (0x54, 0x62):
                        fid = struct.unpack_from('<H', insns, i+2)[0]
                        step = 4
                        extra = f"field #{fid}"
                    print(f"  {addr:04x}: [op={op:02x} r={reg:02x}] {extra}")
                    i += step
