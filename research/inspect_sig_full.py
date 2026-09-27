import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1868716
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"generateMovieBoxXTrSignature reg_sz={reg_sz}, ins_sz={ins_sz}")
# Parameters start at v(reg_sz - ins_sz) = v(30 - 8) = v22
# v22: this
# v23: url
# v24: method
# v25: contentType
# v26: body
# v27: clientToken
# v28: flag
# v29: timestamp (Long)

for i in range(0, 0x0020 * 2, 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    raw = ' '.join(f'{b:02x}' for b in insns[i:i+4])
    print(f"{addr:04x}: op={op:02x} r={reg:02x} raw={raw}")
