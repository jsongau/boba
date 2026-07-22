# Universal Mega Nav — components/nav.html + components/nav.js

The site header is ONE component shared by every page: the Boba Night wordmark, the Shops / Best for / Pick for me / Guides / Society mega panels, the City-or-ZIP search minibar with the animated location beacon, the miles meter, the sound toggle, Sign in, the mobile drawer, and the pinned mobile bottom bar (Account / Shops / Saved). Edit `components/nav.html` (markup) and every page that includes the component shows the change on its next load. Never regenerate page templates for a nav change, and never write header markup inside a template again.

## How any template uses it

Add exactly two lines to the template. Nothing else.

As the FIRST element inside `<body>`, where the header mounts:

    <div id="bn-nav"></div>

At the end of the body, with the page's other scripts:

    <script src="/components/nav.js" defer></script>

That is the entire contract. The loader injects the full header from `components/nav.html`, attaches the three stylesheets it needs (`/css/nav-midnight.css`, `/css/finder.css`, `/css/sound.css`) if the page doesn't already link them, then loads the behavior scripts in order: `/js/nav-midnight.js` (panels, drawer, pin animation, bottom bar), `/js/homepage/near-me.js` (search + location beacon behavior), `/js/sound.js` (sound toggle). The placeholder div is optional — without it the header injects at the top of `<body>` — but including it keeps mount position explicit.

## Rules for template prompts

Copy these into any prompt that builds or edits a page template:

1. Do not write, copy, or generate header or nav HTML. Include the two lines above and nothing more. The header is owned by `components/nav.html`.
2. Do not restyle the nav from page CSS. No selectors targeting `.bn-header`, `.bn-bar`, `.bn-panel`, `.bn-bottombar`, `.fuse`, `.mb-field`, or any `bn-` class anywhere except `css/nav-midnight.css`.
3. If a page already has an old baked `<header>` or nav block, delete it and use the placeholder instead. Pages with the current baked header (the homepage has one, marked `data-bn-header`) are detected by the loader, which then does nothing — so including the script line everywhere is always safe and never double-injects.
4. The placeholder div must keep the id `bn-nav` exactly.
5. Leave `padding-top` room for the fixed header per `nav-midnight.css`; do not add your own header offsets.
6. Do not stub, wrap, or re-request geolocation. The nav's location beacon and any page-level "near me" button share one interceptor in `nav-midnight.js`: every successful geolocation fix animates all `.bn-pin` buttons through idle → radar-searching → locked-found, and on pages that define `window.__bnApplyGeo` (the homepage below-hero does) the fix also personalizes those sections automatically.

## What the nav contains (owned by the component, for reference only)

Desktop: wordmark, five mega-panel triggers with region rails and featured cards, search minibar (City/ZIP input, animated pin beacon, miles meter chip, Closest/Open sorts), sound toggle, Guides, Society, Sign in. Mobile: stacked two-line wordmark, long search pill with pin beacon, hamburger drawer with the full link set, pinned bottom quick bar.

## How changes propagate

- Change a link, panel, city list, or count: edit `components/nav.html`, commit, push. Every page updates on next load.
- Change styling: edit `css/nav-midnight.css`, commit, push.
- Change behavior: edit `js/nav-midnight.js` or `js/homepage/near-me.js`, commit, push.
- The homepage keeps its baked header in `index.html` for SEO and instant paint; when editing `components/nav.html`, mirror the same change in the homepage's baked header (or ask Claude to — the build script owns both). Known drift to fix at build time: the region rail counts are baked (334/46 era) until the site_stats build-step stamping lands.

## Why it is built this way

Same reasoning as the universal footer (`docs/universal-footer.md`): client-side injection from one file gives single-source behavior with zero build step. The homepage keeps a baked, crawlable header so the strongest page never depends on JavaScript for its primary navigation; generated pages accept the small tradeoff that nav links exist only after JS runs, which Google executes. The nav is heavier than the footer (23KB of markup plus three scripts), so the loader fetches the markup once per page load and the browser caches it across pages.
