# 11 - QA Results (code-level, from this build)

All checks below were run against the generated homepage and assets in this session.

## Copy and language
- Banned terms in visible copy (curated, discover, seamless, transform, innovative, elevate, empower, navigate, luxury boba, VIP, hidden gem, nestled, vibrant, indulge, burst of flavor, look no further, amazing, ultimate, unlock, level up, and the old arcade names): **0 hits.**
- "premium" in visible copy: **0** (the only occurrence in data is Chatime's real product name, which is not shown on the homepage).
- Em dashes and en dashes as punctuation in visible copy: **0** (whole file: 0). The one en-dash UI glyph replaced with U+2212.
- Old arcade names (Spin the Straw, Boba Battle, Menu Drop Radar, "What are you craving"): **absent.**

## Structure and links
- Exactly **1** `<h1>`; 12 `<h2>` section titles; heading order sound.
- Duplicate element IDs: **none.**
- Internal links: **44 checked, 0 broken.** All in-page anchors resolve to real IDs.
- Directory (321-shop grid) is on /directory/, not the homepage.

## JavaScript
- `node --check` on all 8 homepage modules: **all pass.**
- Load order (defer, order-preserving): society-data, share, black-book, concierge, house-choice, tasting-flight, evening-route, navigation.
- Modules are guarded (each checks its root exists), so a missing section cannot throw.

## JS-disabled / progressive enhancement
- Server-rendered and useful without JS: Tonight's Selection, House Edit (3), Tasting Flight fallback (3), City After Dark (3), The New Pour, three evening routes with stops, the Black Book empty state, Guides, the Directory entry, Trust. Concierge and House Choice show a graceful fallback message.
- Reveal animation is gated behind a `js` class, so no-JS shows all content.

## Accessibility
- Skip link; visible :focus-visible outline (champagne); 44px targets; aria-modal drawer with aria-expanded burger; SVG hero has role=img + descriptive aria-label; concierge exposes an aria-live region (created with the interactive UI); segmented controls use aria-pressed; native selects have labels; prefers-reduced-motion fully handled.
- Contrast reasoned per surface for WCAG AA (doc 08).

## Performance
- Two web fonts (Fraunces, Inter); one stylesheet (~25KB); eight small JS files (~52KB total incl. 21KB data); no images (CSS/SVG art); no framework; no embedded map; theme-color set. No layout-shift sources (no late-loading media).

## Not verifiable in this environment
- Live browser screenshots and a human-eye visual pass (no rendering tool here) - see doc 10.
- Real macro photography (not sourced) - see doc 09.
- Menu breadth 6 chains / 66 drinks vs the 15 / 75 target - see doc 05.
