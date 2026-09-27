import httpx

url = 'https://pengu.uk/direct/experimental/eyJ0Ijoic2VyaWVzIiwiaSI6InR0NTg3NTQ0NCIsInMiOjEsImUiOjIsImgiOiI5NDM0NDVhMGM2MDZjMWQ4NzY2NTgwZDE1YmViZGM4NmZjYWRkOGI2IiwiZiI6MH0/Slow-Horses-2022-S01E02-2160p-ATVP-WEB-DL-Hybrid-H265-DV-HDR10-DDP-Atmos-5.1-English---HONE-.mkv?psig=1790257518.ThiDGUxP3KGZ-IAKvwhmQM0NQHl5-5XOJh95bvHKDD0%3ABmnKcYOohtk8m52J9w-R_MyK3aLIlVwkbxJtI6CIxzc'

# Try HEAD request first to see headers
r = httpx.head(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10, follow_redirects=True)
print(f'HEAD Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("content-type")}')
print(f'Content-Length: {r.headers.get("content-length")}')
print(f'Final URL: {r.url}')
for k, v in r.headers.items():
    print(f'  {k}: {v}')