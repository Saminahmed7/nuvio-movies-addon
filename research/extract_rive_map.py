import httpx
import re

text = httpx.get('https://www.rivestream.app/_next/static/chunks/2427-f1dd7c2a4b7832e1.js').text

# Find where the domains are assigned to variables
# e.g., a="https://...", o="https://..."
assignments = re.findall(r'([a-zA-Z0-9_]+)\s*=\s*["\'](https?://[^"\']+)["\']', text)
print("Domain variable assignments in Rive:")
domain_map = {}
for var, dom in assignments:
    domain_map[var] = dom
    print(f"  {var} = {dom}")

# Find server array Y
print("\n--- SERVER DEFINITIONS ---")
server_blocks = re.findall(r'label:\s*["\']([^"\']+)["\'],\s*value:\s*["\']([^"\']+)["\'],\s*star:\s*(![01]),\s*category:\s*["\']([^"\']+)["\'],\s*src:\{movie:t=>\{let\{id:e[^}]*return""\.concat\(([a-zA-Z0-9_]+),["\']([^"\']*)["\']', text)

for label, val, star, cat, var, path in server_blocks:
    dom = domain_map.get(var, var)
    star_str = "⭐" if star == "!0" else "  "
    print(f"{star_str} [{val}] {label} ({cat}) -> {dom}{path}{{id}}")
