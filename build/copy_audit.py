#!/usr/bin/env python3
"""Scan the site's VISIBLE copy for AI tells (see docs/COPY-STANDARD-anti-ai.md).

    python3 build/copy_audit.py              # scan all pages, print findings
    python3 build/copy_audit.py path ...     # scan specific files

Catches the MECHANICAL tells only (arrows, em-dash separators, banned words in
visible text). Judgment tells (synthetic triplets, contrast formulas, filler
intros) still need a human/agent read — this is the lint, not the whole audit.
It reads visible text only: strips <script>/<style>, tags, and HTML comments,
so CSS property names and JS keywords don't false-positive.
"""
import re, sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent

ARROWS = ["->", "→", "➔", "⟶", "⇒", "»"]  # -> → ➔ ⟶ ⇒ »
BANNED = [
    # CLAUDE.md list
    "hidden gem", "nestled", "vibrant", "indulge", "premium", "curated",
    "discover", "seamless", "elevate", "empower", "innovative",
    "look no further", "burst of flavor",
    # AI-corporate tells
    "unlock", "leverage", "revolutionary", "cutting edge", "state of the art",
    "comprehensive", "frictionless", "hassle free", "stress free",
    "peace of mind", "one stop shop", "we've got you covered", "game changer",
    "world class", "best in class", "robust", "embark", "ecosystem",
    "next level", "experience the difference", "take control",
]
# contrast/filler shapes (word-boundary-ish, lowercased text)
FORMULAS = [
    "it's not just", "it is not just", "not just a", "more than just",
    "in a world where", "when it comes to", "at the end of the day",
    "now more than ever", "the future of", "this is where",
    "it's worth noting", "it's important to note", "our mission is",
    "we're proud to", "we are proud to",
]

def visible_text(h):
    h = re.sub(r"<script\b.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style\b.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    # keep aria-label / alt / placeholder / title / meta content (visible-ish to users/AT)
    attrs = " ".join(re.findall(r'(?:aria-label|alt|placeholder|title|content)="([^"]*)"', h))
    h = re.sub(r"<[^>]+>", " ", h)
    return html.unescape(h + " " + attrs)

def scan(path):
    t = visible_text(pathlib.Path(path).read_text(errors="ignore"))
    low = t.lower()
    hits = []
    for a in ARROWS:
        if a in t:
            hits.append(("arrow", a, t.count(a)))
    # em dash used between word chars (separator), not a numeric range
    for m in re.finditer(r"\w\s*—\s*\w", t):
        hits.append(("em-dash", m.group(0).strip()[:40], 1)); break
    for w in BANNED:
        n = len(re.findall(r"(?<!\w)" + re.escape(w) + r"(?!\w)", low))
        if n:
            hits.append(("banned", w, n))
    for f in FORMULAS:
        if f in low:
            hits.append(("formula", f, low.count(f)))
    return hits

def main():
    args = sys.argv[1:]
    if args:
        files = [pathlib.Path(a) for a in args]
    else:
        files = [p for p in ROOT.rglob("*.html")
                 if ".git" not in p.parts and "archive" not in p.parts]
    total = 0
    flagged = 0
    for p in sorted(files):
        hits = scan(p)
        if hits:
            flagged += 1
            rel = p.resolve().relative_to(ROOT)
            print(f"\n{rel}")
            for kind, tok, n in hits:
                total += n
                print(f"  [{kind}] {tok!r} x{n}")
    print(f"\n=== {total} tell(s) across {flagged}/{len(files)} files ===")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main())
