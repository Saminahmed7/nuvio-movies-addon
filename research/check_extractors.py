import requests
import re

url = 'https://raw.githubusercontent.com/SaurabhKaperwan/CSX/master/Bollyflix/src/main/kotlin/com/megix/Extractors.kt'
r = requests.get(url, timeout=10)
if r.status_code == 200:
    text = r.text
    classes = re.findall(r'(open\s+)?class\s+(\w+)\s*:\s*ExtractorApi', text)
    for c in classes:
        print(f'Extractor: {c[1]}')
    
    urls = re.findall(r'mainUrl\s*=\s*"([^"]+)"', text)
    for u in urls:
        print(f'  mainUrl: {u}')
else:
    print(f'Extractors: {r.status_code}')