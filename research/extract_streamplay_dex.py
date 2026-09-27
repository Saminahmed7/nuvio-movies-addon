import requests, zipfile, io, re

r = requests.get('https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/builds/StreamPlay.cs3')
z = zipfile.ZipFile(io.BytesIO(r.content))
dex = z.read('classes.dex')

urls = set(re.findall(rb'https?://[a-zA-Z0-9\.\-_/]+', dex))
print(f'Total URLs found: {len(urls)}')
clean_urls = []
for u in sorted(urls):
    u_str = u.decode('utf-8', errors='ignore')
    if any(k in u_str for k in ['api', 'embed', 'stream', 'play', 'video', 'watch', 'vidsrc', 'provider']):
        print(u_str)
