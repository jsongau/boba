# /best/open-late/ — live late-night discovery page (2026-07-20)

Rebuilt everything below the hero into an interactive, Supabase-driven discovery page.
Navbar and hero preserved per brief.

## Architecture (hybrid)
Static shell baked by build/gen_open_late.py, which OWNS this page (gen_site.py now skips the
'open-late' slug in its INTENT loop so it never clobbers this). The live layer in js/open-late.js
reads the CoverCapy niteboba_finder view (publishable key + RLS) for open-now in Pacific time,
the 8 PM to 2 AM time slider, the Leaflet map (1.9.4 + CARTO, same as /near-me/), hidden gems,
shuffle, and the crawl builder. New DB rows appear with no rebuild. The save heart writes to
localStorage bn_saved (seeds future telemetry).

## Files
- build/gen_open_late.py   (--preview <path> | --build)
- build/open-late-data.json (baked buckets, 92 late cities, 40 seed shops, 16 gems; from Supabase)
- css/open-late.css, js/open-late.js
- build/gen_site.py         (one-line skip so gen_site never overwrites this page)

## Data reality
SoCal boba closes 9 to 11 PM, not 2 AM. 450 past 9 PM, 249 past 10, 118 past 11, 40 past midnight,
15 past 1 AM, 6 past 2 AM, ~0 truly 24h. Latest verified: Cha Express, Alhambra (4 AM Fri/Sat).
Rule 1 held: nothing renders without a verified field.

## Gated on backends (honest, not faked)
- Drinks section is educational links to /guide/ and /pantry/ (no per-shop menu data). Unblocks with
  a categories / shop_categories system (Wave A): live "who is serving X tonight" plus /drinks/ hubs.
- Trending omitted (no telemetry). Unblocks with a shop_events table plus edge ingest (Wave B). The
  save heart already writes the signal.

## Regenerate
python3 build/gen_open_late.py --build
Re-pull build/open-late-data.json from Supabase niteboba when shops change (query in claude project docs).

## Next
Add /best/open-late/ to the sitemap. Add a reciprocal "late-night in {city}" link on city pages and
profiles. Wave B (favorites + telemetry) is the next backend task.
