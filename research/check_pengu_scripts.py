from curl_cffi import requests
import re

# Check pengu.uk for any JavaScript that might reveal the API
r = requests.get('https://pengu.uk/', impersonate='chrome133a', timeout=15)

# Look for script tags
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text)
print('Script sources:')
for s in scripts:
    print(f'  {s}')

# Look for any API endpoints in the page
apis = re.findall(r'["\'](/api/[^"\']+)["\']', r.text)
print('\nAPI endpoints in page:')
for a in set(apis):
    print(f'  {a}')

# Look for any mentions of "direct" or "experimental"
direct = re.findall(r'["\']([^"\']*direct[^"\']*)["\']', r.text)
print('\nDirect mentions:')
for d in set(direct):
    print(f'  {d}')

experimental = re.findall(r'["\']([^"\']*experimental[^"\']*)["\']', r.text)
print('\nExperimental mentions:')
for e in set(experimental):
    print(f'  {e}')