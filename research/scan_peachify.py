import sys; sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1780624
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print('Total instructions words:', insns_sz)

i = 0
while i < len(insns):
    op = insns[i]
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        s = get_string(s_idx)
        print(f"{i//2:04x}: \"{s}\"")
        i += 4
    elif op == 0x1b:
        s_idx = struct.unpack_from('<I', insns, i+2)[0]
        s = get_string(s_idx)
        print(f"{i//2:04x}: jumbo \"{s}\"")
        i += 6
    else:
        i += 2
