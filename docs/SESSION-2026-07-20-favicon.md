# SESSION 2026-07-20 (pm) — Favicon

## What shipped
Boba Night had NO favicon (blank globe in every tab); only a theme-color (#0B0C0E) meta existed.
Built a flat vector twin of the nav logo (img/logo-nav.png: milk-tea cup, tapioca pearls, champagne
crescent moon, sparkle, flamingo ripple) on the obsidian badge. Palette pulled verbatim from
css/nav-midnight.css: obsidian #0B0C0E, pearl #F4EFE7, champagne #C5A46D, gilt #F4DDA2, neon #ff2f6d.

New root assets:
- favicon.svg          scalable mark (V1 "detailed": milk swirl, ice, 4 pearls, sparkles, glow)
- favicon.ico          multi-size 16/32/48 fallback (old Safari / Windows)
- apple-touch-icon.png  180x180, FULL-BLEED (iOS masks its own rounded corners; transparent corners render black)

Head tags added to every page:
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">

## How (source, not just output)
- Baked the block into all FOUR head-emitting generators: build/gen_site.py, gen_profiles.py,
  add_spots.py, gen_events.py (2 heads). Each insert anchor-count guarded + py_compile checked.
- New build/apply_favicon.py: idempotent stamp over git-tracked *.html (skips templates/ + build/
  partials), inserts the block after <meta charset> when rel="icon" is absent. Run: changed=973,
  skipped=0, nohead=0. RE-RUN after any gen_* regeneration (same model as apply_nav.py).

## Decision
Two variants proofed at true pixel sizes in headless Chromium (V1 detailed vs V2 bold). Jay first
picked V2, then chose V1 for the richer look (accepts slightly softer literal-16px; sharp retina+).
V2 SVG kept in Downloads if ever wanted.

## Commit
23deb9a — 981 files (973 stamped pages + 3 assets + apply_favicon.py + 4 generators). Surgical:
excluded a pre-staged docs/REPO-AND-DEPLOY.md (left for whoever staged it) and all untracked
bundle/json/_sbscaffold litter. NOT pushed from here (cloud 403 + device VM has no network).

## Traps (device bridge)
- .git/index.lock could not be unlink()'d on the mounted FS after a git status refresh. Cleared with
  python os.rename() into _to_delete/ before committing (rm/mv fail; rename works). The real commit
  finalizes via rename, so it left no lock.
- git add printed a CRLF/LF warning per file (~973 lines) and blew past the tool output cap; harmless,
  re-query staged state quietly.
- Working tree was dirty (another session's untracked work + a pre-staged doc). Staged explicitly
  (git add -u -- '*.html' + named files), never git add -A.

## Target / deploy
GitHub jsongau/niteboba (main) -> Vercel bobatime -> bobanight.com. Push from Jay's Mac Terminal:
  cd /Users/kytlegacy/Claude/Projects/NiteBoba
  git push origin main
Vercel auto-builds on push. Verify: view-source shows the 3 icon links; hard-refresh (favicons cache hard).

## Next
- BACKEND (owed, highest-leverage): enrich near-index.json with rating/open-now/price from niteboba
  for the /near-me/ map + shop modal.
- Optional: web manifest (theme_color #0B0C0E, icon-512.png already generated, maskable) -> installable PWA.
