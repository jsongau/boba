# 00 — Current Build Autopsy

_Reviewed from the attached project ZIP (identical to the live build). Date: 2026-07-01._

## 1. How the homepage is generated
Two separate systems produce the site:

- **`index.html`** (the homepage) is **hand-authored**. It is a single self-contained file: ~500 lines of inline `<style>`, the markup, then two inline `<script>` blocks (nav behavior + the directory grid). It embeds all **321 shops** as a JSON array directly in the page. It does **not** go through the generator.
- **Every other page** (321 profiles, 45 city pages, 5 region hubs, vibe/landmark/guide/legal pages, `/tools/` hub) is produced by **`gen_site.py`**, a Python static-site generator that reads `data/stores-seed.csv` and writes HTML into the repo. All generated pages share **`css/site.css`**.

There is no framework, no bundler, no server. Output is plain static HTML/CSS/JS deployed on Vercel from the `jsongau/boba` GitHub repo.

## 2. Which files control the homepage
- `index.html` — all homepage markup, inline CSS, inline JS, and the embedded 321-shop dataset.
- `css/site.css` — **not** used by the homepage (homepage CSS is inline); it controls the generated pages. The homepage duplicates a "Liquid Night Market" token set inline.
- No shared JS modules; homepage JS is inline and bespoke.

## 3. Code worth preserving
- **The generator (`gen_site.py`)** and all generated pages — this is the SEO surface and it is sound.
- **`css/site.css`** as the shared system for generated pages.
- The **header + mega-nav + mobile drawer markup and JS** in `index.html` (real, crawlable navigation with dropdowns; keyboard-driven).
- The **footer** and **JSON-LD** (WebSite/Organization) blocks.
- The **honesty scaffolding**: `/how-we-rank/`, `/how-we-make-money/`, no stored ratings, "verifying" states rather than invented data.

## 4. Code to delete or refactor
- **The embedded 321-shop array + the entire directory grid should move off the homepage** into a dedicated `/directory/` route (or reuse `/cities/`). Shipping 321 records + grid logic inline on `/` is the "searchable spreadsheet" problem and bloats the initial payload.
- **Inline homepage CSS/JS should be extracted** to `css/homepage.css` and `js/homepage/*.js` for maintainability (currently one monolith).
- **Repeated "Hours verifying" chips** in the discovery experience should be removed; lead with data we actually have (the drink + a real menu link), not the field we lack.
- **The randomizer ("Surprise me")** currently picks a shop only, via `Math.random()` over the array. Replace with a constraint-aware picker that returns a shop **and** a real drink **and** a reason.

## 5. Routes that must remain stable (do not break crawlability)
`/`, `/boba/ca/{city}/{shop}/` (321), `/boba/ca/{city}/` (45), `/area/{region}/` (5), `/best/`, `/best/{vibe}/` (12), `/near/`, `/near/{landmark}/` (8), `/guide/`, `/guide/{slug}/` (6), `/new/`, `/new/{region}/`, `/cities/`, `/tools/`, `/tools/{roulette,drink-matcher,build-your-sip}/`, `/about/`, `/how-we-rank/`, `/how-we-make-money/`, `/report/`, `/claim/`, `/privacy/`, `/terms/`, plus `sitemap.xml`, `robots.txt`, `llms.txt`. The homepage rebuild must keep linking these.

## 6. Weak homepage sections (today)
- Hero is a compact finder + search — useful but not craving-creating; no drink, no recommendation, no immediate manipulation.
- The dominant element is a 321-card directory grid — exhaustive listing, not discovery.
- Monogram (initials) cards — no drink imagery, low appetite.
- "Hours verifying" repeated across cards — reads as unfinished.
- Tools are links out, not on-page experiences.
- No sharing/return loop on the homepage beyond localStorage saves.

## 7. Which data is real
- Per shop: **name, city, address, county/region, chain-vs-independent** (classified), and a stable **profile URL**. That is the complete set of trustworthy per-shop facts today.
- **45 cities, 5 regions, 8 landmarks, 12 vibe categories, 6 guides** — real taxonomy.
- Chain/independent split: **138 chains / 183 independents** across 321 shops.

## 8. Which data is missing
- **Menus / signature drinks / categories / toppings / sweetness / ice** — none per shop.
- **Hours, open-now, coordinates, distance, phone verification, price, caffeine, dairy** — none (the Google Places enrichment function is written but not yet deployed; even it would not provide menus).
- **Per-location drink availability** — not verifiable per store.

## 9. Interactions that are fake, shallow, or incomplete
- Randomizer picks a shop but **no drink** and **no reason**.
- Grid "open/hours" is not shown because it does not exist; the "verifying" chip stands in for it.
- No real recommendation engine; no taste input; no comparison; no group/share flow on `/`.

## 10. How the rebuild preserves crawlability
- Keep `/` **server-rendered** (static HTML) with a real default recommendation card, real chain links, city links, drink/menu links, guide links, and headings present in the HTML — JS only **enhances** (Craving Cup interactivity, filtering, sharing).
- Move the exhaustive 321 grid to `/directory/` (still linked, still crawlable) so `/` is discovery-first.
- Add **chain menu pages** (`/menus/{chain}/`) generated from the new sourced menu data, and link them from the homepage and mega-nav — net new crawlable surface with real content.
- The new visual system and hero are additive to the existing generator; generated pages keep `css/site.css`.

## Key architectural constraint driving sequencing
The craving-first modules (Craving Cup, Spin the Straw, Boba Battle, Menu Drop Radar) all require a **real menu dataset**, which does not exist. Therefore the rebuild's first real step is to **compile official chain menus with sources** (`data/menus/chains/*.json`, `data/research/source-ledger.csv`), then build the hero on top. Chain-level menu facts (a drink that is on a chain's official menu) are defensibly real when matched to that chain's locations already in the directory. This is the honest bridge that unblocks the whole homepage vision.
