from curl_cffi import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://player.vidlove.cc/'
}

var_url = "https://d.whysosigmabro.cfd/api?d=hCl9XkyuGIfGEct6G19k5H-o6gGqIUW0Wrh44I4nqLiKuNiMoYJ10wSDzW5FIAFxu4E8hy6doZA97lAsxSn5KrSD9ANB9Mm2Za7GtHANZp86kAUw4mSksfHZ_wCYldrLt8rjGjvwR-WgSLu9vz-UFZIaRa5VZTu8SKshNFH7o4RtJQJLkwc_xQHAgdO_LwOj4BFidHS6gF5_PyXMOyICSSctrqn6dTSsdstSUCjzi5MZj4-1m4YWiaYnnvhMhsdmhUKIuHVp48K6Pyzj_PGV6feTPFtIctOZ08Z9NmmRhtmL7js4qIAbGVx37_oSllcQW9l20Uha_A9YGBbDgSQLL8mQ2K0slT5zDukEnoN95S6O0lU8ARTHm0UsWGn_taQxnRJdZL1a88-nG_DCHldES46WoK-YiXkkMZ5JHW82wWk_Zw0Q5zdpLyQglEViqCWpxMC_4Z8d50tHpB0YVBIiRMqZo0T_FBJY-Ya3oxmxcgQFmLvjjYigVwHcawVktZ68c_WhUPsL1nWQuUzRNLE8Uwo7xM3jMPFBoXMR3qVtlJLNKSXeiy_VYI6aP4Z_"

r = requests.get(var_url, headers=headers, impersonate='chrome133a')
lines = [l.strip() for l in r.text.splitlines() if l.strip() and not l.startswith('#')]
print(f"Total TS segments in 1080p stream: {len(lines)}")

# Benchmark first 3 segments
total_bytes = 0
t0 = time.time()
for idx, seg in enumerate(lines[:3]):
    sr = requests.get(seg, headers=headers, impersonate='chrome133a')
    size = len(sr.content)
    total_bytes += size
    print(f"Segment {idx+1}: {size/1024:.1f} KB (status {sr.status_code})")

elapsed = time.time() - t0
mbps = (total_bytes * 8) / (elapsed * 1_000_000)
print(f"Downloaded {total_bytes/1024/1024:.2f} MB in {elapsed:.2f}s -> {mbps:.2f} Mbps!")
