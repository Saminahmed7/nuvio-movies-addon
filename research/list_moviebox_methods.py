import sys
sys.path.insert(0, 'research')
from disasm_xpass import dex, get_method, method_ids_size

for i in range(method_ids_size):
    m = get_method(i)
    if 'moviebox' in m.lower():
        print(f"Method #{i}: {m}")
