import sys; sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 2035340
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"peachifyDecrypt insns_sz: {insns_sz}, registers: {reg_sz}")

for i in range(0, len(insns), 2):
    op = insns[i]
    reg = insns[i+1]
    addr = i // 2
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        print(f"{addr:04x}: const-string v{reg}, \"{get_string(s_idx)}\"")
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        m = get_method(mid)
        print(f"{addr:04x}: invoke {m}")
    elif op == 0x12:
        val = (reg >> 4) & 0xf
        vreg = reg & 0xf
        print(f"{addr:04x}: const/4 v{vreg}, {val}")
    elif op == 0x0c:
        print(f"{addr:04x}: move-result v{reg}")
    elif op == 0x0d:
        print(f"{addr:04x}: move-result-object v{reg}")
