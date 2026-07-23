# Front-Page Design Inspiration

Reference material for the Boba Night homepage redesign, gathered 2026-07-20 by two 20-agent runs. This folder is for ideas and decisions. It is not site code and should stay out of deploys (add `docs/design-inspiration/` to `.gitignore` if `docs/` is served).

## What is here

- `web-research-notes.md` — 20 research lanes with concrete CSS/JS techniques (the exact library or approach), how each fits Boba Night, real source links, and specific ideas to steal. Covers award-site motion, scroll-driven animation, modern CSS, interactive cards, WebGL, micro-interactions, cursor and type effects, quiet-luxury design, bento grids, boba and luxury-tea brand sites, premium beverage DTC, matcha and Japanese cafe aesthetics, discovery UX, map near-me patterns, dark palettes, page transitions, snippet sources, and gamified loops.
- `concept-gallery.md` — the 20 built homepage concepts, each with hero, signature interaction, palette, and file path.
- `concepts/` — 20 self-contained, interactive `.html` concept pages. Open any one in a browser.

## The eight techniques worth applying to any direction

These came up across the research as the highest return for a dark, editorial, mobile-first discovery site, and none of them fight the current design system:

1. Split-text headline reveal on the Fraunces H1, line by line, once on load, with slow expo easing. The single strongest "an award team made this" signal.
2. Native CSS scroll-driven reveals (`animation-timeline: view()`) for the shop cards, so mobile scroll stays at 60fps with zero library weight.
3. One easing token everywhere (`cubic-bezier(0.16,1,0.3,1)`), 400 to 900ms, so the whole page feels weighted and calm rather than snappy.
4. Horizontal scroll-snap rails for curated sets like "Open late near you", thumb-friendly on mobile, no JavaScript.
5. One-accent discipline: obsidian plus champagne gold as the only accent, with orchid held strictly for the featured slot. This is the "Done Drinks" formula and it reads premium instantly.
6. Quiet card feedback: a 4px lift and a gold underline that draws in from the left, transform and opacity only.
7. Grain and a single soft radial glow behind the hero for depth without noise.
8. Respect `prefers-reduced-motion` on all of the above.

## My picks for Boba Night

The current live site is already dark and editorial, so the goal is to sharpen and add discovery energy, not reinvent. Strongest directions for that:

- **01 Midnight Atelier** is closest to the current brand and shows how far restraint alone can carry it. Use it as the base skin.
- **12 Spotify for Boba** solves the exact problem you raised earlier, making browsing feel alive with rails and cover-style cards instead of a directory. Best source of discovery patterns.
- **05 Bento Discovery** shows how to make a content-dense homepage feel curated. Good for fitting many modules without clutter.
- **18 Neighborhood Explorer** turns the SoCal regions into the identity, which doubles as internal-linking and SEO strength.
- **11 Pick-a-Pour Deck** or **08 Bubble Physics** is the one signature hero moment that adds delight without a heavy WebGL cost.

Recommended hybrid: keep the Midnight Atelier restraint as the skin, borrow the rails and card system from Spotify for Boba, let the Neighborhood Explorer regions anchor the middle of the page, and pick one signature interaction (the deck draw or the pearl physics) for a single hero flourish. Layer in the eight techniques above.

The two directions I would not lead with: heavy WebGL (10) at directory scale, and the loudest neon (02) unless the neon stays as restrained as the built version.

## Next step

Say which direction or hybrid you want and I will fold it into the v7 below-hero build and the production splice into `index.html`.
