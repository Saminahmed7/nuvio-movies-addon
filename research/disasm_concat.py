import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Let's inspect instructions from 0130 to 0198
for i in range(0x0130 * 2, 0x019b * 2, 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    raw = ' '.join(f'{b:02x}' for b in insns[i:i+6])
    extra = ""
    if op == 0x07: # move-object
        extra = f"move-object v{reg&0xf}, v{reg>>4}"
    elif op == 0x08: # move-object/from16
        src = struct.unpack_from('<H', insns, i+2)[0]
        extra = f"move-object/from16 v{reg}, v{src}"
    elif op == 0x01: # move
        extra = f"move v{reg&0xf}, v{reg>>4}"
    elif op == 0x02: # move/from16
        src = struct.unpack_from('<H', insns, i+2)[0]
        extra = f"move/from16 v{reg}, v{src}"
    elif op == 0x04: # move-wide
        extra = f"move-wide v{reg&0xf}, v{reg>>4}"
    elif op == 0x0c: # move-result-object
        extra = f"move-result-object v{reg}"
    elif op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        try: extra = f'const-string v{reg}, "{get_string(s_idx)}"'
        except: pass
    elif op in (0x6e, 0x6f):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        args = struct.unpack_from('<H', insns, i+4)[0]
        count = reg >> 4
        m = get_method(mid)
        r_list = [f"v{(args >> (4*k)) & 0xf}" for k in range(count)]
        extra = f"invoke {m} ({', '.join(r_list)})"
    elif op in (0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        extra = f"invoke {get_method(mid)}"
    print(f"{addr:04x}: {extra} [{raw}]")
