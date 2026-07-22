# Session 2026-07-22 — Profile order-rail rebuild (Uber location fix, reviews, Toast)

## What changed
The sticky bottom order rail on every profile-v4 page (623 pages) was rebuilt in place
by `build/patch_order_rail.py`. It replaces ONLY the `<!-- TPL:order-rail -->` block and
appends styles to `css/profile-v4.css` — it does not regenerate whole pages, so nav counts,
neighbours, and page count are untouched (deliberately, to keep the diff small and safe).

New rail, left to right:
- Lead: shop name, Google rating, review count, full street address (zip shown only when present).
- Uber Eats — location deep-link. URL now carries `pl=<base64 JSON>` of {address, latitude, longitude}
  so Uber loads results centred on the shop. Old link was name-only, so Uber fell back to the
  account's last-used address (showed Las Vegas from the scrape session). Fixed.
- DoorDash — name search. Verified in-browser that DoorDash IGNORES lat/lng in the URL for
  logged-out users, so it lands on the visitor's saved address. No public fix; exact-store needs a
  per-store DoorDash store id (future `build/check_doordash.py`, same pattern as Toast).
- Toast — verified-only. `build/check_toast.py` queries Toast Local per shop at its coordinates and
  writes `build/toast_links.json`. The rail renders a full-colour clickable Toast button only where
  a shop is confirmed present (confidence high/review); otherwise a greyed, non-clickable placeholder.
  Until the checker is run, every shop shows the greyed state.
- Directions — Google Maps search link (unchanged behaviour).

## Decisions made
- Surgical patch over full `gen_profiles_v4.py` regen — the generator has known-stale nav counts and
  would spawn ~268 new pages; wrong tool for a sticky change.
- Toast greyed-everywhere as the ship-now default, verified Toast as a fast follow after the checker.
- Three equal-weight services (no Uber referral promo) per direction; referral idea dropped because
  Uber `/invite/` links can't deep-link to a store, so a referral would break the store landing for
  the majority of visitors who already have Uber.

## Traps discovered
- `bn-shop-data` JSON has nested arrays/objects; a lazy regex mis-parses it, so slug is taken from the
  folder name (`boba/ca/<city>/<slug>/`), which is authoritative.
- Supabase `zip` is null for many shops (e.g. Share Tea) — address must degrade gracefully to
  "street, City, CA" without a trailing zip.
- DoorDash lat/lng in URL is a no-op for logged-out users — do not trust it.

## Exact next steps
1. Run `build/check_toast.py` (~11 min) to produce `build/toast_links.json`, then re-run
   `build/patch_order_rail.py` to light up verified Toast buttons, and redeploy.
2. Write `build/check_doordash.py` to capture per-store DoorDash store ids so DoorDash lands on the
   exact store like Uber does.
3. Consider tagging the three outbound links with UTM/affiliate params for click attribution.


## ADDENDUM (same day, evening) - what actually shipped
The surgical patcher approach above was SUPERSEDED: instead of patching 623 pages in place,
the generator itself was rewritten to emit the universal chrome kit template natively
(five kit lines, zero baked chrome) with the v3 order rail built in (incl. google_place_id
in the Uber pl payload). patch_order_rail.py remains as tooling but the generator owns the
template now.

Shipped this session: Amino Avenue pilot page live on the kit template; 260 new pages for
previously page-less Supabase shops (add-only unzip -n; existing pages untouched); footer
component files committed; origin-aware nav.js + CORS for file:// previews; nav.js loads
finder-data+finder post-injection; SITE-WIDE finder.js crash fixed (unguarded #dock from the
near-me dock feature killed the nav search-pill upgrade on every non-homepage page);
build/check_nav_sync.py drift guard (homepage baked header is the ONE manual mirror).

Traps added: bridge commits leave undeletable .git lock files (mount forbids deletes) - every
Terminal git block must start with rm -f of index.lock/HEAD.lock. Reconstructed generator had
an unescaped % in the map-ring fallback branch (only fired for some densities) - fixed with %%.

Next: (1) regenerate existing 623 onto the kit (one generator run, then git add -A boba),
(2) city hub pages + ~45 root templates onto the five kit lines, (3) run check_toast.py and
regenerate to light verified Toast buttons, (4) check_doordash.py for exact-store links,
(5) extend check_nav_sync.py to drawer/bottombar blocks.
