# Session — Mega nav rolled sitewide (2026-07-19 pm2)

## What & why
Put the Pearl Line finder header (mega dropdowns + City/ZIP proximity finder + Sign in) on all 440 pages.
Done as a shared, cached module rather than inlining (inlining 220KB x 440 would wreck performance).

## Module (new)
- css/finder.css  — finder controls, refined dropdowns, floater, Sign in CTA; page body/html/a globals
  stripped so it can't pollute other pages; overflow-x:clip + fit media queries so the bar never scrolls.
- js/finder.js    — engine (Haversine ranking, open-now in Pacific time) + dock + floater search;
  reads window.FINDER_DATA. Site's nav-midnight.js still drives dropdowns/drawer/overlay (no conflict).
- js/finder-data.js — window.FINDER_DATA, 322 shops trimmed to finder fields (n,c,cs,sl,p,lat,lng,st,per) + 217 locations. ~124KB, cached once across the site.
- templates/nav.html — regenerated to the Pearl Line partial (header wrapped in minimal #fuse, no flamingo
  decorations; overlay + drawer + bottombar + ty-float floater + #dock). Source of truth.

## Rollout mechanism
build/apply_finder_nav.py --apply : regex-swaps the old `<a class="bn-skip">...</nav>` block for the new
partial, injects finder.css after nav-midnight.css and the two finder scripts before </body>. Dry-run by
default. Skips build/templates/docs/etc., and /nearby/ + /account/ (own finder / no nav). 440 swapped,
7 nav-less skipped, 2 named-skipped.

## Verified
Homepage, /best/ (listing), /area/sgv/ (city) render with working header, dropdowns (via nav-midnight.js),
finder engine (322 shops), floater search; own page bodies intact; 0 JS errors; overflow-free 1080-1600.

## Traps
- The finder page (/nearby/) wraps its header in a decorative .fuse hero frame and the engine needs #fuse;
  the module uses a minimal #fuse wrapper (no smoke/palm/flamingo) so it stays clean sitewide.
- Do NOT git add -A (repo root has untracked *.bundle + card-*.png). Use git add -u + explicit new files.

## Next
- Live-verify a profile page (Leaflet map) at bobanight.com after deploy.
- Trim finder-data.js further if perf needs it; consider lazy-loading finder.js on interaction.
