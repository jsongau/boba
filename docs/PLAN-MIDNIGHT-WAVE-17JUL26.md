# The Midnight Wave — full product plan (17 JUL 2026, evening)

Synthesized from six specialist agents (live UX audit with screenshots, IA,
behavior psychology, profile design, events, design trends). Status: AWAITING
JAY'S APPROVAL. Nothing below is built yet except what wave 1 already shipped
(midnight directory).

## P0 hotfixes (live-site bugs found by the audit — ship first, small diff)

1. Invisible primary CTA: `.btn-mini--solid` renders black-on-black in the
   hero Tonight's Pour card AND two more JS widgets (js/homepage/tonight-pour.js:35,
   concierge.js:100, house-choice.js:52). Specificity bug in
   css/luxury-homepage.css:199 region. The top conversion action on three
   sections is unreadable — on the LIVE site right now.
2. Homepage nav hardcodes "Directory · 322" (index.html:45) while everything
   else says 334. Extend sync_from_supabase.py to own this string everywhere.
3. Banned word shipped: "A small indulgence" chip (js/homepage/concierge.js:14).
   Also rewrite hero headline — "Something exquisite for tonight" says nothing
   about boba/SoCal/directory in the 5-second window.
4. 31 of 34 homepage sections load at opacity:0 (scroll-reveal JS gate) —
   crawlers/reader-mode/failed-JS users get ~10,000px of blank page. Gate
   reveals behind html.js + prefers-reduced-motion; content visible by default.
5. Directory static fallback text "Showing 328 of 328" (pre-JS) — bake 334.
6. Delete archive/boba-profile-v1/v2.html (live public pages; violates the
   no-version-files rule).

## W1 — One site, one nav (kills "three sites in a trenchcoat")

Audit finding: homepage, directory, and profile/tools/meetups each carry a
DIFFERENT nav, brand lockup, and palette. Fix: a single nav generated from one
source (build/gen_site.py) applied to every template.

Structure (IA agent): **SHOPS · BEST FOR · NEW · PICK FOR ME · GUIDES ·
RATINGS & MEETUPS** + persistent search (cmd-K, baked JSON index of shops/
cities/pages/ingredients) + one pink CTA "Tonight". SHOPS panel = left rail
(5 regions + Near a landmark + All 334, with counts) swapping a right city
pane (≤7 cities + view-all). Every panel: one editorial feature cell (the
SHOPS cell is the paid featured slot, labeled). Mobile: 4-slot bottom bar
(Tonight / Shops / Search / Saved) + accordion drawer. Breadcrumbs mirror
canonical hierarchy sitewide with BreadcrumbList JSON-LD.
Disclosure semantics (button + aria-expanded), click-to-open, no role=menu.

## W2 — Homepage: 13.5 screens → ~6, one picker

Audit counted SEVEN competing decision widgets on one page + 12,160px height.
Disposition: KEEP hero (rewritten: identity + proof + search + Tonight's Pour
as right-column hook) · directory entry PROMOTED to screen 2 (it's the
product; currently at 11,000px) · concierge stays as THE one picker (House
Choice merged in) · House Edit as editorial proof · New Pour capped at 3 rows ·
featured Taro Yuan after directory w/ plain "Featured" label (honesty rule) ·
guides as a link strip · trust section closes. KILLED from homepage: Tasting
Flight, Evening planner (→ /tools/), Black Book section (empty-state screen for
every new visitor; lives in nav), First Meet + Pearl Deck (→ /meetups/).
Tonight's Pour becomes date-seeded 5pm rotation (deterministic, no backend).

## W3 — Profile template: the anti-Yelp (biggest wave, biggest payoff)

Spine: breadcrumb → hero with **verification ledger** (dated checkable facts
where Yelp puts stars) → **Tonight strip** (open-now computed client-side from
baked Google-format hours; 213 shops have them) → what-to-order (3 honest
states) → lazy Leaflet map on CARTO dark tiles (keyless, matches theme; 322
shops have coords) → facts panel with provenance stamps → events block →
**nearby rails** (haversine at build time — the endless-night session loop) →
quiet claim band (revenue) → closed-shop epitaph variant (99 shops need it).
JSON-LD upgraded conditionally: geo/telephone/sameAs/hasMap/openingHours.
Data flow: extend Supabase export to full stores-data.json → gen_site bakes
all 334 profiles. THE SEO UNLOCK: profiles with verified hours+coords flip
from noindex to indexable (locked rule 3 satisfied) — 200+ pages enter Google.

## W4 — Events system (the meetups moat)

data/events.json with SERIES (recurring club) + OCCURRENCE (dated instance).
Build-time: /meetups/ restyled midnight in place (don't fork /events/),
cadence chips ("EVERY TUESDAY · 7PM") + computed "Next: Tue Jul 21", per-shop
"Hosts: Sunday Boba Run" badges joined by slug, homepage "This week" strip
that renders ONLY when real occurrences exist in next 7 days, /meetups/submit/
form (requires public listing URL; mailto + GitHub-issue transports), per-series
ICS files + hub-wide subscribe feed, Event JSON-LD as one node per materialized
occurrence (never eventSchedule, never guessed dates). Supabase schema
(events_series / events_occurrences / submissions inbox keyed to niteboba.slug)
specced for the dynamic phase.

## W5 — Engagement layer (behavior psych, ethics-railed)

localStorage schema `bobanight.v1 = {saved[], visited[], quiz, ranks[]}`
(designed now so Supabase accounts are a straight upsert later). Save-pearl on
every card/profile + /black-book page · visited check-ins + per-city completion
meters ("San Gabriel: 12 of 87 houses") · variety badges (Untappd pattern:
push toward NEW venues) · taste quiz → archetype share card (canvas PNG) ·
Fresh Pours weekly Friday drop · Pearl Rank pairwise ranking (Beli pattern,
P1) · measurement via Vercel Analytics custom events with stated kill
criteria. ETHICS RAILS: no fake scarcity, no guilt copy, weekly (never daily)
streak units, everything respects prefers-reduced-motion.

## Motion + texture contract (trends agent)

CSS scroll-driven animations (animation-timeline: view()) — no JS scroll libs ·
cross-document View Transitions for card→profile morphs (CSS-only, progressive)
· timing tokens: 120ms flips / 180-240ms hovers / 300-500ms reveals, expo-out,
30-60ms staggers · film grain as a tiled static PNG (replace the live SVG
turbulence overlay — cheaper paint) · progressive-blur header scrim · sticky
chapter nav w/ scroll-spy on long pages · micrographic marginalia (verification
data as compositional texture — the honesty brand as decoration) · KILL LIST:
preloaders, parallax stacks, hover-only reveals, cursor replacement, infinite
marquees. All motion behind prefers-reduced-motion; transform/opacity only.

## Trade-offs accepted

- Static-first everywhere; localStorage until accounts justify Supabase auth.
- Leaflet + CARTO free tiles over Google Maps embed (keyless, dark, honest).
- events.json hand-maintained until submission volume justifies the tables.
- View Transitions degrade gracefully in unsupporting browsers (hard cut).

## Build order + why

P0 (live bugs, hours) → W1 nav (every template inherits it) → W2 homepage →
W3 profiles (biggest; needs W1's nav + full data export) → W4 events →
W5 engagement. Each wave ships on its own deploy.

## Success criteria

One nav everywhere · homepage ≤6 screens, 1 picker · 200+ profiles indexable
with live open-now · events joined shop↔hub both directions · measurable
session depth (rail CTR, saves/session, Pour return rate).
