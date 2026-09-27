import zipfile, struct

z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')

# DEX header parsing
magic = dex[:8]
string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
proto_ids_size, proto_ids_off = struct.unpack_from('<II', dex, 72)
field_ids_size, field_ids_off = struct.unpack_from('<II', dex, 80)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)

def get_string(idx):
    off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    # uleb128 length
    length = 0
    shift = 0
    p = off
    while True:
        b = dex[p]
        p += 1
        length |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return dex[p:p+length].decode('utf-8', errors='ignore')

def get_type(idx):
    desc_idx = struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0]
    return get_string(desc_idx)

def get_method(idx):
    class_idx, proto_idx, name_idx = struct.unpack_from('<HHI', dex, method_ids_off + idx * 8)
    return get_type(class_idx), get_string(name_idx)

print(f"Total methods: {method_ids_size}, class defs: {class_defs_size}")

# Find method idx for decryptXpassDataUrl
target_methods = []
for m_idx in range(method_ids_size):
    cname, mname = get_method(m_idx)
    if 'xpass' in mname.lower():
        target_methods.append((m_idx, cname, mname))
        print(f"Method {m_idx}: {cname}->{mname}")

# Now find class def for StreamPlayUtilsKt
for c_idx in range(class_defs_size):
    class_type_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + c_idx * 32)
    cname = get_type(class_type_idx)
    if 'StreamPlayUtilsKt' in cname:
        print(f"Found class def: {cname}, class_data_off: {class_data_off}")
        if class_data_off == 0: continue
        
        # Read class_data_item (uleb128: static_fields_size, instance_fields_size, direct_methods_size, virtual_methods_size)
        class Cursor:
            def __init__(self, pos): self.p = pos
            def read_uleb(self):
                res = 0; shift = 0
                while True:
                    b = dex[self.p]; self.p += 1
                    res |= (b & 0x7f) << shift
                    if not (b & 0x80): break
                    shift += 7
                return res
        
        cur = Cursor(class_data_off)
        sf_size = cur.read_uleb()
        if_size = cur.read_uleb()
        dm_size = cur.read_uleb()
        vm_size = cur.read_uleb()
        
        # skip fields
        for _ in range(sf_size): cur.read_uleb(); cur.read_uleb()
        for _ in range(if_size): cur.read_uleb(); cur.read_uleb()
        
        # direct methods
        cur_mid = 0
        for _ in range(dm_size):
            mid_delta = cur.read_uleb()
            cur_mid += mid_delta
            m_flags = cur.read_uleb()
            code_off = cur.read_uleb()
            _, mname = get_method(cur_mid)
            if 'xpass' in mname.lower() or 'peachify' in mname.lower() or 'vidzee' in mname.lower():
                print(f"  Direct method {cur_mid}: {mname} at code_off: {code_off}")
                if code_off > 0:
                    # dump code item
                    registers_size, ins_size, outs_size, tries_size, debug_info_off, insns_size = struct.unpack_from('<HHHHII', dex, code_off)
                    insns = dex[code_off+16 : code_off+16 + insns_size*2]
                    print(f"    insns_size: {insns_size}, raw hex: {insns[:64].hex()}")

        # virtual methods
        cur_mid = 0
        for _ in range(vm_size):
            mid_delta = cur.read_uleb()
            cur_mid += mid_delta
            m_flags = cur.read_uleb()
            code_off = cur.read_uleb()
            _, mname = get_method(cur_mid)
            if 'xpass' in mname.lower() or 'peachify' in mname.lower() or 'vidzee' in mname.lower():
                print(f"  Virtual method {cur_mid}: {mname} at code_off: {code_off}")
