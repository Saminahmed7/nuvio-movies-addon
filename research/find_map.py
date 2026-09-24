import httpx

text = httpx.get('https://www.rivestream.app/_next/static/chunks/2427-f1dd7c2a4b7832e1.js').text

# Find where "MAP" is used in the file
pos = text.find('4k/Single-Server')
if pos != -1:
    print("--- 4k/Single-Server Context ---")
    print(text[max(0, pos - 200): min(len(text), pos + 1200)])

pos2 = text.find('value:"MAP"')
if pos2 != -1:
    print("\n--- value:\"MAP\" Context ---")
    print(text[max(0, pos2 - 200): min(len(text), pos2 + 1200)])
