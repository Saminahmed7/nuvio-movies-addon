import httpx

url = "https://d.whysosigmabro.cfd/api?d=hCl9XkyuGIfGEct6G19k5H-o6gGqIUW0Wrh44I4nqLiKuNiMoYJ10wSDzW5FIAFxu4E8hy6doZA97lAsxSn5KrSD9ANB9Mm2Za7GtHANZp86kAUw4mSksfHZ_wCYldrLt8rjGjvwR-WgSLu9vz-UFZIaRa5VZTu8SKshNFH7o4RtJQJLkwc_xQHAgdO_LwOj4BFidHS6gF5_PyXMOyICSSctrqn6dTSsdstSUCjzi5MZj4-1m4YWiaYnnvhMhsdmhUKIuHVp48K6Pyzj_PGV6feTPFtIctOZ08Z9NmmRhtmL7js4qIAbGVx37_oSllcQW9l20Uha_A9YGBbDgSQLL8mQ2K0slT5zDukEnoN95S6O0lU8ARTHm0UsWGn_taQxnRJdZL1a88-nG_DCHldES46WoK-YiXkkMZ5JHW82wWk_Zw0Q5zdpLyQglEViqCWpxMC_4Z8d50tHpB0YVBIiRMqZo0T_FBJY-Ya3oxmxcgQFmLvjjYigVwHcawVktZ68c_WhUPsL1nWQuUzRNLE8Uwo7xM3jMPFBoXMR3qVtlJLNKSXeiy_VYI6aP4Z_"

r = httpx.get(url, follow_redirects=True, timeout=10)
print(f"Content type: {r.headers.get('content-type')}")
print(f"Content length: {len(r.content)}")
print(f"First 100 bytes: {r.content[:100]}")
