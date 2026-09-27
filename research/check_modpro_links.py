from curl_cffi import requests
import re

links = [
    'https://links.modpro.blog/archives/5785',
    'https://links.modpro.blog/archives/5786',
    'https://links.modpro.blog/archives/5787',
]

for link in links:
    r = requests.get(link, impersonate='chrome133a', timeout=15)
    print(f'{link} -> {r.status_code}')
    
    download_links = re.findall(r'href=["\']([^"\']*(?:drive|mega|mediafire|gdrive|1fichier|pixeldrain|gofile|anonfiles|bayfiles|dropbox|yadi\.sk|cloudflare|workers\.dev|m3u8)[^"\']*)["\']', r.text, re.IGNORECASE)
    if download_links:
        print(f'  Download links: {download_links[:3]}')
    
    m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
    if m3u8:
        print(f'  m3u8: {m3u8}')
    
    video_hosts = re.findall(r'https?://[^\s"\'<>]+', r.text)
    video_hosts = [v for v in video_hosts if any(h in v for h in ['drive', 'mega', 'mediafire', '1fichier', 'pixeldrain', 'gofile', 'anonfiles', 'bayfiles', 'dropbox', 'yadi', 'cloudflare', 'workers.dev', 'gdrive'])]
    if video_hosts:
        print(f'  Video hosts: {video_hosts[:5]}')