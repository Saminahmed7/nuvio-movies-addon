import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_string, get_method
import struct

code_off = 1865032
reg_sz, ins_sz, out_sz, tri_sz, dbg_off, insns_sz = struct.unpack_from('<HHHHII', dex, code_off)
insns = dex[code_off+16:code_off+16+insns_sz*2]

# Method signature:
# buildMovieBoxCanonicalString(url: String, method: String, contentType: String, body: String, clientToken: String, timestamp: Long)
# reg_sz = 36, ins_sz = 8
# v28: this
# v29: url
# v30: method
# v31: contentType
# v32: body
# v33: clientToken
# v34, v35: timestamp (Long)

print("Disassembling buildMovieBoxCanonicalString:")
i = 0
while i < len(insns):
    w = struct.unpack_from('<H', insns, i)[0]
    op = w & 0xff
    reg = (w >> 8) & 0xff
    addr = i // 2
    step = 2
    desc = f"op=0x{op:02x}"
    
    if op == 0x01: desc = f"move v{reg&0xf}, v{reg>>4}"
    elif op == 0x02:
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        desc = f"move/from16 v{reg}, v{src}"
    elif op == 0x04: desc = f"move-wide v{reg&0xf}, v{reg>>4}"
    elif op == 0x05:
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        desc = f"move-wide/from16 v{reg}, v{src}"
    elif op == 0x07: desc = f"move-object v{reg&0xf}, v{reg>>4}"
    elif op == 0x08:
        src = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        desc = f"move-object/from16 v{reg}, v{src}"
    elif op == 0x0a: desc = f"move-result v{reg}"
    elif op == 0x0b: desc = f"move-result-wide v{reg}"
    elif op == 0x0c: desc = f"move-result-object v{reg}"
    elif op == 0x0e: desc = "return-void"
    elif op == 0x0f: desc = f"return v{reg}"
    elif op == 0x11: desc = f"return-object v{reg}"
    elif op == 0x12:
        v = (reg >> 4) & 0xf
        r = reg & 0xf
        if v & 8: v -= 16
        desc = f"const/4 v{r}, {v}"
    elif op == 0x13:
        v = struct.unpack_from('<h', insns, i+2)[0]; step = 4
        desc = f"const/16 v{reg}, {v}"
    elif op == 0x1a:
        s_idx = struct.unpack_from('<H', insns, i+2)[0]; step = 4
        try: desc = f'const-string v{reg}, "{get_string(s_idx)}"'
        except: desc = f"const-string v{reg}, str#{s_idx}"
    elif op in (0x28, 0x29):
        off = struct.unpack_from('<b', insns, i+1)[0] if op == 0x28 else struct.unpack_from('<h', insns, i+2)[0]
        step = 2 if op == 0x28 else 4
        desc = f"goto 0x{addr + off:04x}"
    elif 0x32 <= op <= 0x37:
        r1 = reg & 0xf; r2 = (reg >> 4) & 0xf
        off = struct.unpack_from('<h', insns, i+2)[0]; step = 4
        desc = f"if-cmp v{r1}, v{r2}, 0x{addr + off:04x}"
    elif 0x38 <= op <= 0x3d:
        off = struct.unpack_from('<h', insns, i+2)[0]; step = 4
        desc = f"if-test v{reg}, 0x{addr + off:04x}"
    elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        args = struct.unpack_from('<H', insns, i+4)[0]; step = 6
        cnt = reg >> 4
        r_list = [f"v{(args >> (4*k)) & 0xf}" for k in range(cnt)]
        try: desc = f"invoke {get_method(mid)} ({', '.join(r_list)})"
        except: desc = f"invoke mid#{mid}"
    elif op in (0x74, 0x75, 0x76, 0x77, 0x78):
        mid = struct.unpack_from('<H', insns, i+2)[0]
        start = struct.unpack_from('<H', insns, i+4)[0]; step = 6
        r_list = [f"v{start+k}" for k in range(reg)]
        try: desc = f"invoke/range {get_method(mid)} ({', '.join(r_list)})"
        except: desc = f"invoke/range mid#{mid}"
    
    print(f"  {addr:04x}: {desc}")
    i += step
