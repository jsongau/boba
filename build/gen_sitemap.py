#!/usr/bin/env python3
"""Generate sitemap.xml from the site itself.

Includes every *.html page that is NOT marked noindex, with lastmod from file
mtime. Excludes build/template/doc folders. Run after any page-generating step.

  python3 build/gen_sitemap.py          # writes sitemap.xml, prints summary
"""
import os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://www.bobanight.com"

SKIP_DIRS = {".git", ".claude", "node_modules", "_to_delete", "build", "templates",
             "docs", "examples", "design-library", "css", "js", "data", "critic"}
# critic excluded from walk? no — critic is a real section. Remove from skips below.
SKIP_DIRS.discard("critic")

RE_NOINDEX = re.compile(r'name="robots"\s+content="[^"]*noindex', re.I)

urls = []
skipped_noindex = 0
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for fn in fns:
        if fn != "index.html":
            continue
        path = os.path.join(dp, fn)
        try:
            head = open(path, encoding="utf-8").read(4000)
        except Exception:
            continue
        if RE_NOINDEX.search(head):
            skipped_noindex += 1
            continue
        rel = os.path.relpath(dp, ROOT).replace(os.sep, "/")
        loc = BASE + "/" if rel == "." else BASE + "/" + rel + "/"
        lastmod = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
        urls.append((loc, lastmod))

urls.sort(key=lambda x: (x[0].count("/"), x[0]))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, lastmod in urls:
    out.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, lastmod))
out.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")

from collections import Counter
c = Counter()
for loc, _ in urls:
    p = loc.replace(BASE + "/", "")
    top = p.split("/")[0] if p else "(home)"
    c[top] += 1
print("sitemap.xml written:", len(urls), "urls | noindex skipped:", skipped_noindex)
for k, v in c.most_common(20):
    print("  %-14s %d" % (k, v))
