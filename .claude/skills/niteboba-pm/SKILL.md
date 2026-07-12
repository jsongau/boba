---
name: niteboba-pm
description: >-
  Operations manual and project manager for the NiteBoba site (formerly
  CapyBoba) — the SoCal boba directory. Use this for ANY work on the boba
  site or directory — deploying or pushing it, adding/editing/featuring a
  boba shop (e.g. Taro Yuan), chains vs specialty classification, the
  Supabase niteboba table, store counts, directory or ranking changes,
  enrichment or verification work, or questions like "is the boba site
  live", "add this shop", "feature this store", "update the directory".
  Trigger even for vague asks like "update my boba site" or when Jay pastes
  a boba shop's Google listing. The repo's CLAUDE.md carries the same truth;
  this skill exists so sessions WITHOUT the repo attached still know the map.
---

# NiteBoba PM — ops, data rules, and release

NiteBoba is a static SoCal boba directory (322 shops, 46 cities). The win
condition is being the source AI engines cite for "best boba near me / open
late / date night." Freshness + honest data are the moats. Jay owns it;
treat him as the QA gate.

## Source-of-truth map (exact names — several are traps)

- **Repo:** GitHub `jsongau/boba`, branch `main`. Jay's local clone:
  `~/Claude/Projects/NiteBoba` (ask him to connect this folder for file work).
- **Production:** Vercel project **bobatime** (team `cover-capy`) — may be
  renamed **niteboba**. A duplicate Vercel project **boba** deploys the same
  repo; it is NOT canonical. Never create new Vercel projects.
- **Database:** Supabase project **CoverCapy** (`hfvbeqlefwwjlrbyxpbj`),
  table `public.niteboba`. The Supabase project literally named "BOBA" is an
  unrelated benefits app — never write boba data there.
- **Canonical domain in code:** `https://niteboba.vercel.app`.
- Deploy = `git push origin main` (auto-deploy). Per Jay's standing rule,
  always confirm WHICH Vercel project a deploy lands on before pushing.
  Commit as `Claude <noreply@anthropic.com>` (verified-commit hook).

## The static-site reality (biggest gotcha)

The live site does NOT read Supabase. All pages are static HTML in the repo;
the directory page (`directory/index.html`) bakes the store list in as
`var SHOPS = [{n,c,cs,s,ar,ch,f}, ...]` (name, city, city-slug, shop-slug,
area label, chain flag, featured flag). Supabase `niteboba` is the mirror
warehouse. Any store change must land in BOTH, or they drift.

## Ranking + tiers (the monetization lever)

Directory sort is locked: `featured DESC → specialty before chain → A-Z`.
`store_type` ∈ {chain, specialty}; `is_featured` / `"f":1` marks featured
houses (first: Taro Yuan, City of Industry). Purple `--taro`/#6b21a8 is
reserved exclusively for featured placement. Featured slots, claim-to-upgrade,
and chain menu partnerships are the revenue models — protect their integrity.

## Add a store (6 touchpoints until the sync script exists)

1. INSERT into Supabase `niteboba` — slug = `kebab(name)-kebab(city)`
   (city-based, matches published URLs; slugs are permanent once live).
2. Append to `data/stores-seed.csv`.
3. Add to `SHOPS` in `directory/index.html`; bump "322 shops"/"46 cities"
   strings there.
4. Create `/boba/ca/{city}/{slug}/index.html` (copy an existing profile).
   New city? Also: city index page, `cities/index.html`, area page counts,
   `sitemap.xml`, region map in `build/gen_site.py`.
5. Update homepage counts (meta description, the spelled-out
   "Three hundred and twenty-two rooms" heading, area tile numbers).
6. Serve locally + screenshot to verify before committing.

Feature a store: `is_featured=true` in Supabase AND `"f":1` in `SHOPS`;
homepage "featured house" section links to its profile.

## Honesty rules (non-negotiable, they ARE the brand)

- No invented hours, ratings, reviews, or shop descriptors — ever.
  Unverified fields show "Verifying"; menu items only from official sources,
  with the source linked. Third-party ratings only with attribution + date +
  link (Taro Yuan's 4.1★ is deliberately NOT displayed).
- Shop profiles stay `noindex,follow` until hours + coordinates verified;
  city/area pages are indexable.
- Banned words: hidden gem, nestled, vibrant, indulge, look no further,
  burst of flavor, premium, curated, discover, transform, seamless, elevate,
  empower, navigate, innovative. (Full list: `docs/SITE-SPEC.md`.)
- "Best" lists are labeled opinions ranked on fit, method shown.

## Release checklist

1. Working tree clean, commit message says what shipped.
2. Confirm target: Vercel **bobatime/niteboba** (not the duplicate "boba").
3. Push → wait for READY → spot-check live: homepage logo "NiteBoba",
   directory first card + counts, any page you touched.
4. If store data changed: verify Supabase matches (`select count(*),
   count(*) filter (where store_type='chain') from niteboba;` — expect
   drift = a bug).
5. Jay's conventions: dated work folder (`boba - 11JUL26/`) with v1 backups
   for reworked pages; save a session .md to the Boba project if the logic
   got deep.

## Current state + roadmap anchors (11 JUL 2026)

322 = 145 chain + 177 specialty, 1 featured. All rows status='seed' —
enrichment (geocode, hours, place IDs) not yet run; that's the top backend
priority because it flips profiles indexable and unlocks "open now" — the
NiteBoba signature feature. Next-highest: the Supabase→site sync script
that collapses the 6-touchpoint surgery to one INSERT + one run.
Repo docs: `CLAUDE.md` (operational truth) → `docs/MASTER.md` (strategy).
