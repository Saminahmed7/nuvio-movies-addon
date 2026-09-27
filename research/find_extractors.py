from disasm_xpass import dex, get_string, get_method
import struct

string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
proto_ids_size, proto_ids_off = struct.unpack_from('<II', dex, 72)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)

for m_idx in range(method_ids_size):
    class_idx, proto_idx, name_idx = struct.unpack_from('<HHI', dex, method_ids_off + m_idx * 8)
    cname = get_string(struct.unpack_from('<I', dex, type_ids_off + class_idx * 4)[0])
    mname = get_string(name_idx)
    if any(target in mname for target in ['invokeGoated', 'invokeRiveStream', 'invokeM4uhd']):
        print(f"Target method: {cname}->{mname}")
