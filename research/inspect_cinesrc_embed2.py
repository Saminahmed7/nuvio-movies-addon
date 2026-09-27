import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://cinesrc.st/'
}

r = requests.get('https://cinesrc.st/embed/movie/550', headers=headers, timeout=10)
html = r.text

# Find all next.js scripts
scripts = re.findall(r'/_next/static/chunks/[^\s"\']+\.js', html)
print("All scripts from embed page:")
for s in scripts:
    print(" ", s)
    
# Also check script tags in the page
script_tags = re.findall(r'<script[^>]+src="([^"]+)"', html)
print("Script tags:")
for s in script_tags:
    print(" ", s)

# Find _next/data endpoint
data_endpoints = re.findall(r'/_next/data/[^\s"\']+', html)
print("Data endpoints:", data_endpoints)

# Check for server actions
server_actions = re.findall(r'Next-Action.*?([0-9a-f]{40})', html)
print("Server actions from HTML:", server_actions)

# Print first 2000 chars of response
print("\nHTML head snippet:")
print(html[:3000])
