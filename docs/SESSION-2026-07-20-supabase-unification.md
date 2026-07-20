# Session 2026-07-20 — Supabase unification + expansion

## What changed
- **Data source unified on Supabase.** `gen_profiles_v4.py` (profiles) and
  `build/gen_site.py` (city pages, region hubs, sitemap, intents) now read the
  `niteboba` table in the CoverCapy Supabase project (`hfvbeqlefwwjlrbyxpbj`),
  replacing `data/stores-seed.csv`. Buildable set = 622 shops
  (`status='open'` AND `enrichment_status='enriched'`).
- **407 new profile pages** generated for open shops that lacked one.
- **Full scaffold rebuilt from Supabase:** 167 city pages, 6 region hubs, sitemap.
- **New Ventura County / 805 region hub** (`/area/ventura/`, 28 shops, 8 cities).
  Added `ventura` to `AREAS` (gen_profiles_v4) and `REGIONS` (gen_site).
- **Wave-2 enrichment on profiles:** hero Google rating + review link, price,
  service/parking/good-for amenity rows (truth-gated), stacked linkable Area row
  (city / county / region), ZIP-shared-city links. Area row dedupes when the
  region label equals "{county} County" (Ventura).

## Verification
- 0 broken links: all 622 city-page shop links resolve to a real profile.
- 0 template leaks, 0 JS errors, no horizontal overflow on sampled pages.
- Ventura hub: 28 shops / 8 cities. Sitemap: 174 URLs.

## Decisions
- Ventura county gets its own hub (chosen over folding into Greater LA).
- Move gen_site to Supabase (chosen over hand-building a one-off Ventura page) —
  this is what links the 407 new profiles from city pages / hubs for SEO.

## Traps discovered
- THREE data sources existed: `stores-seed.csv` (gen_site, now replaced),
  `directory/index.html var SHOPS` (nav_data → mega-nav region rail + counts,
  STILL STALE), and Supabase. The nav still shows 334/46 and no Ventura until
  `nav_data`/`directory` is repointed at Supabase.
- gen_site's `render_profile` is disabled (profiles owned by the v4 generator);
  regenerating the scaffold does NOT clobber profiles.
- Supabase `hours.periods` shape matches `norm_periods` as-is.

## Next steps (in order)
1. Repoint `directory/index.html` SHOPS + `nav_data.py` at Supabase, re-stamp
   nav across all pages (shows Ventura + all 622). THE nav fix.
2. Noindex or remove the 119 stale profile pages (99 closed + 12 seed + 8 temp).
3. Regenerate finder-data so the 407 appear as map pearls + "guests from".
4. Retire `stores-seed.csv` and `new-shops.json`.

## How it was built (for future sessions)
- Adapter: `build_sb_missing.py` (cloud) → `sb_shops.json` (407),
  `sb_all_shops.json` (622), merged `enrich.json`.
- Scaffold run: `build/run_sb_scaffold.py` monkeypatches gen_site (adds Ventura,
  swaps load_rows to the Supabase export, output to `_sbscaffold/`).
