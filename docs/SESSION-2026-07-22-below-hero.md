# Session 2026-07-22 — Homepage below-hero redesign, production splice

## What shipped
The full below-hero redesign (19 preview iterations, boba-full-preview v1→v19) spliced into production:

- `index.html`: hero edits (search form and proof line removed, animated map-card CTA), meta/schema counts 334/46 → 998/169, duplicate ty-float/dock block removed (pre-existing live bug: duplicate IDs made one search box dead), bulk floater recopy ("Boba for the whole crew" / "One jug pours the whole table." / single Tastea Partea Jugs link), below-hero replaced by `<div id="bh">` (13 sections + SVG sprite + saved bar), footer replaced by `.ft2`.
- `css/below-hero.css` (new): all section CSS scoped under `#bh` (site tokens redefined on the container so nothing leaks), plus unscoped chrome: `.btn-map` hero card, compact `.feat-float`, `.ft2` footer, saved-bar offset.
- `js/below-hero.js` (new): SEED fallback (337 shops) + GAZ gazetteer inline, live fetch of `niteboba_finder` (998 rows) re-renders everything, all section logic, conveyor beltify, chains toggle, chrome live-counts script (hero sub, search empty text, "All N" links, footer stat row).
- `js/nav-midnight.js`: appended search-floater gating (IntersectionObserver on #tonight, scroll fallback on other pages, sessionStorage dismiss + legacy localStorage cleanup).
- `css/finder.css`: appended `.ty-float` gated-entrance styles.
- `docs/copy-voice.md` (new): researched engagement-language guide; also installed as the `boba-night-copy-voice` skill.

## Section order
locate → opennear (vibe+region filter chips) → directory (live counts) → gallery (sushi conveyor: Trending belt RTL + Worth the Drive belt LTR, omakase toggle) → cad → concierge → houseedit → drinks (dark, custom icon sprite) → afterten → spin → social-calendar (calendar CTA card) → houseguide → keep (one-line icon pill rail).

## Decisions made
- Conveyor variant C ("Midnight Express": tilted crossing belts, pink-gold dash rail) chosen over A (hairline belts) and B (gilt frame).
- Chains excluded from the belts BY DEFAULT; "Omakase · independent houses only" ↔ "Full counter · chains on the belt" toggle. Revisit if bounce data suggests people miss familiar chains.
- Vibe taxonomy is DERIVED from real data (hours/rating/reviews/name/type), never stored or invented: Past midnight, Dessert bar, Quiet find, Crowd favorite, Small house, The classic.
- Hidden Gem section cut (fourth chance-mechanic on the page); "Hidden gems" keep-pill re-pointed to /best/cheap/ as "Best value pours".
- Static meta says 998/169 (true at ship time per Supabase); client refreshes live. REAL fix is a site_stats view + build-step stamp — next backend task.

## Decisions rejected
- Iframe embed in production (SEO/geolocation dead) — preview-only technique.
- Tastea Garden Grove drink claims (Oolong/Mung Bean) — unverified; reverted to live-verified 7 Leaves facts. City After Dark kept verbatim from live page.
- content-visibility lazy rendering — caused phantom iframe height and scroll flicker; removed.
- localStorage-forever floater dismissal — session-only now.

## Traps discovered
- Safari collapses flex belts (max-content track + mask + rotation) → cards stack. Fix: flex-wrap:nowrap + flex:0 0 auto + min-width:max-content on groups, fixed card width. Nothing in a marquee may be shrinkable.
- documentElement.scrollHeight ≠ body.scrollHeight (900px phantom) — always measure body for iframe sizing.
- file:// testing silently kills absolute /js /css paths — smoke-test over local HTTP.
- Duplicate DOM IDs from the doubled ty-float block made the first search box win and the second a dead ghost.
- Emoji icons read as clutter at scale; the sprite system (24-grid, 1.5px champagne stroke, one pink payload per icon) is the standard now.

## Next steps
1. site_stats Supabase view + build-step stamping for meta/schema/nav counts (nav rail still says 334/46 with no Ventura — pending from 07-20 too).
2. Verify the conveyor on Jay's Safari specifically (the stacking browser).
3. Consider mobile variant of the search floater (finder.css hides it under 1080px).
4. gen_site/nav_data repoint at Supabase (from 07-20 backlog).
5. Monitor omakase-default bounce; flip default if data says so.

## Stack notes (Jay's preferences)
Static HTML + vanilla JS, no build step for pages; Supabase PostgREST reads with publishable key; scoped-CSS-under-container pattern for section bundles; derived state over stored state; truth-gate on every visible fact; previews as -vN files in chat, repo stays clean; commit = saved, push = live (Vercel bobatime → bobanight.com).
