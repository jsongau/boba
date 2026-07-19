# Session — Nearby Finder shipped to /nearby/ (2026-07-19)

## What changed and why
Shipped the long-iterated "boba near me" finder as a **new standalone page** at `/nearby/index.html`
instead of surgery on the live homepage. Rationale: the header/finder went through ~11 design rounds
(Pearl Line, single-row, cherry drag-meter, Taro Yuan universal-search floater). Landing it as its own
page gives a live, shareable URL to pressure-test the finder on real data with **zero risk** to the
homepage or the other 438 pages. Homepage/site-wide rollout is a deliberate second step, not this one.

## The page
- Source of truth for the build: `boba-1-pearl-line-v3.html` (approved v3).
- Header: brand · Shops / Best for / New / Pick for me (mega dropdowns, 2-state hover SVGs) · cream
  City/ZIP field · collapsible "5 mi" chip revealing the cream miles meter (cherry handle, drag right =
  farther, 1–20, chip label live-syncs) · Closest/Open sort · sound · Guides + Ratings (right of search) ·
  Tonight CTA.
- Taro Yuan floater = universal search over shops + a PAGES index + ingredients, grouped + highlighted.
- Body: production hero (banned-word-free), Browse-by-region (5 real /area/ links), How-the-finder-works,
  Keep-looking (links to /best/, /guide/, /cities/).
- SEO: `index,follow`, canonical `https://www.bobanight.com/nearby/`, OG/Twitter tags,
  JSON-LD WebSite+SearchAction and BreadcrumbList.
- Data: inlined `var DATA` (322 shops) left byte-identical (md5 `bc29f344d082`).

## Decisions made / rejected
- REJECTED: editing the live homepage header in place for this deploy — too high-risk for a first ship.
- REJECTED: reusing `/near/` — that path is the landmark set (Disneyland/UCI/UCLA). `/nearby/` is proximity.
- CHOSE: distinct `/nearby/` slug so both concepts coexist and both are indexable.

## Traps discovered
- The inlined `var DATA` (~220KB single line) must stay byte-identical or the engine breaks — guarded by
  md5 on every edit (bc29f344d082).
- Meter drag is bound to **pointerdown**, not mousedown — synthetic mouse-event tests are no-ops; use
  Playwright real pointer drag to verify.
- Repo root has many untracked junk artifacts (`*.bundle`, `card-*.png` ~3MB) — never `git add -A`;
  add only the intended paths or they deploy and bloat the repo. (Candidate for .gitignore next session.)

## Exact next steps
1. Verify live at https://www.bobanight.com/nearby/ after Vercel builds.
2. Backend/growth (highest leverage, still unbuilt): run `scrape_boba.py` with the Google Places key to
   fill the 77 empty SoCal cities, then link those city pages into the finder + sitemap.
3. Site-wide rollout: port the Pearl Line header into `build/nav_data.py` / `apply_nav.py` so all 438
   pages share it (only after /nearby/ proves out live).
4. Add `*.bundle` and `card-*.png` to `.gitignore`.
