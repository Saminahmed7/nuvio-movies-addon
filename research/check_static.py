import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, method_ids_off, get_type, get_string
import struct

for mid in [9885, 9913, 9914]:
    c_idx, p_idx, n_idx = struct.unpack_from('<HHI', dex, method_ids_off + mid * 8)
    print(f"Method #{mid}: {get_type(c_idx)}->{get_string(n_idx)}")
