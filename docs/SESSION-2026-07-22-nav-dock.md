# Session 2026-07-22 — Universal nav, geo bridge, near-me dock UX

Three rounds in one day. CHANGELOG has the one-liners; this is the context a future session needs.

## What changed and why

**Universal mega nav** (`components/nav.html` + `components/nav.js`). The header is now one component: templates include a `#bn-nav` div plus one script tag and get the full nav, styles, and behavior. `nav.js` reads its own script URL, so previews opened from Downloads load everything from bobanight.com with one absolute tag — `vercel.json` adds `Access-Control-Allow-Origin: *` on `/components/*` to allow the markup fetch. Contract docs: `docs/universal-nav.md`, `docs/universal-footer.md`. Never bake nav or footer markup into any page, including previews.

**Geo bridge.** One interceptor in `js/nav-midnight.js` wraps `getCurrentPosition`: every successful fix animates all `.bn-pin` buttons and calls `window.__bnApplyGeo` (exposed by `js/below-hero.js`, 800ms double-apply guard), which personalizes the below-hero sections. Do not wrap or stub geolocation anywhere else.

**Dock UX** (`js/finder.js` + `css/finder.css`). City lock chip in the nav bar (tap to edit, re-locks on blur); GPS resolves to the nearest SoCal city via the LOCS gazetteer (25 mi cap); city-scope toggle `[City N | Within X mi M]` defaults to the locked city; card geometry is fixed (2-line name reserve, always-rendered hours line, exactly 2 pills); "Lamp Crown" Open-now toggle and "Velvet Channel" segmented controls.

## Decisions made (and why)

- **Ratings fetch live from Supabase** (`niteboba_finder?select=s,rating,reviews`, publishable key, sessionStorage cache 1h) instead of being baked into `finder-data.js`. Anything stored twice diverges; the July 20 regen proved it by dropping the weekly-hours text and stranding every card on "Hours being verified."
- **"Today:" hours are computed client-side from the baked `per` periods**, not stored as text. `todayLine()` falls back to formatting `per` when `wt` is absent. `build/gen_finder_data.py` therefore does NOT need a `wt` field — do not add one back.
- **Scope defaults to the locked city.** The lock metaphor promises "you are browsing this city"; the toggle's counts (11 vs 36) sell the widening.

## Traps discovered

- Playwright routes match in reverse registration order — register catch-alls first, specific stubs last.
- The dock card's 12px "instability" was its own entrance animation (`reA` translateY(12px)) caught mid-flight by fast measurement; wait ~300ms before measuring.
- The `.f3-lednest` absolute nest collides with the dock head on mobile; under 640px the lamp joins the filter row (`position:static`, `margin-left:auto`).
- `.spot-dist` is absolutely positioned: anything added to it (ratings) needs matching `margin-right` clearance on `.spot-meta` and `.spot-hours`.

## Data flags

- 14 of 890 open shops have no `google_rating` in Supabase — scrape pass wanted eventually.
- Nav rail counts in `components/nav.html` are still the 334/46 era and Ventura is missing from the Shops panel: the standing site_stats + build-stamp task, now a one-file fix since the nav is componentized.

## Next steps

1. site_stats Supabase view + stamping (nav counts, meta, schema) — the standing backend task.
2. Hand `bobanight-chrome-kit.zip` to the profile-template prompt; regenerated previews must use the absolute-URL component lines.
3. iPhone verification of the pinned bottom bar (3rd fix: overflow clip scoped to #tonight/#bh) still pending.
