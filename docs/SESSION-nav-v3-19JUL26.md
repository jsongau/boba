# Session — Nav V3 "Neon Cup" sitewide (2026-07-19 pm3)

## What changed
Six nav requests in one pass, shipped as variant V3 of three A/B candidates (V1 Pearl Rise,
V2 Steam Dial, V3 Neon Cup — all built by parallel agents on an identical verified base):
1. Mega dropdowns open centered under their own trigger, viewport-clamped (was: pinned left).
2. Chevron caret removed; hover = champagne underline drawing from center, neon + glow while open.
3. "New" tab removed; "New openings" added to the Shops rail (nav budget: route, don't orphan).
4. "Ratings & meetups" -> "Society"; City/ZIP field widened (230px, 270px focused).
5. Mobile <=920px: pill search field in the bar next to the brand, not in the hamburger.
6. "5 mi" chip -> floating "Set your range" popover: boba-cup SVG gauge that fills with the
   radius (drag / wheel / -/+), replacing the old navbar-expanding meter.

## How it shipped
- css/finder.css + js/finder.js: appended NAV V3 base + skin blocks (shared, cached, all pages).
- build/update_nav_v3.py: idempotent markup pass (remove New, rename Society, wrap #meterChip in
  .rad-anchor + #radPop shell). Applied to 443 pages + templates/nav.html + build/nav-finder-partial.html.
- The cup gauge itself is injected at runtime by finder.js into #radPop (no per-page markup).

## Traps
- Container mount served STALE file content for staged repo files (old bytes at old size even after
  re-stage). Diagnose on-device with git show HEAD:file + grep; rebuild local test fixtures from the
  known partial instead of trusting a stale snapshot.
- .finder-inline .meter{width:0} collapses the meter anywhere inside .finder-inline — the popover
  needed an !important override (V3 hides that meter anyway; V1 needed it).
- html{overflow-x:clip} clips bottom-fixed bars in Safari (Night Guide bar) — never reintroduce.

## Next steps
- Push (commands provided), hard-refresh, verify cup popover on a profile page over the map.
- Live-test /account/ email code (still unverified).
- /bulk/ hub for the catering card; "Save this spot" button wiring favorites into boba_favorites.
