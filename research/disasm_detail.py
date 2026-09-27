import sys
sys.path.insert(0, 'research')
from disasm_xpass import insns, get_string, get_method
import struct

def disasm_range(start_word, end_word):
    i = start_word * 2
    while i < end_word * 2:
        op = insns[i]
        reg = insns[i+1]
        addr = i // 2
        if op == 0x1a:
            s_idx = struct.unpack_from('<H', insns, i+2)[0]
            print(f"{addr:04x}: const-string v{reg}, \"{get_string(s_idx)}\"")
            i += 4
        elif op == 0x1b:
            s_idx = struct.unpack_from('<I', insns, i+2)[0]
            print(f"{addr:04x}: const-string/jumbo v{reg}, \"{get_string(s_idx)}\"")
            i += 6
        elif op == 0x0c:
            src = insns[i+1] # move-result
            print(f"{addr:04x}: move-result v{src}")
            i += 2
        elif op == 0x0d:
            src = insns[i+1] # move-result-object
            print(f"{addr:04x}: move-result-object v{src}")
            i += 2
        elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
            count = reg >> 4
            mreg = reg & 0x0f
            mid = struct.unpack_from('<H', insns, i+2)[0]
            regs = []
            if count > 0:
                r1 = insns[i+4]
                r2 = insns[i+5]
                # decode args
                regs = [r1 & 0xf, (r1 >> 4) & 0xf, r2 & 0xf, (r2 >> 4) & 0xf][:count]
            print(f"{addr:04x}: invoke-{op:02x} {regs} {get_method(mid)}")
            i += 6
        elif op in (0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59):
            fld = struct.unpack_from('<H', insns, i+2)[0]
            print(f"{addr:04x}: iget/iput op={op:02x} v{reg&0xf}, v{(reg>>4)&0xf} fld={fld}")
            i += 4
        elif op == 0x22:
            tid = struct.unpack_from('<H', insns, i+2)[0]
            print(f"{addr:04x}: new-instance v{reg}")
            i += 4
        else:
            w = struct.unpack_from('<H', insns, i)[0]
            print(f"{addr:04x}: {op:02x} (word={w:04x})")
            i += 2

disasm_range(0x0060, 0x00d0)
