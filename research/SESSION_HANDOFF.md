# Session Handoff & Status Summary

**Date:** 2026-09-27  
**Repository:** `F:\nuvio-movies-addon`  
**Current Production Version:** `v2.1.0` (Deployed on Vercel)  
**Active Production Providers:** `videasy`, `cinejoy`, `xpass`, `vidlove`, `vidrock`

---

## 1. Saved State & Git Status
- All changes, research scripts, disassembled DEX dumps, and analysis files have been committed to local git on branch `main`.
- Working tree status: Clean.

---

## 2. Active Production Status (v2.1.0)
- **Deployed App:** `https://nuvio-movies-addon-samin13.vercel.app`
- **Health:** `/health` returns `200 OK`, `version: 2.1.0`.
- **Diagnostic:** `/diag` reports 5 providers functional:
  - `videasy` (4K/1080p)
  - `cinejoy` (4K/1080p, Lisbon/Nebula/Solara nodes)
  - `xpass` (1080p, AES-128-GCM local decryption, TIK/VIP nodes)
  - `vidlove` (1080p)
  - `vidrock` (1080p Luna)
- **Local Test Suite:** `python test_app.py` passes 14/14 tests.

---

## 3. Provider Research Findings

### Candidates Evaluated:
1. **Peachify:** Abandoned (API endpoints return 404).
2. **Vidzee:** Abandoned for serverless (requires client-side WASM decrypt `streams-BHpSC3gU.js`).
3. **CineSrc (`cinesrc.st`):** Abandoned for serverless (two-stage WebAssembly PoW: `pow-worker-v3.js`, `pow-v3.wasm`).
4. **MovieBox (`aoneroom.com`):** Disassembled HMAC-MD5 signature algorithm (`research/disasm_moviebox*.py`, `research/test_mbox_vars.py`), but server returns 407 (signature validation failure).
5. **Vidlink (`vidlink.pro`):** ❌ ABANDONED
   - Token mechanism works: `GET https://enc-dec.app/api/enc-vidlink?text={tmdb_id}` returns valid token
   - API endpoint: `GET https://vidlink.pro/api/b/movie/{tmdb_id}?token={token}` returns HTTP 200
   - **Problem**: All responses return `null` — no stream data available
   - Tested with multiple TMDB IDs (550, 27205, 1396, 1399, 66732, 76479, 106379) — all null
   - Both movie and TV endpoints return null
   - Conclusion: Vidlink has no content available (possibly geo-blocked or requires auth)

---

## 4. Future Plan & Next Steps (For Next Agent / Developer)

### Step 1: CSX-Style Free Provider Implementation
- Vidlink abandoned (API returns null for all content)
- Goojara accessible but no extractable content
- BanglaPlex accessible but uses complex embed chain (plextream → abyssplayer → JWPlayer)
- **New approach**: Port CSX CloudStream extractors to Python (all free, no debrid)
- **Target file hosts**: GDFlix, HubCloud, Driveleech, Gofile (most common in CSX)
- **Source sites to scrape**: Bollyflix, MoviesDrive, Moviesmod (provide file host links)

### Step 2: Implement File Host Extractors in Python
- GDFlix/GDLink: Parse HTML for download buttons, extract direct links
- HubCloud/VCloud: Extract URLs from JavaScript variables
- Driveleech/Driveseed: Parse HTML for download links
- Gofile: API-based file listing
- Use `cloudscraper` or `curl_cffi` for Cloudflare bypass

### Step 3: Scrape Source Sites for File Host Links
- Bollyflix (`bollyflix.frl`): Parse `a.dl` buttons, decode base64 links
- MoviesDrive (`moviesdrive.forum`): Parse `h5 > a` buttons
- Moviesmod (`moviesleech.rest`): Parse `a.maxbutton-*` buttons
- All use dynamic URLs from `urls.json`

### Step 4: Integrate and Test
- Wire source site scraping + file host extraction into provider chain
- Bump version, test, deploy

### Step 5: Additional Free Providers (Backlog)
- **Movies & TV:** Cinefreak (`search.yagaverse.net`), Goojara (`ww1.goojara.to`)
- **Anime Addon (`F:\nuvio-anime-addon`):** AllWish (`all-wish.me`)
- **CSX Sources:** Bollyflix, MoviesDrive, Moviesmod, VegaMovies (free, no auth)

---

## 5. Constraints & Operational Rules
- Target runtime: Python 3.10 on Windows / Vercel Serverless.
- Execution deadline: Responses must complete in $< 4.0$s.
- Quality floor: Strictly $\ge 1080p$ streams only.
- Preserve all existing files in `research/`.
- **NO PAID SERVICES** — Real-Debrid, AllDebrid, Premiumize, or any subscription-based debrid is OFF LIMITS. All providers must be free (no accounts, no fees, no credits).

---

## 6. Vercel Deployment Info
- **Project ID:** `prj_LKLeEcjq3eBqOx9rBkU8tHLIJ9ZN`
- **Token:** stored in `.env` as `VERCEL_TOKEN`
- **Deploy URL:** `https://nuvio-movies-addon-samin13.vercel.app`
- **vercel.json:** rewrites all routes to `/api/index`, maxDuration=60s
- **Entry point:** `api/index.py` imports `main:app`
