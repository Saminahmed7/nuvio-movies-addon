import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, proto_ids_off, method_ids_off, get_type, get_string
import struct

c_idx, p_idx, n_idx = struct.unpack_from('<HHI', dex, method_ids_off + 9887 * 8)
print('Method:', get_type(c_idx), get_string(n_idx))
shorty_idx, ret_idx, params_off = struct.unpack_from('<III', dex, proto_ids_off + p_idx * 12)
print('Shorty:', get_string(shorty_idx))
if params_off > 0:
    cnt = struct.unpack_from('<I', dex, params_off)[0]
    for i in range(cnt):
        t_idx = struct.unpack_from('<H', dex, params_off + 4 + i * 2)[0]
        print(f'Param {i}:', get_type(t_idx))
