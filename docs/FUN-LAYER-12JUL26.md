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

## Verification

All changes render-tested locally (Playwright screenshots): hero with Spin CTA,
nav single-line at 1440px, First Meet deck dealing, `/directory/?q=taro`
filtering to the featured card. JS syntax-checked with `node --check`.
