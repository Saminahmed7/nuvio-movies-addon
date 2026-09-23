"""Lightweight Cloudflare & TLS bypass for movie/tv providers.

Strategy:
1. TLS fingerprint impersonation via curl_cffi (chrome133a).
2. Host concurrency gating and polite delay per host.
3. Common fetch_text / fetch_json helpers.
"""
import asyncio
import os
import time
from urllib.parse import urlparse

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)
IMPERSONATE = "chrome133a"

CF_MARKERS = (
    "Just a moment",
    "Verify you are human",
    "cf-challenge",
    "cf_clearance",
    "Attention Required! | Cloudflare",
    "Enable JavaScript and cookies to continue",
    "ddos-guard",
    "check.ddos-guard.net",
    "__ddg",
    "DDoS protection by",
)


class CFBlocked(Exception):
    pass


_gates: dict[str, asyncio.Semaphore] = {}
_last_hits: dict[str, float] = {}


def _get_gate(host: str) -> asyncio.Semaphore:
    if host not in _gates:
        _gates[host] = asyncio.Semaphore(3)
    return _gates[host]


def effective_ua() -> str:
    return os.getenv("BROWSER_UA", DEFAULT_UA).strip() or DEFAULT_UA


def parse_cookie_header(raw: str) -> dict:
    out: dict[str, str] = {}
    for part in (raw or "").split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def cookies_for(*env_names: str) -> dict:
    for name in env_names:
        raw = os.getenv(name, "")
        if raw.strip():
            return parse_cookie_header(raw)
    return {}


async def _polite_delay(host: str):
    try:
        wait_ms = int(os.getenv("CF_DELAY_MS", "300"))
    except ValueError:
        wait_ms = 300
    now = time.monotonic()
    last = _last_hits.get(host, 0.0)
    wait = wait_ms / 1000.0 - (now - last)
    if wait > 0:
        await asyncio.sleep(wait)
    _last_hits[host] = time.monotonic()


def is_cf_challenge(status: int, text: str) -> bool:
    if status in (403, 503) and any(m in text for m in CF_MARKERS):
        return True
    if any(m in text for m in ("cf-challenge-form", "cf_turnstile")):
        return True
    return False


async def fetch_text(
    url: str,
    referer: str = "",
    cookie_envs: tuple[str, ...] = (),
    extra_headers: dict | None = None,
    timeout: int = 20,
) -> tuple[int, str, str]:
    """GET with TLS impersonation. Returns (status, text, final_url). Raises CFBlocked."""
    from curl_cffi.requests import AsyncSession

    host = urlparse(url).netloc.lower()
    async with _get_gate(host):
        await _polite_delay(host)
        headers = {
            "User-Agent": effective_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        if referer:
            headers["Referer"] = referer
        if extra_headers:
            headers.update(extra_headers)
        cookies = cookies_for(*cookie_envs) if cookie_envs else {}
        async with AsyncSession(impersonate=IMPERSONATE, timeout=timeout) as s:
            r = await s.get(url, headers=headers, cookies=cookies, allow_redirects=True)
            try:
                body = r.text
            except Exception:
                body = ""
            if is_cf_challenge(r.status_code, body):
                raise CFBlocked(
                    f"Cloudflare challenge at {url} (HTTP {r.status_code})."
                )
            return r.status_code, body, str(r.url)


async def fetch_json(
    url: str,
    referer: str = "",
    cookie_envs: tuple[str, ...] = (),
    extra_headers: dict | None = None,
    timeout: int = 20,
) -> tuple[int, object, str]:
    import json as _json

    status, text, final_url = await fetch_text(url, referer, cookie_envs, extra_headers, timeout)
    if status != 200:
        return status, None, final_url
    try:
        return status, _json.loads(text), final_url
    except Exception:
        return status, None, final_url
