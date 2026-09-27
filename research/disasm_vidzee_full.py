import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1833292
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"invokeVidzee insns_sz: {insns_sz}")
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
    elif op == 0x12: # const/4
        val = (reg >> 4) & 0xf
        r = reg & 0xf
        # sign extend 4-bit
        if val & 8: val = val - 16
        print(f"  {addr:04x}: const/4 v{r}, {val}")
    elif op == 0x13: # const/16
        val = struct.unpack_from('<h', insns, i+2)[0]
        print(f"  {addr:04x}: const/16 v{reg}, {val}")
