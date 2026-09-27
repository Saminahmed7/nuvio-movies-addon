import re

with open('research/cinesrc_main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for the gc() function and how it composes the full challenge token  
# We already know: return e+"::c2::"+t+"::c3::"+d
# where e = d6.gc() = stage1 result from 300726c-prod.js
#       t = window.__ss2_challenge.gc() = stage2 result
#       d = x-cs-r (session token from bootstrap)

# Let's look at d6.gc()  
print("=== d6 context ===")
for m in re.finditer(r'.{0,100}d6.{0,400}', text):
    ctx = m.group(0)
    if 'gc' in ctx or 'challenge' in ctx.lower():
        print(ctx[:400])
        print("---")
        break

# Look for how the final challenge token is used to call /api/c/issue
print("\n=== issue call with full challenge token ===")
for m in re.finditer(r'.{0,200}Next-Action|api/c/issue.{0,400}', text):
    print(m.group(0)[:400])
    print("---")

# Look for the stage2 challenge  
print("\n=== __ss2_challenge context ===")
for m in re.finditer(r'.{0,50}__ss2_challenge.{0,300}', text):
    print(m.group(0)[:300])
    print("---")
