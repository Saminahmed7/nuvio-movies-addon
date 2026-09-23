# Nuvio Movies & TV Addon (>= 1080p)

High-performance, zero-maintenance Stremio/Nuvio HTTP addon providing direct streaming links for Movies and TV Series.

## Features
- **Strict Quality Enforcement**: Filters and serves streams strictly **$\ge 1080p$** (1080p Full HD, 1440p 2K, 2160p 4K UHD). All $<1080p$ streams are dropped.
- **File Size in UI**: Computes and formats video file sizes for both text badges (`Size: 2.4 GB`) and native `behaviorHints.videoSize`.
- **Zero Maintenance**: Direct HTTP/HLS streams without mandatory cookies or accounts.
- **Fast Serverless Concurrency**: Built with FastAPI, `httpx`, and `curl_cffi` designed to resolve streams within strict serverless budgets (Vercel 10s execution window).
- **Metadata Support**: Resolves IMDb (`tt...`) and TMDB IDs via Cinemeta.

## Local Development
```bash
pip install -r requirements.txt
python main.py
```
App starts on `http://127.0.0.1:7001`.

## Endpoints
- `/manifest.json` — Addon manifest
- `/stream/{type}/{id}.json` — Stream resolution endpoint (`type`: `movie` or `series`)
- `/diag?q=Inception` — Provider health checks
- `/ping` — Keep-alive endpoint
