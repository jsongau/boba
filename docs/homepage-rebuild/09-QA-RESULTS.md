# 09 — QA Results (automated, this build)

Run with Python (unicode-safe) + `node --check`. Screenshot/visual QA (doc 08) is not included: this environment has no browser-render tool, so those breakpoints must be captured separately.

## Passing
- **Copy:** 0 banned words in rendered copy; 0 in the sourced menu data.
- **Typography rule:** 0 em/en dashes used as punctuation in rendered copy.
- **Headings:** exactly one `<h1>` ("What are you craving right now?").
- **IDs:** 0 duplicate `id` attributes across the page.
- **JavaScript:** all three inline modules (directory grid, Craving Cup hero, Battle/Radar) pass `node --check`.
- **Links:** every server-rendered profile link (`/boba/ca/{city}/{shop}/`) resolves to a real page; all 20 Craving Cup chain-location links resolve.
- **Progressive enhancement:** hero + Battle render a real default with JavaScript disabled; Menu Drop Radar is fully server-rendered.
- **Data honesty:** no hours/open-now/distance/price rendered anywhere (none verified); every menu item carries a source + check date.

## Not yet tested (needs a browser)
Performance budgets (LCP/INP/CLS), keyboard traversal captured visually, reduced-motion behavior, and the 8-breakpoint screenshot review. These are owed as a separate pass with a headless browser.
