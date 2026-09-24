from curl_cffi import requests
import re

url = 'https://anyembed.xyz/assets/index-uplUFmH_.js'
text = requests.get(url, impersonate='chrome133a').text

pos = text.find('/embed/tmdb-movie-')
if pos == -1:
    pos = text.find('tmdb-movie-')

if pos != -1:
    print(text[max(0, pos - 200): min(len(text), pos + 1000)])
