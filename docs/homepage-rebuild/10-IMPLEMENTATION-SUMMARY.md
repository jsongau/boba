# 10 — Implementation Summary

_Pass 1 of the homepage rebuild. Honest scope: this delivers the real data foundation and the Craving Cup hero (the signature interaction), plus Spin the Straw and Boba Pulse, wired to sourced menus. It is not the full 17-step deliverable; remaining modules, palette rollout, route extraction, more chains, and the screenshot/QA docs are listed under "Not done yet."_

## Files created
- `docs/homepage-rebuild/00-CURRENT-BUILD-AUTOPSY.md`
- `docs/homepage-rebuild/03-BOBA-MENU-AND-MARKET-RESEARCH.md`
- `docs/homepage-rebuild/10-IMPLEMENTATION-SUMMARY.md` (this file)
- `data/menus/chains/7-leaves.json`, `sharetea.json`, `kung-fu-tea.json`, `tastea.json`
- `data/homepage/featured-drinks.json`, `featured-shops.json`, `source-map.json`
- `data/research/source-ledger.csv`

## Files changed
- `index.html` — added the **Craving Cup "arcade" hero** as the new first screen (new soda-shop palette, Space Grotesk display font); demoted the old finder (H1 → H2, dropped the forbidden "Find your boba, fast." headline); relabeled the shop grid heading to "Browse all 321 shops" so it reads as the exhaustive list below the fold, not the star.

## Files removed
- None. The 321-shop grid is demoted below the hero, not deleted (still crawlable).

## Data sources added
Four chains, official-first, checked 2026-07-01, full provenance in `source-ledger.csv`: **7 Leaves Cafe** (7leavescafe.com), **Sharetea** (1992sharetea.com + DoorDash first-party), **Kung Fu Tea** (kungfutea.com + DoorDash first-party), **Tastea** (gotastea.com). 42 drinks, mapped to **20 real locations** already in the directory. Caffeine/dairy only where a source states it; prices null (none verified).

## Interactions implemented (this pass)
- **Craving Cup** — draggable pearl on a 2D taste pad (refreshing↔creamy, mellow↔tea-forward), Familiar/Either/Adventurous mood, a no-drag preset `<select>`, and **arrow-key** support. As taste changes: the SVG cup recolors by drink category, and the recommendation updates to a **real drink on a real chain's menu at a real shop**, with a plain-language "why it fits," a **See menu** link (official source), **Directions** (Google Maps search), **Save** (localStorage), **Share** (Web Share API + clipboard fallback), and **Another match**.
- **Spin the Straw** — replaces the shop-only randomizer; returns a real drink + real shop + a meaningful **backup**, honoring the mood and city constraints. No `Math.random()` over unverified data.
- **Boba Pulse** — honest context from the client clock + selected city (time of day, which sourced chains are in that city). No open/closed, distance, or demand claims.
- **Progressive enhancement** — a real default recommendation (7 Leaves Oolong Milk Tea at 7 Leaves Cafe, Irvine) is **server-rendered in the HTML**, so the first screen is crawlable and useful with JavaScript disabled; JS only enhances.

## Known limitations (stated plainly)
- Only **4 chains** sourced so far (brief asks for 25). The Craving Cup city list is limited to cities that have these chains, precisely so every recommendation stays real. ~183 independent shops and the other chains have no menu data yet.
- **No hours / open-now / distance / price** anywhere in the hero — none are verified. The result card omits them by design (this is how the repeated "Hours verifying" clutter gets removed honestly).
- The **new palette is on the hero only**; the rest of `index.html` and the 400+ generated pages still use the current skin. Full rollout is a follow-up.
- The 321-grid is **demoted, not yet extracted** to a dedicated `/directory/` route.
- **Modules not yet built:** Boba Battle, Menu Drop Radar, Boba Crawl Builder, Taste Passport, Chain Constellation, Send the Plan. (Live now: Craving Cup, Spin the Straw, Boba Pulse.)
- **Mega-nav** not yet restructured to Discover/Menus/Chains/Cravings; existing nav retained (it is already crawlable).
- **Not produced:** research docs 01, 02, 04, 05, 06, 07, 08, 09, the asset ledger, and the 8-breakpoint screenshots + visual QA — screenshots can't be captured in this environment (no browser-render tool), so those are owed as a separate pass.

