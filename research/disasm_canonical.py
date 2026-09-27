import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"buildMovieBoxCanonicalString insns_sz={insns_sz}, reg_sz={reg_sz}")
i = 0x0150 * 2
while i < len(insns):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    step = 2
    extra = ""
    if op in (0x1a, 0x1c, 0x1f, 0x22):
        ref = struct.unpack_from('<H', insns, i+2)[0]
        step = 4
        if op == 0x1a:
            try: extra = f'"{get_string(ref)}"'
            except: pass
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid_ref = struct.unpack_from('<H', insns, i+2)[0]
        step = 6
        try: extra = f"invoke {get_method(mid_ref)}"
        except: pass
    elif op in (0x74, 0x75, 0x76, 0x77, 0x78):
        mid_ref = struct.unpack_from('<H', insns, i+2)[0]
        step = 6
        try: extra = f"invoke/range {get_method(mid_ref)}"
        except: pass
    elif op == 0x12:
        val = (reg >> 4) & 0xf
        r = reg & 0xf
        if val & 8: val = val - 16
        extra = f"const/4 v{r}, {val}"
    elif op in (0x54, 0x62):
        fid = struct.unpack_from('<H', insns, i+2)[0]
        step = 4
        extra = f"field #{fid}"
    print(f"  {addr:04x}: [op={op:02x} r={reg:02x}] {extra}")
    i += step
