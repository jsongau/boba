#!/usr/bin/env python3
"""build/apply_nav.py — swap every page's old header for the canonical partial.

DRY-RUN BY DEFAULT. It only writes when you pass --apply.

It finds the THREE header patterns that exist across the site and replaces each
with templates/nav.html, and injects the nav's CSS/JS links if they're missing:

  1. homepage      <header class="masthead"> ... </header> + its .drawer sibling
  2. directory     <header class="site-header" id="siteHeader"> ... + .drawer
  3. gen_site      <header class="site-header"><div class="header-inner"> ... </header>

For 1 and 2 the old markup includes a trailing mobile drawer, so the match runs
from the header's start tag up to the following <main …>. For 3 there is no
drawer; the same up-to-<main bound covers it. The partial itself carries the new
header + search overlay + drawer + bottom bar, so one substitution does it all.

Usage:
    python3 build/apply_nav.py            # dry run: report only, writes nothing
    python3 build/apply_nav.py --apply    # actually rewrite the files
    python3 build/apply_nav.py --verbose  # also print each changed file

Prints per-pattern replace counts and lists any *.html that has a <header> but
matched none of the three known shapes (so nothing slips through silently).
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CSS_LINK = '<link rel="stylesheet" href="/css/nav-midnight.css">'
JS_LINK = '<script src="/js/nav-midnight.js" defer></script>'

# Each pattern: (name, compiled regex). All run from the header start tag up to
# the following <main…> so a trailing mobile drawer is swallowed too.
PATTERNS = [
    ("homepage/masthead",
     re.compile(r'<header class="masthead">[\s\S]*?(?=<main\b)')),
    ("directory/site-header",
     re.compile(r'<header class="site-header" id="siteHeader">[\s\S]*?(?=<main\b)')),
    ("gen_site/site-header",
     re.compile(r'<header class="site-header"><div class="header-inner">[\s\S]*?</header>\s*(?=<main\b)')),
]

HAS_HEADER = re.compile(r'<header[\s>]')


def load_partial():
    with open(os.path.join(ROOT, "templates", "nav.html"), encoding="utf-8") as f:
        # store the partial without a trailing newline explosion
        return f.read().rstrip("\n") + "\n"


def iter_html():
    skip = {".git", "docs", "examples", "templates", "build", "data"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def inject_assets(html):
    """Add the nav CSS to <head> and JS before </body> if not already present."""
    changed = False
    if "/css/nav-midnight.css" not in html:
        if "</head>" in html:
            html = html.replace("</head>", "  " + CSS_LINK + "\n</head>", 1)
            changed = True
    if "/js/nav-midnight.js" not in html:
        if "</body>" in html:
            html = html.replace("</body>", JS_LINK + "\n</body>", 1)
            changed = True
    return html, changed


def process(path, partial):
    """Return (matched_pattern_name | None, new_html | None, asset_injected)."""
    with open(path, encoding="utf-8") as f:
        html = f.read()
    matched = None
    new_html = html
    for name, rx in PATTERNS:
        if rx.search(new_html):
            new_html = rx.sub(lambda m: partial, new_html, count=1)
            matched = name
            break
    if matched is None:
        return None, None, False
    new_html, asset = inject_assets(new_html)
    return matched, new_html, asset


def main():
    apply = "--apply" in sys.argv
    verbose = "--verbose" in sys.argv
    partial = load_partial()

    counts = {name: 0 for name, _ in PATTERNS}
    asset_only = 0
    unmatched_with_header = []
    changed_files = []
    total = 0

    for path in iter_html():
        total += 1
        rel = os.path.relpath(path, ROOT)
        matched, new_html, asset = process(path, partial)
        if matched:
            counts[matched] += 1
            changed_files.append(rel)
            if apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_html)
            if verbose:
                print(f"  [{matched}] {rel}" + ("  (+assets)" if asset else ""))
        else:
            with open(path, encoding="utf-8") as f:
                raw = f.read()
            if HAS_HEADER.search(raw):
                unmatched_with_header.append(rel)

    mode = "APPLIED" if apply else "DRY RUN (no files written — pass --apply to write)"
    print("=" * 64)
    print(f"apply_nav.py — {mode}")
    print("=" * 64)
    print(f"HTML files scanned:            {total}")
    print("Per-pattern replacements:")
    for name, _ in PATTERNS:
        print(f"  {name:28s} {counts[name]}")
    print(f"  {'TOTAL headers replaced':28s} {sum(counts.values())}")
    print()
    print(f"Files with a <header> but NO known pattern matched: {len(unmatched_with_header)}")
    for rel in unmatched_with_header:
        print(f"  ? {rel}")
    if not apply:
        print()
        print(f"Would rewrite {len(changed_files)} file(s). Re-run with --apply to commit changes.")


if __name__ == "__main__":
    main()
