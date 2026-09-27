import sys; sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)

for c_idx in range(class_defs_size):
    class_type_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + c_idx * 32)
    cname = get_string(struct.unpack_from('<I', dex, type_ids_off + class_type_idx * 4)[0])
    if 'PeachifyServer' in cname and class_data_off:
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
        sf = cur.read_uleb(); inf = cur.read_uleb(); dm = cur.read_uleb(); vm = cur.read_uleb()
        for _ in range(sf): cur.read_uleb(); cur.read_uleb()
        for _ in range(inf): cur.read_uleb(); cur.read_uleb()
        cur_mid = 0
        for _ in range(dm + vm):
            mid_delta = cur.read_uleb(); cur_mid += mid_delta
            flags = cur.read_uleb(); code_off = cur.read_uleb()
            mname = get_method(cur_mid)
            if code_off:
                reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
                insns = dex[code_off+16:code_off+16+insns_sz*2]
                for i in range(0, len(insns), 2):
                    if insns[i] == 0x1a:
                        s_idx = struct.unpack_from('<H', insns, i+2)[0]
                        print(f"  {mname} const-string: \"{get_string(s_idx)}\"")
