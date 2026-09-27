import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1875132
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]
for i in range(0, len(insns), 2):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    if op in (0x59, 0x69, 0x54, 0x62):
        fid = struct.unpack_from('<H', insns, i+2)[0]
        if fid in (9312, 9313, 9314, 9315, 9316):
            print(f"{addr:04x}: op={op:02x} field #{fid}")
    elif op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]
        try:
            s = get_string(s_idx)
            if any(k in s.lower() for k in ['okhttp', 'movie', 'com.', 'android', 'user', 'agent']):
                print(f"  {addr:04x}: str: \"{s[:80]}\"")
        except: pass
