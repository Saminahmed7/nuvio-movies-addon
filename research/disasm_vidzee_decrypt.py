import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

# Let's inspect decryptVidzeeUrl at code_off 2030124
code_off = 2030124
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
print(f"decryptVidzeeUrl (size {insns_sz}):")
for i in range(0, len(insns), 2):
    op = insns[i]
    reg = insns[i+1]
    addr = i // 2
    if op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        print(f"  {addr:04x}: const-string v{reg}, \"{get_string(s_idx)}\"")
    elif op == 0x1b:
        s_idx = struct.unpack_from('<I', insns, i+2)[0]
        print(f"  {addr:04x}: const-string/jumbo v{reg}, \"{get_string(s_idx)}\"")
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        print(f"  {addr:04x}: invoke {get_method(mid)}")
    elif op == 0x54:
        # iget-object
        fid = struct.unpack_from('<H', insns, i+2)[0]
        print(f"  {addr:04x}: iget v{reg}, field#{fid}")
    elif op == 0x62:
        # sget-object
        fid = struct.unpack_from('<H', insns, i+2)[0]
        print(f"  {addr:04x}: sget v{reg}, field#{fid}")
