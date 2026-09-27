import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Let's inspect instructions 0108 to 0142
i = 0x0108 * 2
while i < 0x0145 * 2:
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    raw = ' '.join(f'{b:02x}' for b in insns[i:i+4])
    print(f"{addr:04x}: op={op:02x} r={reg:02x} raw={raw}")
    step = 2
    if op in (0x1a, 0x13, 0x02, 0x05, 0x08, 0x22, 0x54, 0x62, 0x59, 0x69, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d):
        step = 4
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72, 0x74, 0x75, 0x76, 0x77, 0x78):
        step = 6
    i += step
