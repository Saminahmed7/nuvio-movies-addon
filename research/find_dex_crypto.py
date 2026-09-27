import zipfile, re

z = zipfile.ZipFile('research/StreamPlay.cs3')
dex = z.read('classes.dex')

# Let's search for "decryptXpassDataUrl" and see the Dalvik bytecode around it!
# In DEX, method_ids point to proto, class, name.
# Let's search for occurrences of "decryptXpassDataUrl" string in dex string table
str_idx = dex.find(b'decryptXpassDataUrl\x00')
print('str_idx:', str_idx)

# Search for any references to that string index or literal strings in StreamPlayUtilsKt
# Let's search for all UTF-8 strings in dex between 5 and 50 chars that look like keys, urls, ivs
keys = re.findall(rb'[\x20-\x7e]{16,64}', dex)
for k in set(keys):
    if any(term in k.lower() for term in [b'xpass', b'pass', b'key', b'secret', b'token', b'iv', b'aes', b'auth']):
        print(k)
