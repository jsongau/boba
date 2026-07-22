#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boba Night - nav drift guard.

The homepage keeps a BAKED copy of the universal mega nav (for SEO and instant
paint); every other page loads it live from components/nav.html. This script
verifies the two are in sync, because a drifted pair is the one failure the
chrome kit cannot self-heal.

    python3 /Users/kytlegacy/Claude/Projects/NiteBoba/build/check_nav_sync.py
    python3 /Users/kytlegacy/Claude/Projects/NiteBoba/build/check_nav_sync.py --fix

Plain run: reports SYNCED or DRIFTED (with the first differing lines) and exits
1 on drift - safe for a pre-push habit. --fix: splices the component markup into
the homepage's baked header so components/nav.html stays the single source of
truth. Run it after ANY edit to components/nav.html.
"""
import os, re, sys, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX  = os.path.join(ROOT, "index.html")
NAV  = os.path.join(ROOT, "components", "nav.html")

def strip_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)

def norm(s):
    s = strip_comments(s)
    return re.sub(r"\s+", " ", s).strip()

def homepage_block(idx):
    m = re.search(r"<header[^>]*data-bn-header.*?</header>", idx, re.S)
    if m: return m.group(0), m.span()
    m = re.search(r'<div class="fuse".*?(?=<main)', idx, re.S)
    if m: return m.group(0), m.span()
    return None, None

def main():
    idx = open(IDX, encoding="utf-8").read()
    nav = open(NAV, encoding="utf-8").read()
    # compare like with like: only the <header> portion of the component
    m = re.search(r"<header[^>]*data-bn-header.*?</header>", nav, re.S)
    if m: nav = m.group(0)
    block, span = homepage_block(idx)
    if block is None:
        print("DRIFTED: could not find the baked header in index.html"); sys.exit(1)
    if norm(block) == norm(nav):
        print("SYNCED: homepage baked header matches components/nav.html"); return
    if "--fix" in sys.argv:
        out = idx[:span[0]] + strip_comments(nav).strip() + idx[span[1]:]
        open(IDX, "w", encoding="utf-8").write(out)
        print("FIXED: homepage baked header replaced with components/nav.html markup")
        print("Review with: git -C %s diff index.html" % ROOT); return
    print("DRIFTED: homepage baked header differs from components/nav.html")
    a = norm(block).split("> <"); b = norm(nav).split("> <")
    for line in list(difflib.unified_diff(a, b, "homepage", "component", lineterm=""))[:14]:
        print("  " + line[:150])
    sys.exit(1)

if __name__ == "__main__":
    main()
