import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct
from precise_disasm import OP_LENGTHS

code_off = 1532684
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

i = 0x00a8 * 2
while i < 0x0130 * 2:
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    length = OP_LENGTHS.get(op, 1)
    
    desc = f"op=0x{op:02x}"
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        desc = f'const-string v{reg}, "{get_string(s_idx)}"'
    elif op == 0x08:
        src = struct.unpack_from('<H', insns, i+2)[0]
        desc = f"move-object/from16 v{reg}, v{src}"
    elif op == 0x07: desc = f"move-object v{reg&0xf}, v{reg>>4}"
    elif op == 0x0c: desc = f"move-result-object v{reg}"
    elif op == 0x13:
        v = struct.unpack_from('<h', insns, i+2)[0]
        desc = f"const/16 v{reg}, {v}"
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        args = struct.unpack_from('<H', insns, i+4)[0]
        cnt = reg >> 4
        r_list = [f"v{(args >> (4*k)) & 0xf}" for k in range(cnt)]
        desc = f"invoke {get_method(mid)} ({', '.join(r_list)})"
    elif op in (0x74, 0x75, 0x76, 0x77, 0x78):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        start = struct.unpack_from('<H', insns, i+4)[0]
        r_list = [f"v{start+k}" for k in range(reg)]
        desc = f"invoke/range {get_method(mid)} ({', '.join(r_list)})"
    
    print(f"  {addr:04x}: {desc}")
    i += length * 2
