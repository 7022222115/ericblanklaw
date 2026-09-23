#!/usr/bin/env python3
"""Redirect coverage audit — EBIA WordPress -> Astro migration.

Reads every legacy URL from the triage sheet (EBIAtriageinventory_2_WORKING.xlsx,
sheet "Triage", columns URL + New Astro URL) and checks it against the target host.

PASS = the legacy path answers 301/308 straight to the expected target (single hop,
trailing slash normalised) AND the target answers 200.
Also reports how the NO-trailing-slash variant of each legacy path behaves, because
WordPress 301'd /foo -> /foo/ for every URL and Cloudflare Pages _redirects does not.

Usage:
    pip install openpyxl
    python scripts/redirect_audit.py EBIAtriageinventory_2_WORKING.xlsx [https://ericblanklaw.pages.dev]

Re-run after ANY _redirects change, and again on cutover day against the apex.
Known false-flags (sheet's "New Astro URL" is stale, decision was deliberate):
  #164 /sitemap/          -> /sitemap-index.xml (sheet says /sitemap.xml)      session 4
  #194 /chayannegiveaway/ -> /giveaway/        (sheet says keep URL)           session 5
"""
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

import openpyxl

XLSX = sys.argv[1] if len(sys.argv) > 1 else "EBIAtriageinventory_2_WORKING.xlsx"
HOST = (sys.argv[2] if len(sys.argv) > 2 else "https://ericblanklaw.pages.dev").rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = urllib.request.build_opener(NoRedirect)
opener.addheaders = [("User-Agent", "ebia-redirect-audit/1.0")]


def head(url):
    """Return (status, location) without following redirects."""
    req = urllib.request.Request(url, method="GET")
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location")
    except Exception as e:  # network
        return -1, str(e)


def norm(path):
    """Compare paths ignoring host and trailing slash (XML/file targets keep no slash)."""
    p = urlsplit(path).path if "://" in path else path
    last = p.rsplit("/", 1)[-1]
    if not p.endswith("/") and "." not in last:
        p += "/"
    return p


def check(row):
    n, legacy, target = row
    path = urlsplit(legacy).path or "/"
    status, loc = head(HOST + path)
    result = {"n": n, "path": path, "target": target, "status": status, "loc": loc}
    if path == "/":
        result["ok"] = status == 200
        result["why"] = "" if result["ok"] else f"homepage {status}"
    elif status in (301, 308) and loc and norm(loc) == norm(target):
        t_status, _ = head(HOST + urlsplit(loc).path)
        result["ok"] = t_status == 200
        result["why"] = "" if result["ok"] else f"target {t_status}"
    elif status == 200 and norm(path) == norm(target):
        result["ok"] = True  # URL kept as-is (KEEP rows)
        result["why"] = ""
    else:
        result["ok"] = False
        result["why"] = f"{status} -> {loc}" if loc else f"{status}"
    # no-slash variant (informational)
    if path != "/" and path.endswith("/"):
        s2, l2 = head(HOST + path.rstrip("/"))
        result["noslash"] = f"{s2}" + (f" -> {urlsplit(l2).path}" if l2 else "")
    else:
        result["noslash"] = "n/a"
    return result


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Triage"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    i_url, i_new = hdr.index("URL"), hdr.index("New Astro URL")
    data = [(r[0], r[i_url], r[i_new]) for r in rows[1:] if r[i_url] and r[i_new]]
    print(f"{len(data)} legacy URLs from {XLSX} -> {HOST}\n")
    with ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(check, data))
    ok = [r for r in results if r["ok"]]
    bad = [r for r in results if not r["ok"]]
    print(f"PASS {len(ok)} / {len(results)}\n")
    if bad:
        print("FAIL:")
        for r in bad:
            print(f"  #{r['n']:<4} {r['path']:<70} expected {r['target']:<45} got {r['why']}")
    noslash_404 = [r for r in results if r["noslash"].startswith("404")]
    print(f"\nNo-trailing-slash variant 404s: {len(noslash_404)} of {len(results)} (WordPress 301'd these; Pages _redirects does not match them)")


if __name__ == "__main__":
    main()