## Remaining verification work
- Source the remaining priority chains; several (Sunright, OMOMO, Gong cha, Tiger Sugar, etc.) are **not yet in the directory** and need rows first.
- Deploy the `boba-enrich` Edge Function to get hours + coordinates; only then can open-now and distance appear (honestly) in the result card and grid.
- Build `/menus/{chain}/` pages from the chain JSON and link them from the hero + nav.
- Add the image/asset strategy + `asset-ledger.csv` before any drink photography is shown.

## Commands
- **Local run:** `cd boba-repo && python3 -m http.server 8000`, then open `http://localhost:8000/` (profile links resolve on a served site).
- **Regenerate generated pages:** `python3 gen_site.py` (the homepage is hand-authored, not generated).
- **Deploy:** commit and push to `jsongau/boba`; Vercel auto-deploys.

## Routes to test
`/` (Craving Cup hero, Spin the Straw, grid below), several `/boba/ca/{city}/{shop}/`, `/cities/`, `/best/`, `/near/`, `/tools/`.

## QA run this pass
0 banned words (copy + menu data), 0 stray em/en dashes, 0 duplicate IDs, hero JS passes `node --check`, exactly one `<h1>`, all 20 hero location links resolve, SSR default resolves.

---

## Pass 2 — enrichment deploy, security fix, palette rollout, two more modules

**Supabase (live infra changes):**
- Deployed the `boba-enrich` Edge Function (the exact reviewed source; field mask omits rating/reviews). It is ACTIVE with `verify_jwt=true`; it reads `GOOGLE_MAPS_API_KEY` from the Supabase secret at runtime. All 321 `boba` rows are still unenriched seed (0 coords), so invoking it (start `POST {"limit":5}`) is what fills coordinates/hours/phone and flips profiles to indexable. Est. ~$10-15 in Places calls to do all 321.
- Fixed the flagged security advisory: `public.san_diego_dentists` had RLS disabled while every sibling table had it on. Enabled RLS and added anon/authenticated SELECT policies mirroring `public.dentists`, so the finding clears without changing read behavior.

**Palette rollout (all 417 pages):**
- Remapped the `:root` design tokens in `css/site.css` and the homepage's inline token block from the plum/cream "night market" values to the Craving Arcade palette (night-ink chrome, foam reading sheets, arcade neon accents). Because the site is token-driven, this recolors every generated page. Kept the light reading sheets + dark chrome structure so contrast and SEO text are unchanged; verified each accent's usage context (e.g., `--matcha` is only ever a background) so no neon-on-light readability regressions. Also converted 5 hardcoded leftover colors and the grid's monogram-avatar palette to arcade hues.

**Two new modules (`index.html`, arcade palette, on real sourced data):**
- **Boba Battle** — two real drinks head-to-head with flavor/category/caffeine/dairy from official menus, pick-a-winner, a personal (localStorage) tally, and share. No fabricated global vote totals. SSRs a default matchup; JS handles rerolls and picks.
- **Menu Drop Radar** — server-rendered cards for the four chain menus just sourced (each with an official-menu link and the check date) plus seasonal items flagged from official menus (with source links). No "trending" without a signal.

**QA this pass:** 0 banned words, 0 stray dashes, one `<h1>`, 0 duplicate IDs, all three homepage script blocks pass `node --check`, all server-rendered profile links resolve.

**Still not done** (unchanged from Pass 1 except where noted): the remaining chains; extracting the 321-grid to `/directory/`; the other modules (Crawl Builder, Taste Passport, Chain Constellation, Send the Plan); mega-nav restructure; research docs 01/02/04–08; screenshots (no browser-render tool here). Enrichment is deployed but not yet *invoked*, so open-now/distance are still not shown anywhere.
