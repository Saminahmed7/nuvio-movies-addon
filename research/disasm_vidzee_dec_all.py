import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1866956
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"decryptVidzeeUrl insns_sz: {insns_sz}, reg_sz: {reg_sz}, ins_sz: {ins_sz}")
i = 0
while i < len(insns):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    extra = ""
    step = 2
    if op in (0x1a, 0x1c, 0x1f, 0x22):
        ref = struct.unpack_from('<H', insns, i+2)[0]
        step = 4
        if op == 0x1a: extra = f'const-string "{get_string(ref)}"'
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        step = 6
        extra = f"invoke {get_method(mid)}"
    elif op == 0x12:
        val = (reg >> 4) & 0xf
        r = reg & 0xf
        if val & 8: val = val - 16
        extra = f"const/4 v{r}, {val}"
    print(f"  {addr:04x} [op={op:02x}] {extra}")
    i += step
