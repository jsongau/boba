# SITE-SPEC — NITEBOBA (LOCKED)
> Architecture, URL structure, page types, design system, and voice. Lock this before building. Changing URL structure or design tokens after pages exist is expensive — decide now.

---

## 1. URL STRUCTURE (the programmatic spine)
Clean, lowercase, hyphenated, trailing slash, no query params for content.

```
/                                         Homepage
/boba/{state}/{city}/                     City directory      e.g. /boba/ca/irvine/
/boba/{state}/{city}/{shop-slug}/         Shop profile        e.g. /boba/ca/irvine/7-leaves-cafe-jeffrey/
/best/{intent}/{place}/                   Intent page (MONEY) e.g. /best/date-night/irvine/
/area/{region}/                           Region hub          e.g. /area/sgv/  /area/little-saigon/  /area/convoy-san-diego/
/near/{landmark}/                         Landmark page       e.g. /near/uc-irvine/  /near/disneyland/  /near/cal-state-fullerton/
/new/{region}/                            New-openings feed   e.g. /new/orange-county/   (the freshness engine, rendered)
/brand/{brand-slug}/                      Chain hub           e.g. /brand/sunright/  /brand/sharetea/
/guide/{slug}/                            Editorial guide     e.g. /guide/brown-sugar-vs-tiger-sugar/
```

**Slug rules.** ~~Original plan: cross-street disambiguator~~ **AS PUBLISHED (locked 11 JUL 2026): shop slug = `kebab(name)-kebab(city)`, e.g. `7-leaves-cafe-irvine`.** The site shipped with city-based slugs; published slugs are permanent, so this is now the rule. Place slug = `kebab(city)`; regions use canonical short slugs (`sgv`, not `san-gabriel-valley`). Never change a published slug — 301 if you must.

**Canonicalization.** A shop lives at exactly one canonical URL (`/boba/ca/{city}/{slug}/`). It is *referenced* from city pages, intent pages, region hubs, and landmark pages, but those references link to the canonical — never duplicate the full profile.

---

## 2. PAGE TYPES (what each one is for)
| Type | Primary query it wins | Core blocks |
|---|---|---|
| **Homepage** | brand / "niteboba" | search, map entry, top regions, new-openings strip, featured intents |
| **City directory** | "boba in {city}", "{city} boba shops" | answer lede, filterable shop list, map, intent links, FAQ |
| **Shop profile** | "{shop name} {city}", "{shop} hours/menu" | facts block, signature drinks, attributes, hours, map, nearby, FAQ |
| **Intent page** (money) | "best boba for {intent} in {place}" | answer-first ranked list (editorial, labeled), per-pick reasons, FAQ, schema |
| **Region hub** | "best boba in {region}" | region narrative, top cities, top shops, intents, new openings |
| **Landmark page** | "boba near {landmark}" | distance-sorted shops, walkability, the "after dinner / before movie" framing |
| **New-openings feed** | "new boba {region} 2026" | dated list of recent openings + "recently closed" flags (freshness signal) |
| **Brand hub** | "{chain} locations near me" | brand overview, all SoCal locations, which location is best for what |
| **Guide** | informational long-tail | editorial explainer, internal links to relevant intent/city pages |

---

## 3. THE INTENT TAXONOMY (drives /best/{intent}/{place}/)
Canonical intents (slug → label):
- `date-night` → Boba for a date night
- `first-date` → Boba for a first date (quieter than date-night)
- `study` → Study-friendly boba (wifi + seating + outlets)
- `open-late` → Boba open late / late night
- `brown-sugar` → Best brown sugar boba
- `fruit-tea` → Best fresh fruit tea
- `matcha` → Best matcha
- `non-dairy` → Non-dairy / vegan-friendly boba
- `cheap` → Best cheap boba / best value
- `group` → Boba for a group hangout
- `drive-thru` → Drive-thru boba
- `with-food` → Boba + food (popcorn chicken, Taiwanese eats)
- `aesthetic` → Aesthetic / photo-worthy boba cafes

`{place}` = any city, region, or landmark with enough qualifying shops. **Page exists only if ≥4 qualifying, verified shops** — thin pages are banned (your CoverCapy rule). This matrix is the scale engine; see SEO-GEO-STRATEGY.md for sequencing.

---

