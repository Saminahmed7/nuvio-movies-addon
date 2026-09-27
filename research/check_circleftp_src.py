import requests

# Check src directory
url = 'https://api.github.com/repos/redowan99/Redowan-CloudStream/contents/BdixCircleftp/src'
r = requests.get(url, timeout=10)
items = r.json()
for item in items:
    print(f"{item['type']}: {item['name']}")