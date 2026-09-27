import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1513248
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Let's inspect instructions 0060 to 0087
i = 0x0060 * 2
while i < 0x0088 * 2:
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    step = 2
    desc = f"op=0x{op:02x} r={reg}"
    if op == 0x01: desc = f"move v{reg&0xf}, v{reg>>4}"
    elif op == 0x02:
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        desc = f"move/from16 v{reg}, v{src}"
    elif op == 0x07: desc = f"move-object v{reg&0xf}, v{reg>>4}"
    elif op == 0x08:
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        desc = f"move-object/from16 v{reg}, v{src}"
    elif op == 0x0c: desc = f"move-result-object v{reg}"
    elif op == 0x12:
        v = (reg >> 4) & 0xf; r = reg & 0xf
        if v & 8: v -= 16
        desc = f"const/4 v{r}, {v}"
    elif op == 0x13:
        v = struct.unpack_from('<h', insns, i+2)[0]; step = 4
        desc = f"const/16 v{reg}, {v}"
    elif op in (0x70, 0x71):
        mid = struct.unpack_from('<H', insns, i+2)[0]; step = 6
        desc = f"invoke {get_method(mid)}"
    elif op == 0x77:
        mid = struct.unpack_from('<H', insns, i+2)[0]
        start = struct.unpack_from('<H', insns, i+4)[0]; step = 6
        r_list = [f"v{start+k}" for k in range(reg)]
        desc = f"invoke/range {get_method(mid)} ({', '.join(r_list)})"
    print(f"  {addr:04x}: {desc}")
    i += step
