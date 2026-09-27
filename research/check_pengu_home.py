from curl_cffi import requests

# Check pengu.uk homepage
r = requests.get('https://pengu.uk/', impersonate='chrome133a', timeout=15)
print(f'Homepage Status: {r.status_code}')
print(f'Title: {r.text[:500]}')

# Check if there's an API or documentation
r2 = requests.get('https://pengu.uk/api', impersonate='chrome133a', timeout=15)
print(f'\nAPI Status: {r2.status_code}')
print(f'Response: {r2.text[:500]}')