import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Search for any write to v6 or v2
for i in range(0, len(insns), 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    if op in (0x07, 0x08, 0x01, 0x02, 0x0c, 0x1a, 0x12, 0x13):
        # writes to reg
        dest = reg & 0xf if op in (0x01, 0x07, 0x12) else reg
        if dest in (2, 6) and addr > 0x0100:
            src = struct.unpack_from('<H', insns, i+2)[0] if op in (0x02, 0x08) else "N/A"
            print(f"addr 0x{addr:04x}: op=0x{op:02x} dest=v{dest} src={src}")
