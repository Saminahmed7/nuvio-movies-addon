import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Let's inspect instructions from 0135 to 015a
i = 0x0135 * 2
while i < 0x015a * 2:
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    step = 2
    extra = f"op=0x{op:02x} r={reg}"
    if op == 0x01: # move
        extra = f"move v{reg&0xf}, v{reg>>4}"
    elif op == 0x02: # move/from16
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        extra = f"move/from16 v{reg}, v{src}"
    elif op == 0x04: # move-wide
        extra = f"move-wide v{reg&0xf}, v{reg>>4}"
    elif op == 0x05: # move-wide/from16
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        extra = f"move-wide/from16 v{reg}, v{src}"
    elif op == 0x07: # move-object
        extra = f"move-object v{reg&0xf}, v{reg>>4}"
    elif op == 0x08: # move-object/from16
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        extra = f"move-object/from16 v{reg}, v{src}"
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]; step = 6
        extra = f"invoke {get_method(mid)}"
    elif op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        extra = f'const-string "{get_string(s_idx)}"'
    print(f"  {addr:04x}: {extra}")
    i += step
