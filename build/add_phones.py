#!/usr/bin/env python3
"""Backfill `telephone` into profile JSON-LD from data/stores-data.json.

build/gen_profiles.py already emits telephone for new builds; deployed pages
predate that line. This patches them in place. Idempotent; --apply to write.
"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPLY = "--apply" in sys.argv

rows = json.load(open(os.path.join(ROOT, "data", "stores-data.json"), encoding="utf-8"))
phone_by_slug = {r["slug"]: (r.get("phone") or "").strip() for r in rows}

RE_LD = re.compile(r'(<script type="application/ld\+json">)(\s*\{.*?"@type":\s*"CafeOrCoffeeShop".*?\})(</script>)', re.S)

patched = had = nophone = missing = 0
base = os.path.join(ROOT, "boba", "ca")
for city in sorted(os.listdir(base)):
    cdir = os.path.join(base, city)
    if not os.path.isdir(cdir):
        continue
    for slug in sorted(os.listdir(cdir)):
        pdir = os.path.join(cdir, slug)
        page = os.path.join(pdir, "index.html")
        if not os.path.isdir(pdir) or not os.path.exists(page):
            continue
        phone = phone_by_slug.get(slug, "")
        if not phone:
            nophone += 1
            continue
        s = open(page, encoding="utf-8").read()
        m = RE_LD.search(s)
        if not m:
            missing += 1
            continue
        try:
            ld = json.loads(m.group(2))
        except Exception:
            missing += 1
            continue
        if ld.get("telephone"):
            had += 1
            continue
        ld["telephone"] = phone
        new = m.group(1) + json.dumps(ld, ensure_ascii=False) + m.group(3)
        s = s[:m.start()] + new + s[m.end():]
        patched += 1
        if APPLY:
            open(page, "w", encoding="utf-8").write(s)

print(("APPLIED" if APPLY else "DRY-RUN"),
      "| telephone added:", patched, "| already had:", had,
      "| no phone in data:", nophone, "| no/bad JSON-LD:", missing)