## 4. DESIGN SYSTEM (editorial, not SaaS — Capy DNA)
Same philosophy as CoverCapy: editorial spacing, large type, hairline dividers, real whitespace. **Not** gradients, glassmorphism, rounded-card soup, or beige AI templates. Boba register = warm, milky, brown-sugar, a little playful — but the *directory* reads trustworthy and grown-up, not like a bubble-tea logo.

### Tokens (proposed — adjust to taste, then LOCK)
```
--ink:        #1A1410   /* near-black brown, body text */
--brown-sugar:#3D2817   /* deep, headings / dark accents */
--syrup:      #A6713C   /* mid caramel, primary accent */
--milk:       #F4ECE0   /* milk-tea cream, page background */
--paper:      #FBF7F0   /* lightest, cards / surfaces */
--matcha:     #6F8F4E   /* secondary accent (fresh/fruit/veg cues, "open now") */
--taro:       #8E6FB0   /* sparing accent — reserve for one role (e.g. "featured") */
--line:       #E4D8C7   /* hairline dividers */
```
Reserve `--taro` for a single role the way CoverCapy reserves purple for Platinum Elite — pick one (e.g. featured/member shops) and never bleed it elsewhere.

### Type
- **Display / headings:** Fraunces (you already own this in the Capy stack — keep it for family consistency). Optical sizing on, a little soft.
- **Body / UI:** Inter Tight (matches CoverCapy) or a humanist grotesque. One body face, one display face. No third font.

### Layout rules
- Max content width ~720–760px for editorial pages; wider only for map + list split views.
- No large dark full-bleed sections (carry the CoverCapy rule — they read heavy and un-editorial). One scoped dark element max per page if needed.
- Hairline dividers over boxes. Whitespace over borders.
- Maps: list-left / map-right on desktop (mirror the CoverCapy find-a-dentist pattern you already validated).

---

## 5. BRAND VOICE
**Who's talking:** the friend who has tried every boba shop from the 626 to Convoy and has specific, confident, slightly playful opinions — and who will tell you the truth (this spot is great for a group, wrong for a first date). Knows the vocabulary (brown sugar vs. tiger sugar, cheese foam, loose-leaf vs. powder, 50% sweet, crystal boba/deerioca, fruit tea vs. milk tea). Never breathless, never marketing-brained.

**Do:** be specific and concrete; state opinions and the reason for them; use real boba vocabulary; give the order recommendation; respect the reader's time; admit when something needs verifying.

**Don't:** gush, hedge into mush, or write the same sentence about every shop.

### BANNED WORDS / PHRASES (anti-AI-slop)
Boba-blog clichés (banned — they erase specificity and signal AI slop):
`hidden gem`, `nestled`, `vibrant`, `indulge`, `a symphony of`, `burst of flavor`, `look no further`, `whether you're … or …`, `tantalize`, `oasis`, `go-to spot` (as filler), `treat yourself` (as filler), `crave-worthy`, `next-level`, `game-changer` (overused), `must-try` is allowed but only with a named drink.

Capy-family ban list (carried from CoverCapy for consistency):
`premium`, `curated`, `discover`, `transform`, `seamless`, `modern`, `innovative`, `empower`, `elevate`, `navigate`.

### Typographic house style (optional port from CoverCapy)
CoverCapy bans em/en dashes as punctuation and arrow glyphs on buttons. NiteBoba is a different brand so it's your call, but porting these keeps the "Capy" family visually consistent. **Decide and lock here:** ☐ port dash/arrow rules ☐ relax for NiteBoba.

---

## 6. WHAT SHIPS IN PHASE 1 (so the build has a finish line)
- Homepage + search + map shell
- All 5 region hubs (SGV, Little Saigon, Convoy, + 2)
- City directory pages for the ~15 highest-intent cities (SGV core + Irvine + Westminster/GG + SD Convoy)
- Shop profiles for every verified shop in those cities
- Intent pages for `date-night`, `open-late`, `brown-sugar`, `study`, `with-food` across those cities/regions where ≥4 qualifying shops exist
- New-openings feeds for OC, SGV/LA, SD
- JSON-LD on every page (see SEO-GEO-STRATEGY.md)

Phase 2 = scale the matrix to all cities + remaining intents + landmark pages. Phase 3 = Boba Passport (UGC/gamification, first-party ratings → unlocks first-party `aggregateRating` schema).
