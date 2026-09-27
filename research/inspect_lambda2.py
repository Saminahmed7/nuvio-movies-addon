import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1864936
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"lambda$2 insns_sz={insns_sz}")
i = 0
while i < len(insns):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    step = 2
    extra = ""
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        step = 4
        try: extra = f'"{get_string(s_idx)}"'
        except: pass
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        step = 6
        try: extra = f"invoke {get_method(mid)}"
        except: pass
    print(f"  {addr:04x}: [op={op:02x}] {extra}")
    i += step
