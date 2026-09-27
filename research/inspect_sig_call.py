import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1513248
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Let's inspect instructions 0060 to 0088
for i in range(0x0060 * 2, 0x0088 * 2, 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    raw = ' '.join(f'{b:02x}' for b in insns[i:i+6])
    print(f"{addr:04x}: op={op:02x} r={reg:02x} raw={raw}")
