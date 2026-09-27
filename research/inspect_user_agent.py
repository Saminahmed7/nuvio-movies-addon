import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct
from disasm_moviebox_helpers import methods

for mid, code_off in methods:
    if mid == 9867:
        print("code_off:", code_off)
        reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
        insns = dex[code_off+16:code_off+16+insns_sz*2]
        for i in range(0, len(insns), 2):
            op = insns[i]
            reg = insns[i+1]
            if op == 0x1a:
                s_idx = struct.unpack_from('<H', insns, i+2)[0]
                print(f'str: "{get_string(s_idx)}"')
            elif op == 0x62:
                fid = struct.unpack_from('<H', insns, i+2)[0]
                print(f'sget field #{fid}')
