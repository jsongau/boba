# NiteBoba

The Southern California boba directory. Real hours, honest rankings, new openings tracked — no fabricated stats, no fabricated reviews, no first-party star rating until Boba Passport (Phase 3).

## Status

This is a design/build preview, not a launched site. Two pages are real static HTML you can open directly or serve with any static host:

- `index.html` — homepage, with the full mega nav (by area, by vibe, near a landmark, new openings, guides)
- `boba/ca/irvine/7-leaves-cafe-jeffrey/index.html` — a shop profile (v3: map moved into the main column as its own "Find it" section, right rail kept lean for facts)

On the profile page, the shop **name and street address are real** (from the seed data). Every other field — hours, drinks, attributes, ratings — is marked **Sample** and is placeholder only, shown to demonstrate layout. Nothing on a `Sample`-tagged field should be read as fact about the actual shop. Real values are filled in by the verification pipeline (see `docs/DATA-SCHEMA.md`) before any profile goes live.

`archive/` holds earlier profile iterations (v1: original layout with map in the right rail; v2: added the hero band, live open-now status, claimed badge, and attribute tooltips) kept for reference, not part of the live URL tree.

## Repo structure

```
index.html                                   → homepage
boba/{state}/{city}/{shop-slug}/index.html    → shop profile pages
docs/                                         → the locked build package (spec, SEO/GEO strategy,
                                                 data schema, analysis, 20-workstream build plan)
templates/                                    → page templates (city directory, intent page, shop profile)
examples/                                     → gold-standard worked examples on real seed data
data/stores-seed.csv                          → 321 shops, 45 cities, 5 counties, hand-transcribed
                                                 lead list (verify_needed = yes on every row)
archive/                                      → earlier profile page iterations, for reference
```

`docs/MASTER.md` is the index — start there for the full picture, the locked rules, and how the pieces fit together.

## The rules (see `docs/SITE-SPEC.md` for the full list)

No fabricated stats, reviews, or testimonials, ever. Ratings shown are third-party, attributed, dated, and linked — never a NiteBoba score. Editorial "best for" picks are labeled opinions with a stated method. Every page ships with an `Updated {date}` stamp. File versions are additive (`-v2`, `-v3`, ...), never overwritten.

## Design tokens

Fraunces (display) + Inter Tight (body). `--ink #1A1410` `--brown-sugar #3D2817` `--syrup #A6713C` `--milk #F4ECE0` `--paper #FBF7F0` `--matcha #6F8F4E` `--taro #8E6FB0` (reserved for one role: featured/member placement) `--line #E4D8C7`.
