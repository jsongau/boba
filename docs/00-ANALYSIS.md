# 00 — DIRECTORY ANALYSIS + COMPETITIVE TEARDOWN
> What the seed data actually is, where it's weak, who's ranking now, and the wedge.

---

## 1. WHAT YOU'RE STARTING WITH
The source is the **Southern California Boba Directory (SCBD)** — a hobbyist Google Sheet (@benher76 / @bobacrave), compiled "through help from Yelp and humans." Tabs: LA, LA_COUNTY, LA_COUNTY_PT2, ORANGE_COUNTY, RIVERSIDE_COUNTY, SAN_BERNARDINO_COUNTY, SAN_DIEGO.

**Extracted into `stores-seed.csv`: ~320 named shops across 45 cities and 5 counties.** (Address-only rows were dropped; full re-extraction of every row is Workstream A1.)

### What it is
A **NAP skeleton** — name + city + address, nothing else. That's the entire payload.

### What it is NOT (every one of these is a gap = an opportunity)
- ❌ No coordinates (can't power a map or "near me")
- ❌ No hours (can't answer "open late," the single highest-intent boba query)
- ❌ No phone, no website, no Google Business Profile link
- ❌ No ratings or review counts
- ❌ No signature drinks, price band, or attributes (wifi, seating, drive-thru, brown sugar, fruit tea, non-dairy)
- ❌ No "last verified" date → **unknown staleness**, and boba has brutal churn (shops open and close constantly)
- ❌ No entity resolution → chains (Quickly, Lollicup, Tapioca Express, 7 Leaves, Ten Ren's, CoCo, BAMBU, Sharetea) are scattered as loose rows

### Where the coverage is strong (and where the money is)
Three boba meccas dominate the data and dominate intent:
1. **San Gabriel Valley (the 626)** — Arcadia, Rowland Heights, San Gabriel, Monterey Park, Temple City, Pasadena. Highest concentration of *authentic, loose-leaf, brewed-to-order* shops in CA. This is the credibility center of gravity. Win here and the whole site reads as authoritative.
2. **OC / Little Saigon + Irvine** — Westminster, Garden Grove, Fountain Valley (Little Saigon density); Irvine (Diamond Jamboree, UCI student demand, date-night + study intent goldmine).
3. **San Diego — Convoy + Mira Mesa** — Clairemont Mesa Blvd / Convoy St cluster.

Riverside and San Bernardino are thin in the seed (18 and 3 rows) — real gap to fill, low competition, easy wins.

---

## 2. THE COMPETITIVE TEARDOWN (who's ranking right now)
Pulled live. The people currently winning "best boba in {region}" are **not boba companies** — they're realtors and bloggers using boba content as an SEO play. That's the tell that this niche is *winnable with depth + structure + scale.*

**What the current leaders do well** (steal this):
- Direct **FAQ-shaped Q&A** that maps to voice/AI queries: "Are there award-winning boba shops in the SGV?", "What are the best late-night boba spots?", "Where's the best brown sugar boba?"
- Visible **freshness signals**: "Updated Quarterly," "Last updated Q1 2026," "verified with current addresses and hours."
- **Trust signals**: "personally visited every shop," "no sponsorships, no free products, all drinks purchased out of pocket."
- **Specificity**: named must-try drinks + prices, exact hours, neighborhood context (e.g., the Valley Blvd 1-mile stretch with ~13 shops).

**Where they're weak** (this is your wedge):
- 🎯 **No structured data.** They're prose blogs. None are emitting `ItemList` / `LocalBusiness` / `FAQPage` schema. Easy to out-rank in AI Overviews and rich results.
- 🎯 **Single-author, narrow geography.** One person covers the SGV. Nobody is covering *every* SoCal city × every intent. That's a programmatic-scale gap only a system can fill.
- 🎯 **No interactivity.** Static lists, no map, no filters (open now, near me, brown sugar, non-dairy, late).
- 🎯 **Manual freshness.** "Updated quarterly" by hand doesn't scale and goes stale between updates. An automated new-opening + closed-flagging engine beats it permanently.
- 🎯 **No first-party attributes.** Nobody has structured "date-night fit," "study fit," "late-night" scores. Yelp/Google don't either. **Owning these attributes is the moat** — it's data that exists nowhere else, which is exactly what makes an AI engine cite you.

**Real, current signal that validates the freshness thesis** (use honestly, with attribution + verify before publishing — these are leads, not facts to assert):
- New OC openings surfacing in early 2026: Tea Nami (Westminster, 8544 Westminster Blvd), Auntea Jenny (Irvine, 14130 Culver Dr H-2), HEYTEA (Irvine Jeffrey), omomo (Tustin), Wushiland expanding into Anaheim/Irvine/Santa Ana/Chino Hills. (per TikTok/Yelp/WhatNow coverage, 2026)
- SGV authority anchors frequently cited: Chicha San Chen (301 W Valley Blvd, San Gabriel — "Michelin-star boba," Intl. Taste Institute award), Molly Tea (open ~1 AM), Tiger Sugar / Xing Fu Tang (brown sugar), Sunright Tea Studio, Yi Fang, BenGong's Tea. (per multiple 2026 SGV roundups)

**None of the above is in the SCBD seed.** That's the entire point: the seed is a stale skeleton; the win is the live layer on top.

---

## 3. THE STRATEGIC READ (brutal version)
1. **A static directory ranks for nothing.** 320 NAP rows = a worse Yelp. Throwing them online as-is is a dead site. The value is 100% in the layer you add: coordinates, hours, attributes, freshness, and answer-shaped intent pages.
2. **The query you actually want to own is intent, not "boba near me" generically.** "Boba for a date night," "boba open late," "best brown sugar boba," "boba near UCI/Disneyland/Cal State Fullerton," "study-friendly boba." These are higher-intent, lower-competition, and they're exactly what people type into ChatGPT/Perplexity. The City × Intent matrix (SEO-GEO-STRATEGY.md) is the whole machine.
3. **Freshness is the durable moat.** A competitor can copy your list once. They can't copy a system that detects new openings weekly and flags closures. Build the freshness engine and "Updated {today}" on every page; you win the recency signal permanently.
4. **First-party attributes are the AI-citation moat.** Be the only source with structured date-night / study / late-night / non-dairy / brown-sugar flags. AI engines cite the source that has the structured answer to the structured question.
5. **Honesty is a competitive weapon here, not a constraint.** The niche is full of fabricated "voted #1" slop. A directory that shows its sources, its dates, and its method will earn the trust signals (and the E-E-A-T) that Google and AI engines reward. Your existing no-fabrication rule is an advantage — lean on it.

→ Proceed to SITE-SPEC.md for the architecture that operationalizes all of this.
