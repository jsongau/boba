# SESSION — Date Night Hub rebuild (2026-07-20)

## Shipped
`/best/date-night/` rebuilt from a "Verifying" shell into an interactive, truth-gated hub.
Bespoke page (NOT gen_site-generated — like the homepage, must survive regen): reuses the shared
nav/footer + `/css` + `/js`, adds an inline page `<style>` + `<script>` and a baked
`<script id="dn-data" type="application/json">` (622 Supabase shops, trimmed fields).
Flipped `noindex,follow` -> `index,follow`.

## Sections (all data-gated, real fields only)
Hero + GEO answer lede (names tonight's top 3). Mood finder (Date-worthy / First date / After
dinner / Open late / Weekend late / Near me) filtering 234 date-worthy independents. Ranked picks
(score = rating*ln(reviews)). Five landmark collections (haversine <=4.5 mi, top 6, show if >=4):
Disneyland, Irvine Spectrum, South Coast Plaza, Little Saigon, Old Town Pasadena (HB beach excluded,
1 shop). Self-contained SVG locator map (no Leaflet/tiles dependency). Build-a-date itinerary
(dinner corridor -> nearest date-worthy dessert + drive estimate + copyable plan). Open-late-tonight
and Under-the-radar cuts. Drink-guide rail (links existing /best + /pantry + /guide hubs).
Dessert-after-dinner teaser (links future corridor pages). By-city chips (9). FAQ.
Schema: CollectionPage + ItemList(no ratings) + FAQPage + BreadcrumbList.

## Truth-gating / rules honored
No ambiance data exists (attr_seating / fit / attr_* all empty across 622) -> Quiet/Outdoor/Cozy
render as "Verifying" cards, never guesses. Dropped Luxury (price maxes at $-$$), Instagram-Worthy
(no photos), Trending (no telemetry). "hidden gem" (banned word) -> "Under the radar". Ratings shown
"N on Google", dated, NO first-party aggregateRating schema. Hanzi shop names (安然居 Ān Rán Jū /
潤喉堂 Rùn Hóu Táng) get ruby pinyin + a zh-CN pronounce button. No arrows, no em-dash separators.

## Link coverage (no 404s)
Only 56 / 234 date-worthy shops have committed `/boba/ca/` profiles (178 are among the 407
uncommitted new profiles). Cards link to the profile when committed, else to the shop's city page.
Every link upgrades to a profile automatically once the 407 land — regenerate this page then.

## Data logic
date-worthy = specialty & google_rating>=4.3 & reviews>=25 & latest_close>=2000  (234 shops).
Google hours day 0 = Sunday; HHMM ints; no overnight closes in data. Under-the-radar = specialty &
rating>=4.6 & 25<=reviews<=120. Open-late-tonight = date-worthy & open now (America/Los_Angeles).

## Build
Cloud: `/home/claude/boba/build_preview.py` — `PROD=1` emits the production page (root-relative
assets, index,follow), default emits a self-contained standalone preview. Source data:
`/home/claude/boba/shops.json` (Supabase pull). This page is baked at build; not wired into gen_site.

## Next (in order)
1. Places Details enrichment (needs Jay's Google Places key) -> outdoor_seating, dine_in, reservable,
   good_for_*, editorial_summary, photos -> lights up the Verifying collections + compatibility scores.
2. Child pages: 5 landmark + 9 city, via a gen_site.py extension using the intent-page template.
3. Commit the 407 profiles -> re-run this build so every card links to a profile.
4. Verify the 15 dining-corridor coordinates -> build the "dessert after X" pages.
5. Regenerate sitemap.xml so /best/date-night/ (now index) is listed; repoint nav_data at Supabase
   (nav still shows 334/46, no Ventura).
