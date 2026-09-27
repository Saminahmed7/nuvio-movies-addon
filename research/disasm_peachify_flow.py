import sys; sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1780624
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
for i in range(0, min(len(insns), 600), 2):
    op = insns[i]
    reg = insns[i+1]
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        print(f"{i//2:04x}: const-string: \"{get_string(s_idx)}\"")
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        m = get_method(mid)
        if any(t in m for t in ['get', 'post', 'Regex', 'search', 'find', 'replace', 'peachify', 'url', 'Url']):
            print(f"{i//2:04x}: invoke: {m}")
