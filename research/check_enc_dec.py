import httpx
import json

r = httpx.get('https://enc-dec.app', timeout=5.0)
idx1 = r.text.find('<script id="data-json"')
idx1 = r.text.find('>', idx1) + 1
idx2 = r.text.find('</script>', idx1)
d = json.loads(r.text[idx1:idx2])
for section, items in d.items():
    print(f"=== {section} ===")
    for item in items:
        eps = [f"{e['method']} {e['path']}" for e in item.get('endpoints', [])]
        print(f"  {item['title']}: {', '.join(eps)} ({item.get('sample')})")
