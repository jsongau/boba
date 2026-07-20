#!/usr/bin/env python3
"""Idempotent favicon stamp for Boba Night.

Inserts the favicon <link> block into the <head> of every git-tracked HTML page
that does not already have it. Mirrors apply_nav.py — run it after any page
regeneration (gen_site / gen_profiles / add_spots / gen_events) so the whole
site keeps the favicon. Safe to run repeatedly.

    python3 build/apply_favicon.py
"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = (
    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
)
CHARSET = re.compile(r'<meta[^>]*charset[^>]*>', re.I)
HEAD = re.compile(r'<head[^>]*>', re.I)

def tracked_html():
    out = subprocess.check_output(['git', '-C', ROOT, 'ls-files', '*.html'], text=True)
    return [f for f in out.split() if f and not f.startswith(('templates/', 'build/'))]

def main():
    changed = skipped = nohead = 0
    for rel in tracked_html():
        p = os.path.join(ROOT, rel)
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        if 'rel="icon"' in s:          # already stamped
            skipped += 1
            continue
        m = CHARSET.search(s) or HEAD.search(s)
        if not m:                       # no head anchor — leave it alone
            nohead += 1
            continue
        i = m.end()
        open(p, 'w', encoding='utf-8').write(s[:i] + '\n' + BLOCK + s[i:])
        changed += 1
    print(f'favicon stamp -> changed={changed} skipped={skipped} nohead={nohead}')

if __name__ == '__main__':
    main()
