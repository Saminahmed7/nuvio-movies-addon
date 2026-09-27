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
5. **Vidlink (`vidlink.pro`):**
   - Analysis scripts: `research/find_vidlink_methods.py`, `research/inspect_vid_providers.py`.
   - Identified extraction mechanism in DEX (`StreamPlayExtractor.invokeVidlink` / Method #10088):
     - Token request: `GET https://enc-dec.app/api/enc-vidlink?text={tmdb_id}` -> `{"result": "<token>"}`
     - Movie API: `GET https://vidlink.pro/api/b/movie/{tmdb_id}/{result_token}`
     - TV API: `GET https://vidlink.pro/api/b/tv/{tmdb_id}/{season}/{episode}/{result_token}`
     - Headers required: `Referer: https://vidlink.pro/`, `Origin: https://vidlink.pro`
     - Response structure: `VidlinkResponse` with `stream.qualities` (1080p/720p `.m3u8` links) and `stream.captions`.

---

## 4. Future Plan & Next Steps (For Next Agent / Developer)

### Step 1: Live Verification of Vidlink
- Run a test script against `enc-dec.app` and `vidlink.pro`:
  - Request token for sample movie (TMDB ID `550` = Fight Club).
  - Call `https://vidlink.pro/api/b/movie/550/{token}` with required headers.
  - Verify that `stream.qualities['1080p'].url` returns HTTP 200 with valid `.m3u8` playlist.

### Step 2: Implement Provider Module (`providers/vidlink.py`)
- Signature: `async def get_streams(media_type: str, tmdb_id: str, season: Optional[int] = None, episode: Optional[int] = None) -> List[Dict]`
- Enforce strict $\ge 1080p$ filtering.
- Format stream dictionary: `name`, `title`, `url`, `headers`, `subtitles`.
- Set timeout to 3.5s to fit within serverless budget.

### Step 3: Integrate and Bump Version
- Import `vidlink` in `main.py`.
- Add to `PROVIDERS` dict.
- Bump addon version from `2.1.0` to `2.2.0`.
- Add test case in `test_app.py` and run verification.

### Step 4: Additional Backlog Candidates
- **Movies & TV:** Cinefreak (`search.yagaverse.net`), Goojara (`ww1.goojara.to`), BanglaPlex (`banglaplex.lat`).
- **Anime Addon (`F:\nuvio-anime-addon`):** AllWish (`all-wish.me`).

---

## 5. Constraints & Operational Rules
- Target runtime: Python 3.10 on Windows / Vercel Serverless.
- Execution deadline: Responses must complete in $< 4.0$s.
- Quality floor: Strictly $\ge 1080p$ streams only.
- Preserve all existing files in `research/`.
