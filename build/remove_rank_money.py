#!/usr/bin/env python3
"""Remove every mention of /how-we-rank/ and /how-we-make-money/ sitewide.
DRY-RUN by default; --apply to write.

Per HTML file:
  1. nav featured card pointing at /how-we-rank/ -> replaced with The Pearl Ratings card
  2. footer <li> entries for either page -> removed
  3. homepage proof-strip dot + link -> removed
  4. any remaining anchor to either page (relative or absolute) -> removed
Then reports any file still containing the phrases.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPLY = "--apply" in sys.argv

SKIP_DIRS = {".git", "node_modules", "_to_delete", "design-library", "docs", "examples",
             "how-we-rank", "how-we-make-money"}

NEW_FEAT = ('<a class="bn-feat" href="/critic/"><span class="bn-feat-plate plate plate--night">'
            '<span class="grain"></span></span><span class="bn-feat-kick">The critic</span>'
            '<span class="bn-feat-t">The Pearl Ratings</span>'
            '<span class="bn-feat-s">Reviews publish only after real visits.</span></a>')

RE_FEAT   = re.compile(r'<a class="bn-feat" href="(?:https://(?:www\.)?bobanight\.com)?/how-we-rank/">.*?</a>', re.S)
RE_LI     = re.compile(r'<li>\s*<a href="(?:https://(?:www\.)?bobanight\.com)?/how-we-(?:rank|make-money)/">[^<]*</a>\s*</li>')
RE_DOTLNK = re.compile(r'<span class="dot"[^>]*></span>\s*<a href="(?:https://(?:www\.)?bobanight\.com)?/how-we-rank/">[^<]*</a>')
RE_ANCHOR = re.compile(r'<a [^>]*how-we-(?:rank|make-money)[^>]*>[^<]*</a>')
RE_LEFT   = re.compile(r'how-we-rank|how-we-make-money|How we rank|How we make money', re.I)

def transform(s):
    orig = s
    s = RE_FEAT.sub(NEW_FEAT, s)
    s = RE_LI.sub('', s)
    s = RE_DOTLNK.sub('', s)
    s = RE_ANCHOR.sub('', s)
    return s, s != orig

changed = clean = 0
leftovers = []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dp, fn)
        s = open(path, encoding="utf-8").read()
        if not RE_LEFT.search(s):
            clean += 1; continue
        new, did = transform(s)
        if did:
            changed += 1
            if APPLY:
                open(path, "w", encoding="utf-8").write(new)
        rest = RE_LEFT.findall(new)
        if rest:
            leftovers.append((os.path.relpath(path, ROOT), len(rest)))

print(("APPLIED" if APPLY else "DRY-RUN"), "| files changed:", changed, "| already clean:", clean)
if leftovers:
    print("FILES WITH LEFTOVER MENTIONS:", len(leftovers))
    for p, n in leftovers[:12]:
        print("  ", p, n)
else:
    print("no leftover mentions anywhere")
