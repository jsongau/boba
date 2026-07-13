# CLAUDE.md — NiteBoba

Operating manual for any AI session working in this repo. Read this first. The
strategy docs live in `docs/` (start at `docs/MASTER.md`); THIS file is the
operational truth. Where an older doc contradicts this file, this file wins.

## What this is

NiteBoba (formerly CapyBoba, rebranded 11 JUL 2026) is a static SoCal boba
directory: 322 shops, 46 cities, 5 regions. Goal: be the source AI answer
engines cite for "best boba near me / open late / date night." The moats are
verified freshness and first-party fit attributes — see `docs/MASTER.md`.

## Source-of-truth map (exact names — these are traps)

| Thing | Where | Notes |
|---|---|---|
| Code + pages | GitHub `jsongau/niteboba` (renamed from `boba` 12 JUL 2026; old URLs redirect), branch `main` | Jay's local clone: `~/Claude/Projects/NiteBoba` |
| Production | Vercel project **bobatime** (team `cover-capy`, id `team_RgXcylGLXtdbEkjyjdtq6p6A`) | PENDING RENAME → `niteboba` (see §Vercel renames below) |
| Duplicate deploy | Vercel project **boba** | Same repo, auto-deploys too. Do NOT treat as canonical; ask Jay before touching. |
| Store database | Supabase project **CoverCapy** (`hfvbeqlefwwjlrbyxpbj`), table `public.niteboba` | NOT the Supabase project named "BOBA" — that holds an unrelated benefits/HR app. |
| Canonical domain in code | `https://niteboba.vercel.app` | Also in `SITE` constant in `build/gen_site.py`. |

## Vercel renames still pending (dashboard-only, 12 JUL 2026)

Two clicks Jay must do at vercel.com (Claude cannot — vercel.com is blocked
in the Chrome extension unless Jay allows it in extension site permissions):
1. Project **bobatime** → Settings → General → rename to `niteboba`.
   This activates https://niteboba.vercel.app, which every canonical URL,
   sitemap entry, and schema block on the site already points at. Until
   then the site is reachable at bobatime-iota.vercel.app.
2. Project **boba** (the duplicate) → Settings → Git → Disconnect, so only
   one project deploys per push. GitHub repo + About link already renamed.

## Deploy

`git push origin main` → Vercel auto-deploys. That's the whole pipeline.
Always tell Jay WHICH Vercel project a deploy lands on (his standing rule).
Commit as `Claude <noreply@anthropic.com>` or GitHub flags the commit unverified.

## The static-site reality (biggest gotcha)

The live site does NOT read Supabase at runtime. All 1,000+ HTML pages are
static, committed to the repo. The directory page (`directory/index.html`)
has the full store list BAKED IN as `var SHOPS = [...]`. The Supabase
`niteboba` table is the warehouse and must be kept in sync BY HAND (or by the
planned sync script). If you change store data, change it in BOTH places.

## Data model (as actually built — `docs/DATA-SCHEMA.md` shows the target)

- Supabase `niteboba`: `slug` (unique, matches site URLs), `name`, `city`,
  `county`, `address`, `store_type` ('chain'|'specialty'), `is_featured`,
  `signature_drinks[]`, `attr_*` booleans, `fit` jsonb, `status`
  ('seed'→'open' after verification), enrichment columns (all empty today).
- Directory `SHOPS` entries: `{n,c,cs,s,ar,ch,f}` = name, city, city-slug,
  shop-slug, area label ('The 626'|'Greater LA'|'Orange County'|'San Diego'|
  'Inland Empire'), chain flag 1/0, featured flag.
- Counts today: 322 shops = 145 chain + 177 specialty, 1 featured (Taro Yuan).
- RLS public-read on `niteboba` only exposes status open/temporarily_closed;
  every row is still 'seed', so anon reads return 0 rows until enrichment.

## Ranking + featured (the monetization lever)

Directory sort is locked: `featured DESC → specialty before chain → A-Z`.
Featured shops get the purple `★ Featured` pill; `--taro` purple is RESERVED
for featured/member placement only (README tokens) — never use it elsewhere.

## How to add a store (until the sync script exists, it's 6 touchpoints)

1. INSERT into Supabase `niteboba` (slug = `kebab(name)-kebab(city)`).
2. Append to `data/stores-seed.csv`.
3. Add entry to `SHOPS` in `directory/index.html`; bump its "322 shops" /
   "46 cities" strings.
4. Create `/boba/ca/{city}/{slug}/index.html` profile (+ city page if new city
   — also update `cities/index.html`, the area page counts, `sitemap.xml`,
   and `SGV_CITIES`/region map in `build/gen_site.py` if applicable).
5. Homepage counts: meta description + "Three hundred and twenty-two rooms"
   heading + area tile numbers in `index.html`.
6. Verify locally (serve + screenshot) before commit.

To feature a store: `is_featured=true` in Supabase AND `"f":1` in `SHOPS`.

## Locked rules (condensed — full text in `docs/MASTER.md` §LOCKED RULES)

1. NO FABRICATION. No invented hours, ratings, reviews, or descriptors.
   Unverified = "Verifying" state or `{{VERIFY: ...}}`, never a guess.
2. Ratings are third-party, attributed, dated, linked — or absent. No
   first-party `aggregateRating` schema until Boba Passport (Phase 3).
3. Shop profiles stay `noindex,follow` until hours+coords are verified.
   City/area pages are indexable. Don't flip noindex early.
4. "Best" lists are labeled opinions ranked on fit, with method shown.
5. Every page carries an `Updated {date}` stamp where present; slugs are
   permanent once published (301 if you must move).
6. Banned words (full list `docs/SITE-SPEC.md` §5): hidden gem, nestled,
   vibrant, indulge, look no further, burst of flavor, premium, curated,
   discover, transform, seamless, elevate, empower, navigate, innovative.
7. Versions are additive (`-v2`, `-v3`), never overwrite; Jay also keeps
   dated work folders like `boba - 11JUL26/` (git-excluded — leave them).

## Corrections to older docs (audited 11 JUL 2026)

- `docs/SITE-SPEC.md` slug example `7-leaves-cafe-jeffrey` is obsolete:
  PUBLISHED slugs disambiguate by CITY (`7-leaves-cafe-irvine`). Follow the
  published pattern; never rename published slugs to match the old spec.
- `docs/DATA-SCHEMA.md` describes a target `shops` table; the real table is
  `niteboba` with slightly different column names (address/zip/latitude…).
  Treat DATA-SCHEMA as the enrichment roadmap, not current truth.
- `docs/MASTER.md` predates the build (2026-06-26): the site is BUILT and in
  production; `/brand/{slug}/` hubs and the freshness engine are still unbuilt.
- README "Status" previously described a two-page preview; the generator
  `build/gen_site.py` is the page factory (regenerates city/intent/profile
  pages from the CSV; run from repo root: `python3 build/gen_site.py`).

## Don'ts

- Don't run bulk regeneration and commit blind — diff first; hand-edited pages
  (Taro Yuan profile, homepage featured section) must survive.
- Don't write to the Supabase project named "BOBA" for anything boba.
- Don't add stores to only one side (site XOR database).
- Don't invent Google ratings on cards — Taro Yuan's 4.1★ is deliberately
  NOT shown (unverified-display policy).
- Don't create new Vercel projects; two already exist for this repo.
