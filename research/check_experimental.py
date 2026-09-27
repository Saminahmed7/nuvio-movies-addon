from curl_cffi import requests

# Check experimental status endpoint
r = requests.get('https://pengu.uk/api/experimental/status', impersonate='chrome133a', timeout=15)
print(f'Experimental Status: {r.status_code}')
print(f'Response: {r.text}')