import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct
from precise_disasm import OP_LENGTHS

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Find any write to v1
i = 0
while i < len(insns):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    length = OP_LENGTHS.get(op, 1)
    
    if op in (0x07, 0x01, 0x12) and (reg & 0xf) == 1:
        print(f"addr 0x{addr:04x}: op=0x{op:02x} move to v1 from v{reg>>4}")
    elif op in (0x08, 0x02, 0x13, 0x1a, 0x0c) and reg == 1:
        src = struct.unpack_from('<H', insns, i+2)[0] if op in (0x08, 0x02) else "N/A"
        print(f"addr 0x{addr:04x}: op=0x{op:02x} write to v1 (src={src})")
    i += length * 2
