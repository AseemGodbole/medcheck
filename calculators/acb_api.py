"""
ACB calculator API client wrapper.

This module attempts to use an official JSON API endpoint if you provide one.
If no documented API is supplied, it can try to discover XHR/fetch endpoints used
by the web app and call those. Scraping or automated discovery is disabled by
default and must be enabled explicitly via `allow_discovery=True`.

Important: Only enable discovery/scraping if you have permission from the site
owner and if `robots.txt` and the site's Terms permit programmatic access.
"""
from typing import List, Optional
import requests
from urllib.parse import urljoin
import re
import json
import logging

logger = logging.getLogger(__name__)

DEFAULT_BASE = "https://www.acbcalc.com/"


def fetch_robots(base_url: str = DEFAULT_BASE, timeout: int = 5) -> Optional[str]:
    r = requests.get(urljoin(base_url, "robots.txt"), timeout=timeout)
    if r.status_code == 200:
        return r.text
    return None


def discover_xhr_endpoints(html: str) -> List[str]:
    """Try to find likely XHR/fetch endpoints in inline scripts.

    Returns a list of endpoint URLs (may be relative paths).
    """
    endpoints = set()
    # look for fetch('/api/...') or fetch("/something") patterns
    for m in re.findall(r"fetch\((?:\'|\")([^\'\"]+)(?:\'|\")", html):
        endpoints.add(m)
    # look for axios/post or XHR urls in scripts
    for m in re.findall(r"\b(?:url|endpoint)\s*[:=]\s*(?:'|\")([^\'\"]+)(?:'|\")", html):
        endpoints.add(m)
    # also capture hard-coded /api/ or /ajax/ paths
    for m in re.findall(r"([\"'])(/[^\"'\s>]+/api[^\"']*)\1", html):
        endpoints.add(m[1])
    return list(endpoints)


def try_call_endpoint(base_url: str, endpoint: str, drugs: List[str], timeout: int = 8):
    url = urljoin(base_url, endpoint)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"drugs": drugs}
    # try POST then GET
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return r.text
    except Exception:
        pass
    try:
        # as fallback try GET with drugs joined
        q = ",".join(drugs)
        r = requests.get(urljoin(url, f"?drugs={requests.utils.requote_uri(q)}"), headers=headers, timeout=timeout)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return r.text
    except Exception:
        pass
    return None


def compute_remote_acb(drugs: List[str], base_url: str = DEFAULT_BASE, api_endpoint: Optional[str] = None,
                       allow_discovery: bool = False) -> dict:
    """Compute ACB using a remote source.

    - If `api_endpoint` is provided, calls that endpoint (POST JSON {"drugs": [...]})
    - Otherwise, if `allow_discovery=True`, fetches the homepage and looks for XHR
      endpoints to call automatically.

    Returns a dict with keys: `source`, `result`.
    """
    if api_endpoint:
        res = try_call_endpoint(base_url, api_endpoint, drugs)
        if res is not None:
            return {"source": api_endpoint, "result": res}
        raise RuntimeError(f"API endpoint {api_endpoint} did not return a usable response")

    if allow_discovery:
        # fetch homepage and try to discover endpoints
        r = requests.get(base_url, timeout=8)
        r.raise_for_status()
        html = r.text
        endpoints = discover_xhr_endpoints(html)
        if not endpoints:
            raise RuntimeError("No XHR endpoints discovered on page. Discovery failed.")
        for ep in endpoints:
            try:
                res = try_call_endpoint(base_url, ep, drugs)
                if res is not None:
                    return {"source": ep, "result": res}
            except Exception:
                continue
        raise RuntimeError("Discovery ran but no endpoints returned usable results.")

    raise RuntimeError("No API endpoint provided and discovery not allowed. Provide `api_endpoint` or set `allow_discovery=True`.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python calculators/acb_api.py \"drug1, drug2\" [--discover]")
        sys.exit(1)
    raw = sys.argv[1]
    allow_discovery = False
    if len(sys.argv) > 2 and sys.argv[2] == "--discover":
        allow_discovery = True
    meds = [m.strip() for m in raw.split(",") if m.strip()]
    try:
        out = compute_remote_acb(meds, allow_discovery=allow_discovery)
        print("Source:", out["source"])
        print("Result:")
        print(out["result"])
    except Exception as e:
        print("Error:", e)
