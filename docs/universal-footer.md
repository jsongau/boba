# Universal Footer — components/footer.css + components/footer.js

The site footer is ONE component shared by every page. Edit `components/footer.js` (markup) or `components/footer.css` (styling) and every page that includes the component shows the change on its next load. Never regenerate page templates for a footer change, and never write footer markup inside a template again.

## How any template uses it

Add exactly three lines to the template. Nothing else.

In the `<head>`:

    <link rel="stylesheet" href="/components/footer.css">

Where the footer should appear, as the last element before `</body>` content ends:

    <div id="bn-footer"></div>

At the end of the body, with the page's other scripts:

    <script src="/components/footer.js" defer></script>

That is the entire contract. The script injects the full footer into the placeholder, styles come from the component stylesheet, and the shop and city counts render live from Supabase (with a per-session cache and a checked static fallback for first paint).

## Previews and off-site pages (Downloads, file://, other domains)

Preview files opened from Downloads run on `file://`, where root-relative paths cannot load. Never bake footer markup into a preview; use absolute URLs for the same two assets instead:

    <link rel="stylesheet" href="https://www.bobanight.com/components/footer.css">
    <script src="https://www.bobanight.com/components/footer.js" defer></script>

The markup lives inside footer.js so it needs no extra fetch, and the live counts query works from any origin.

## Rules for template prompts

Copy these into any prompt that builds or edits a page template:

1. Do not write, copy, or generate footer HTML. Include the three lines above and nothing more. The footer is owned by `components/footer.js`.
2. Do not restyle the footer from page CSS. No selectors targeting `.ft2` anywhere except `components/footer.css`.
3. Do not hardcode shop or city counts in the footer or near it. The component fetches live numbers.
4. If a page already has an old `<footer class="site-footer">` or any other footer, delete it and use the placeholder instead. If a page has a `<footer class="ft2">` baked in (the homepage does, for SEO), leave it: the component detects it and replaces it with the canonical version at load, so it can never drift.
5. The placeholder div must keep the id `bn-footer` exactly.

## What the footer contains (owned by the component, listed here for reference only)

Brand block with the Boba Night wordmark, positioning line, live stat row (shops · cities · checked and current), and the open-late pill. Four link columns: Tonight, Explore (all six region pages), The Menu, Community. Bottom bar with copyright and the corrections link.

## How changes propagate

- Change link, column, or wording: edit the MARKUP string in `components/footer.js`, commit, push. Every page updates on next load.
- Change styling: edit `components/footer.css`, commit, push.
- The homepage additionally keeps a baked copy of the footer markup in `index.html` for crawlers; when editing the component markup, mirror the same change in the homepage's baked copy (or ask Claude to — the build script does both). Generated pages do not need baked copies; the placeholder is enough.

## Why it is built this way

Server-side includes need a build step this static site avoids; client-side injection from one file gives the same single-source behavior with zero build. The tradeoff is that footer links on generated pages exist only after JavaScript runs — Google executes JS and follows them, but the homepage keeps a baked copy so the strongest page always has crawlable footer links in raw HTML. The counts fetch is one small query cached per session.
