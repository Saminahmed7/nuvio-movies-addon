import requests

# Check BdixDflix source
providers = ['BdixDflix', 'BdixDhakaFlix', 'BanglaPlex', '9kMovies', 'Mp4Moviez']

for p in providers:
    url = f'https://api.github.com/repos/redowan99/Redowan-CloudStream/contents/{p}/src/main/kotlin/com/redowan'
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        items = r.json()
        print(f"\n=== {p} ===")
        for item in items:
            print(f"  {item['type']}: {item['name']}")
    else:
        print(f"\n=== {p} ===")
        print(f"  Status: {r.status_code}")