#!/usr/bin/env python3
"""Sync the static site from the Supabase warehouse (Boba Night).

Source of truth: Supabase project CoverCapy (hfvbeqlefwwjlrbyxpbj),
table public.niteboba. This script consumes data/stores-status.csv —
a slug,status export of that table — and applies it to every baked-in
surface so the site never claims a closed shop is open.

    python3 build/sync_from_supabase.py            # apply + report
    python3 build/sync_from_supabase.py --check    # report only, no writes

Surfaces updated:
  1. directory/index.html  SHOPS array — per-shop status flags:
       "x":1  permanently closed   "tc":1 temporarily closed
       "vf":1 verified open        (no flag = seed / still verifying)
     plus the shop-count strings on the page.
  2. tools/roulette/index.html SHOPS array — closed/paused shops REMOVED
     (roulette must never send anyone to a dead shop).
  3. index.html nav "Directory · N" label.

To refresh data/stores-status.csv: export slug,status from Supabase
(table editor or SQL: SELECT slug,status FROM niteboba ORDER BY slug).

Deliberately NOT automated: city/area per-page counts (regen via
build/gen_site.py and diff by hand), profile-page closed banners.
The script prints what still needs hand attention.
"""
import csv, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECK = "--check" in sys.argv

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"['\".]", "", s); s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

# 1. load status map -------------------------------------------------------
status = {}
with open(ROOT / "data/stores-status.csv") as f:
    for row in csv.DictReader(f):
        status[row["slug"]] = row["status"]
n_open = sum(1 for v in status.values() if v == "open")
n_closed = sum(1 for v in status.values() if v == "closed")
n_tc = sum(1 for v in status.values() if v == "temporarily_closed")
n_seed = sum(1 for v in status.values() if v == "seed")
total = len(status)
listed_pool = total                     # everything stays listed (Jay's call)
roulette_pool_pred = n_open + n_seed    # roulette never spins closed/paused
print(f"DB: {total} shops = {n_open} open / {n_closed} closed / "
      f"{n_tc} paused / {n_seed} verifying")

# 2. directory SHOPS -------------------------------------------------------
dpath = ROOT / "directory/index.html"
dhtml = dpath.read_text()
m = re.search(r"var SHOPS = (\[.*?\]);", dhtml, re.S)
shops = json.loads(m.group(1))
missing_on_site, flagged = [], {"x": 0, "tc": 0, "vf": 0}
seen = set()
for s in shops:
    seen.add(s["s"])
    st = status.get(s["s"])
    for k in ("x", "tc", "vf"):
        s.pop(k, None)
    if st == "closed":
        s["x"] = 1; flagged["x"] += 1
    elif st == "temporarily_closed":
        s["tc"] = 1; flagged["tc"] += 1
    elif st == "open":
        s["vf"] = 1; flagged["vf"] += 1
missing_in_db = sorted(seen - set(status))
missing_on_site = sorted(set(status) - seen)
new_array = json.dumps(shops, separators=(",", ":"), ensure_ascii=False)
dhtml = dhtml[:m.start(1)] + new_array + dhtml[m.end(1):]
# count strings on the directory page
listed = len(shops)  # only shops that actually have pages
dhtml = re.sub(r">\d{3}</b> shops", f">{listed}</b> shops", dhtml)
dhtml = re.sub(r"Browse all \d{3} shops", f"Browse all {listed} shops", dhtml)
dhtml = re.sub(r"\d{3} shops across", f"{listed} shops across", dhtml)
if not CHECK:
    dpath.write_text(dhtml)
print(f"directory: {flagged['x']} closed-flagged, {flagged['tc']} paused, "
      f"{flagged['vf']} verified-open; {len(shops)} listed")
if missing_on_site:
    print(f"  !! in DB but NOT on site ({len(missing_on_site)}): "
          + ", ".join(missing_on_site))
if missing_in_db:
    print(f"  !! on site but NOT in DB ({len(missing_in_db)}): "
          + ", ".join(missing_in_db))

# 3. roulette SHOPS --------------------------------------------------------
rpath = ROOT / "tools/roulette/index.html"
rhtml = rpath.read_text()
m = re.search(r"const SHOPS = (\[.*?\]);", rhtml, re.S)
rshops = json.loads(m.group(1))
kept, dropped, unmatched = [], [], []
for s in rshops:
    slug = f"{slugify(s['n'])}-{slugify(s['c'])}"
    st = status.get(slug)
    if st is None:
        unmatched.append(slug); kept.append(s)
    elif st in ("closed", "temporarily_closed"):
        dropped.append(slug)
    else:
        kept.append(s)
new_array = json.dumps(kept, separators=(",", ":"), ensure_ascii=False)
rhtml = rhtml[:m.start(1)] + new_array + rhtml[m.end(1):]
if not CHECK:
    rpath.write_text(rhtml)
print(f"roulette: {len(kept)} spinnable, {len(dropped)} closed/paused removed")
if unmatched:
    print(f"  !! roulette entries with no DB match ({len(unmatched)}): "
          + ", ".join(unmatched))

# 4. homepage nav count ----------------------------------------------------
hpath = ROOT / "index.html"
hhtml = hpath.read_text()
hhtml2 = re.sub(r"Directory · \d{3}", f"Directory · {len(shops)}", hhtml)
if not CHECK and hhtml2 != hhtml:
    hpath.write_text(hhtml2)
print(f"homepage nav: Directory · {len(shops)}")

print("\nHand-check still needed: homepage area tiles + written-out counts, "
      "city/area page counts (gen_site.py), profile pages of closed shops.")
if CHECK:
    print("(--check: nothing written)")
