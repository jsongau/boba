# Fun Layer — build log (12 JUL 2026)

What shipped in the interactivity pass, how each module works, and the bugs
fixed along the way. Companion to `docs/PROPOSAL-homepage-nav-fun-12JUL26.md`.

## Nav legibility (P0)

- Relabels on the homepage masthead + mobile drawer: The Concierge → Concierge,
  Tea Houses → **Directory · 322**, The Menu → Drinks, The New Pour → New
  Openings, Black Book → Saved ♥. Section ids/anchors unchanged, so no links
  broke. Dropdown mega-panels untouched.
- **Desktop header search** (`.nav-search`, wired in `js/homepage/navigation.js`)
  → submits to `/directory/?q=…`. Hidden ≤1240px (drawer search covers mobile).
- **Directory now honors `?q=`** — previously the drawer search navigated to
  /directory/?q=X and the page ignored it. It now seeds the filter, fills the
  input, and scrolls to the grid.
- **Dead /search route fixed** — the directory's Enter handler used to navigate
  to `/search?q=` (a page that does not exist). It now filters in place.
  NOTE: SearchAction schema on the directory still points at /search; either
  build /search later or repoint the schema (tracked, low priority).

## Hero

- Added "Can't decide? Spin" (`btn-line`) → `/tools/roulette/` next to the
  concierge CTA.
- **Bug fix — focus scroll-hijack:** `concierge.js` focused the first quiz
  option on initial render, which scrolled every visitor past the hero on page
  load (the page appeared to "start" at Four Questions). Focus now happens only
  after first user interaction, with `preventScroll`.

## First Meet + The Pearl Deck (`#first-meet`, `js/homepage/first-meet.js`)

The Tinder-match use case: two people matched, need a low-pressure first hang.
- **Energy picker** (3 options) → editorial recommendation line + link to the
  matching intent page: Keep it easy → `/best/first-date/`, Make it playful →
  `/best/with-food/`, Already 9pm → `/best/open-late/`. No shop facts asserted
  — routing only, so no honesty-rule exposure.
- **The Pearl Deck**: 24 editorial conversation cards, shuffled per load, dealt
  without repeats. Keyboard accessible (card is a focusable button; Enter/Space
  deal). Content is opinion/prompt-only — nothing verifiable, nothing banned-list.
- Styling appended to `css/luxury-homepage.css` (`.fm-*`); `--taro` purple used
  only as the selected-state accent, consistent with the featured-only rule.

## Meetups (shipped 12 JUL 2026)

- `/meetups/` page (indexable, in sitemap, linked from Guides mega + drawer +
  First Meet) + Supabase `niteboba_meetups` table (9 seeded rows) listing clubs and
  recurring events that meet at SoCal boba/tea shops. Every listing requires a
  `source_url`; cadence/details show only what the source states; unverified
  details render as "check their page." See `docs/MEETUPS-RESEARCH-12JUL26.md`
  for findings + sources.

## Round 2 layers (same day)

- **Tonight's Pour** (`js/homepage/tonight-pour.js`): the hero selection now
  rotates DAILY AT 5 PM, deterministically (date-seeded) across the 66 sourced
  SOCIETY drinks + a real location of that chain. Tags render only what the
  source states (caffeine/dairy unknown = no tag). Source line rebuilds per
  chain. Static HTML stays as the no-JS fallback. Freshness signal, zero backend.
- **The Order Oracle** (`/tools/order-oracle/`): 5-question personality quiz →
  8 personas (Loose-Leaf Purist, Brown Sugar Maximalist, Fruit Tea Optimist,
  Matcha Devotee, Topping Collector, Late-Night Regular, One-Order Loyalist,
  Seasonal Chaser). Each result: verdict + "your order" + 3 intent links + a
  1080x1350 canvas share card (Save/Send via Web Share API). All editorial —
  the page literally says "The Oracle deals in opinions, not facts."
  Entry points: Tonight mega, drawer, First Meet, tools index, sitemap.
- **Pearl Deck "Send this card"**: shares the current icebreaker with
  attribution via CBS.share.

## Round 3 layers (13 JUL 2026)

- **The Date Night Planner** (`/tools/date-planner/`): the flagship interactive.
  Pick area + energy → deals a 3-stop night: a drink spot, a dessert house
  (falls back to a "second pour" in the 2 areas with no dessert house yet — IE,
  SD), and "the after" linking to the right intent page. Renders a 1080x1350
  canvas share card ("Tonight in {area}"), Save/Send via Web Share API.
  Powered by an embedded 328-shop dataset (name/city/area/slug/chain/dessert/
  featured), seeded PRNG so re-deals vary. Honesty: every stop is a real shop,
  each shows "Hours verifying" + links to profile/Google — the page states
  "the itinerary is a plan, not a promise the doors are open." Entry points:
  Tonight mega, drawer, First Meet, tools index (first card), sitemap.
  Built via build/add_spots.py NOTE: the planner has its OWN embedded SHOPS
  array (8th surface) — regenerate it from directory+roulette data when the
  store list changes (see the /tmp gen in this session, or rebuild by hand).

## Verification

All changes render-tested locally (Playwright screenshots): hero with Spin CTA,
nav single-line at 1440px, First Meet deck dealing, `/directory/?q=taro`
filtering to the featured card. JS syntax-checked with `node --check`.
