# SESSION 2026-07-23 — SoCal/OC profile-page + hub fill

## What changed
- Generated **388 v4 profile pages** for every open shop from the recent SoCal fill
  (373 across ~84 cities) + the deep Chino/Chino Hills/OC-Irvine pass (15) that did
  **not** already have a page. IE's 132 pages already existed from the prior wave, so
  they were skipped. 0 generation errors.
- Generated **20 new city hubs** for the cities that gained shops but had no hub:
  avila-beach, bakersfield, chatsworth, fort-irwin, goleta, grover-beach, isla-vista,
  ladera-ranch, laguna-beach, lompoc, morro-bay, newport-beach, paso-robles,
  pismo-beach, rancho-palos-verdes, san-luis-obispo, santa-barbara, santa-maria,
  solvang, valley-center. (87 distinct city-slugs across the 388 pages; 172 hubs
  already existed; 67 of the 87 already had a hub, leaving 20 to create.)
- All 408 files committed to the one live repo. Pages are **noindex,follow** by
  design (verify gate); hubs are index (they match the live eastvale hub exactly).

## How it was built
- Pages: `build/gen_profiles_v4.py` driven offline via `NBV4_SAMPLE=<open_sample.json>`
  (the full 1,529-row open-shop sample pulled from Supabase). Driver:
  `gen_missing.py` — generates only slugs not in `build/_haspages.txt` and not in
  `G.SKIP_SLUGS`. Dedup slugs (e.g. `7-leaves-cafe-irvine-6217bb`) are the v4
  generator's own collision suffixing, so re-runs are safe.
- Hubs: `gen_hubs2.py` — imports `build/gen_site.py` with a **stubbed `nav_data`
  module** (see trap) and the baked header lifted from the live `boba/ca/eastvale/`
  hub, then calls `G.render_city(...)` per missing city. Region map built from the
  same open_sample via `G.region_of` / `G.slugify`.

## Decisions
- **Scoped this commit to pages + hubs only.** Map wiring (finder-data.js /
  near-index.json), sitemap regen, and the noindex->index flip are deliberately
  held for a verify pass — the pages ship crawlable-but-noindex so nothing
  half-verified enters the index.
- Reused the eastvale baked header for new hubs rather than repairing `nav_data`,
  so hub chrome is byte-identical to live hubs without touching the broken pipeline.

## Traps discovered (for the next session / any AI)
- `build/gen_site.py` imports `nav_data`, which reads `directory/index.html` for a
  `var SHOPS` blob that no longer exists there — **import fails**. Workaround:
  inject a stub `nav_data` module via `sys.modules` whose `render_header()` returns
  a header string lifted from an existing live hub. The mega-nav **counts in that
  baked header are stale** (626=123, OC=93, etc.) and will stay stale until
  `nav_data` is repointed at Supabase. Separate, pre-existing follow-up.
- **Bridge git can't unlink `.git/index.lock`** ("Operation not permitted"), so
  normal `git add`/`commit` through the device VM strands a lock. Reliable path is
  the **plumbing commit**: `GIT_INDEX_FILE=/tmp/idx git read-tree HEAD; git add -A
  <paths>; TREE=$(git write-tree); COMMIT=$(git commit-tree $TREE -p HEAD -m ...);
  printf '%s\n' "$COMMIT" > .git/refs/heads/main; cp /tmp/idx .git/index`.
- **device_bash sees the repo at the mount `mnt/NiteBoba`, NOT the raw
  `/Users/kytlegacy/...` path** (that raw path is only for device_list_dir /
  device_commit_files). device_bash also **cannot `rm`** — move unwanted files to
  `_to_delete/` instead.

## Exact next steps
1. **Verify + flip to index.** Spot-check ~15 of the 388 (open hours, rating
   attribution, no null fields, map centers right), then flip the v4 `robots` meta
   from `noindex,follow` to `index,follow` and regen. This is the SEO unlock — the
   388 pages earn nothing while noindex.
2. **Wire the new shops into the map.** Regenerate `js/finder-data.js`
   (window.FINDER_DATA) + `js/near-index.json` via `build/gen_finder_data.py` with
   the same open_sample so the new shops appear as pins in the near-me finder.
3. **Sitemap.** Once indexable, add the 388 pages + 20 hubs to `sitemap.xml`.
4. **nav_data repoint.** Fix `build/nav_data.py` to read Supabase (not the dead
   directory blob) so mega-nav region/city counts reflect the real ~1,500 shops.
5. **Pinyin ruby.** All-Chinese shop names (e.g. the Diamond Bar shop reslugged to
   `ri-qing-liang-yue-diamond-bar`) should render hanzi + pinyin ruby, matching the
   date-night hub treatment.

## Stack / approach note
Static generated pages, Supabase as source of truth, offline generators driven by a
JSON sample env var, universal chrome kit (nav.html/footer.js + 4 CSS files) so
generated pages carry zero baked chrome. Commits via git plumbing over the device
bridge; pushes run by Jay in real Terminal (sandbox has no GitHub auth).
