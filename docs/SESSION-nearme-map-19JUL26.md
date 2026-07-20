# SESSION-nearme-map-19JUL26 — /near-me/ finder ships to the homepage

## What changed and why
- New page `near-me/index.html` (self-contained ~264KB): the map-first finder. Fullscreen CARTO dark Leaflet map
  (offline SVG fallback baked in), search pill with city/ZIP + shop-name typeahead, GPS "Near me", draggable search
  (pink center pin moves it, gold edge handle resizes 1-30 mi), filters with live facet counts (radius, open now,
  Local/Chains, rating 4.0+/4.5+, 200+ reviews, Near a park, Near a dog park), custom SVG pins (gold-lid cups = local,
  silver = chain, guava drink = open now; trees = parks, paws = dog parks, legend doubles as layer toggles,
  pins clipped to the radius), and a right-side drawer with Overview / Stroll / Hours tabs (sticky while browsing).
  Stroll always pins the nearest dog park (to 4 mi) and park (to 3 mi) with walk minutes + walking routes.
- Homepage `index.html`: one additive line button in the hero find-row: "Open the boba map" -> /near-me/.
- Data baked at build time from Supabase niteboba (215 OPERATIONAL shops with coords; 99 closed filtered out) +
  map_anchors (177 SoCal anchors) + 25 seeded central-LA/Westside/LB/SD parks. Google reviews link out via
  google_place_id (search.google.com/local/reviews) — no ratings stored beyond what profile pages already show.

## Decisions
- Drawer quick-view first, static profile behind "See the full page" (SEO pages stay the destination; the map is a funnel).
- Reviews/ratings shown live-linked, consistent with the no-stored-stats rule.
- /near-me/ chosen over /near/ (that is the landmark hub). Page is indexable; gen_sitemap.py picks it up automatically.
- Duplicate Vercel project "boba" still auto-deploys this repo (CLAUDE.md); bobatime is canonical.

## Traps discovered
- hours jsonb open_now is a scrape snapshot — the page computes open-now live from periods in America/Los_Angeles.
- 25 seeded park coords are from model knowledge, marked for a Places verification pass BEFORE promoting them into
  Supabase map_anchors (do not sync unverified; map_anchors may feed CoverCapy surfaces).
- The finder build chain lives in the cloud session (shops/cities/anchors JSON + build.py prerender); fold into
  build/ scripts when the data pipeline moves into the repo.

## Next steps
1. Places verification for the 25 seeded parks, then optional map_anchors sync (needs Jay approval).
2. Enrich js/near-index.json (rating, price, periods, store_type, place_id) and swap shop-page map popups for the
   shared drawer, so profile pages get the same quick view.
3. "Open late" filter wired to /best/open-late/. 4. app.bobanight.com domain add on bobatime if wanted.
5. The 77 empty cities + 122 noindex profiles still wait on the Places scrape (biggest SEO lever, per pm8).
