#!/usr/bin/env python3
"""Swap the site's nav partial for the Pearl Line finder header on every page,
and inject the shared finder assets. DRY-RUN by default; pass --apply to write.

  python3 build/apply_finder_nav.py           # report only
  python3 build/apply_finder_nav.py --apply   # rewrite pages in place
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPLY = "--apply" in sys.argv

PARTIAL = open(os.path.join(HERE, "nav-finder-partial.html"), encoding="utf-8").read().strip()

OLD_NAV = re.compile(r'<a class="bn-skip".*?<nav class="bn-bottombar"[^>]*>.*?</nav>', re.S)
CSS_LINK = '<link rel="stylesheet" href="/css/finder.css">'
JS_LINKS = ('<script defer src="/js/finder-data.js"></script>\n'
            '<script defer src="/js/finder.js"></script>')
NAVCSS = '<link rel="stylesheet" href="/css/nav-midnight.css">'

SKIP_DIRS = {".git", "node_modules", "build", "templates", "_to_delete",
             "design-library", "docs", "examples", "critic"}
# pages that must NOT be touched (own finder / no nav)
SKIP_PATHS = {"nearby/index.html", "account/index.html"}

def iter_html():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn)

def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, "/")

swapped = injected = skipped_nonav = skipped_named = 0
no_navcss = []
for path in iter_html():
    r = rel(path)
    if r in SKIP_PATHS:
        skipped_named += 1; continue
    s = open(path, encoding="utf-8").read()
    if not OLD_NAV.search(s):
        skipped_nonav += 1; continue
    new = OLD_NAV.sub(lambda m: PARTIAL, s, count=1)
    # inject finder.css after nav-midnight.css (once)
    if CSS_LINK not in new:
        if NAVCSS in new:
            new = new.replace(NAVCSS, NAVCSS + "\n" + CSS_LINK, 1)
        else:
            no_navcss.append(r)
            new = new.replace("</head>", CSS_LINK + "\n</head>", 1)
    # inject finder scripts before </body> (once)
    if "/js/finder.js" not in new:
        new = new.replace("</body>", JS_LINKS + "\n</body>", 1)
    swapped += 1
    if new != s:
        injected += 1
        if APPLY:
            open(path, "w", encoding="utf-8").write(new)

print(f"{'APPLIED' if APPLY else 'DRY-RUN'}")
print(f"  pages swapped:        {swapped}")
print(f"  pages written:        {injected if APPLY else 0} (would write {injected})")
print(f"  skipped (no nav):     {skipped_nonav}")
print(f"  skipped (named):      {skipped_named}")
if no_navcss:
    print(f"  WARN no nav-midnight.css link ({len(no_navcss)}): {no_navcss[:5]}")
