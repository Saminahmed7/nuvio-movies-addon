import re

with open('research/vidfast_27205.html', 'r', encoding='utf-8') as f:
    text = f.read()

pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*)"\]\)', text)
print(f"Total pushes: {len(pushes)}")
full_rsc = "".join(pushes)

try:
    unescaped = bytes(full_rsc, 'utf-8').decode('unicode_escape')
except Exception:
    unescaped = full_rsc

with open('research/vidfast_rsc.txt', 'w', encoding='utf-8') as f:
    f.write(unescaped)

print("Saved unescaped RSC to research/vidfast_rsc.txt (length:", len(unescaped), ")")

# Search for any URLs or servers in the unescaped text
urls = re.findall(r'https?://[^\s"\'\\<>]+', unescaped)
print("URLs in RSC:")
for u in set(urls):
    print(" ", u)
