import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string
import struct

code_off = 1875132
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
for i in range(0x00a0 * 2, 0x00d5 * 2, 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    addr = i // 2
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        print(f"0x{addr:04x} str: {get_string(s_idx)}")
    elif op == 0x69:
        fid = struct.unpack_from('<H', insns, i+2)[0]
        print(f"0x{addr:04x} sput field #{fid}")
