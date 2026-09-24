import re

with open('research/movy_27205.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('api.wecollege.net')
if pos != -1:
    print(text[max(0, pos - 200): min(len(text), pos + 500)])
else:
    print("Not found in html text directly, let us check where wecollege appears")
    for m in re.finditer(r'wecollege\.net[^\s"\'\\<>]*', text):
        print(" ", m.group(0))
