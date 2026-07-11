# NITEBOBA — MASTER BUILD INDEX
> The single source of truth for the NiteBoba directory build. Memory lives in these docs, not in chat. Read this file first, every session. Nothing gets built that contradicts the LOCKED RULES below.

Last updated: 2026-06-26 · Owner: Jay · Stack target: vanilla static HTML/CSS/JS on Vercel + Supabase (mirror the CoverCapy stack)

---

## WHAT THIS IS
NiteBoba is a SoCal boba directory engineered to be **the source AI answer engines cite** when someone asks "best boba near me," "boba for a date night in Irvine," "boba open late in the 626," etc. The win condition is not traffic-for-traffic's-sake; it's **answer-engine authority + freshness no competitor can match.**

The boba equivalent of CoverCapy's moats:
| CoverCapy moat | NiteBoba moat |
|---|---|
| Verified insurance eligibility | **Verified, fresh shop data** (open/closed status, real hours, new-opening detection) |
| First-dentist-after-purchase moment | **The "where should we get boba" decision moment** (date night / study / late night) |
| Gamification (Crowns/Diamonds) | **Boba Passport** (check-ins, streaks, shop nominations) — Phase 3 |
| Programmatic SEO at scale | **City × Intent page matrix** (thousands of answer-shaped pages) |
| Honest data (no fabrication) | **Same rule, hard-locked** (see below) |

---

## FILE MAP (build/read order)
1. **MASTER.md** ← you are here. Index + locked rules + how to parallelize.
2. **00-ANALYSIS.md** — what the seed data actually is, gaps, and the competitive teardown (who's ranking now and how we beat them).
3. **SITE-SPEC.md** — information architecture, URL structure, page types, design system, brand voice, banned words.
4. **SEO-GEO-STRATEGY.md** — the AEO/GEO playbook: answer-first structure, schema, the intent matrix, the freshness engine. This is the document that wins the AI-citation game.
5. **DATA-SCHEMA.md** — the canonical data model + the enrichment/verification pipeline + the honesty/provenance rules.
6. **BUILD-PLAN.md** — the 20-workstream parallelization plan (how to actually run this across many Cowork sessions), sequencing, dependencies, and QA gates.
7. **templates/TEMPLATE-city-page.md** — programmatic city directory page.
8. **templates/TEMPLATE-shop-profile.md** — individual shop profile page.
9. **templates/TEMPLATE-intent-page.md** — "best boba for {intent} in {place}" page (the money pages).
10. **examples/example-irvine-boba-date-night.md** — flagship intent page, built on real Irvine data. Use as the gold-standard reference for voice + structure + schema.
11. **examples/example-rowland-heights-best-boba.md** — flagship region page (SGV). Second gold-standard reference.
12. **data/stores-seed.csv** — ~320 shops (45 cities, 5 counties) transcribed from the SCBD source. LEAD LIST ONLY — must be verified before publish.

---

## LOCKED RULES (violate none of these — they carry from the Capy house style)
1. **NO FABRICATION, EVER.** No invented ratings, reviews, hours, star counts, "voted #1," testimonials, or shop-specific descriptors. This is the #1 rule. When you don't have a verified fact, write `{{VERIFY: what's needed}}` and leave it for the pipeline. A wrong "open until 1 AM" that sends someone to a closed shop kills trust and kills the GEO play — Google demotes sites that get caught wrong on local facts.
2. **Ratings are sourced or they don't exist.** Third-party ratings (Google/Yelp) may be surfaced ONLY with explicit attribution + a fetch date + a link, and NEVER placed in first-party schema as if they were ours. First-party `aggregateRating` schema is used only once NiteBoba has its own verified review/check-in data (Phase 3).
3. **Editorial rankings are labeled opinions with a stated method.** Every "best X" list shows its criteria and a "how we rank" note. We rank on *fit* (date-night fit, study fit, late-night fit), not on a fake quality score. Never claim a shop is objectively "the best" without the methodology visible.
4. **Frame as fit, not better/worse.** Like CoverCapy: different shops fit different moments. A loud popcorn-chicken spot is great for a group and wrong for a first date; say that, don't trash it.
5. **Every page carries an "Updated {date}" stamp and a real review cadence.** Freshness is the moat; show it. (Competitors are literally beating generic content on "Updated Q1 2026" alone — see 00-ANALYSIS.)
6. **NAP consistency is sacred.** One canonical Name / Address / Phone per location, matching its Google Business Profile, identical across every page it appears on. Entity authority depends on this.
7. **Banned words / anti-cliché list** (see SITE-SPEC for the full list). The boba-blog clichés — "hidden gem," "nestled," "vibrant," "indulge," "burst of flavor," "look no further," "whether you're…or…" — are banned because they signal AI slop and erase specificity. Also carry the CoverCapy ban list (premium, curated, discover, transform, seamless, modern, innovative, empower, elevate, navigate) for Capy-family consistency.
8. **Save new versions, never overwrite.** `irvine-date-night-v3.md`, etc. Same discipline as CoverCapy.
9. **Revenue framing is win-win, never "free."** NiteBoba will earn from shop memberships / featured placement / affiliate ordering links — never frame as ad-free or commission-free. Frame: shop fees fund the directory that sends them customers.

---

## HOW TO USE THIS PACKAGE IN A BUILD SESSION
- Paste this MASTER.md + the relevant template + the relevant data slice into the session. Do not rely on the model "remembering" the rules — re-inject them.
- Tell the session exactly which Workstream (see BUILD-PLAN.md) it owns and which files it may write. One session = one workstream = one coherent output set. This is how you avoid the generic-output problem from mixed-context multi-file builds.
- Every generated page must pass the QA checklist in BUILD-PLAN.md before it's considered done.

---

## THE 20-"AGENT" REALITY CHECK
You can't literally spawn 20 autonomous agents that scrape, verify, and build a site end-to-end unattended today — anything claiming that is theater, and it's exactly how you get 20 piles of generic output. What works: **20 narrow, well-scoped workstreams**, each run in its own Cowork session with this package injected, with a human (you) at the QA gate. BUILD-PLAN.md defines those 20 workstreams, their dependencies, and the order to fire them. That's the realistic path to "NiteBoba reigns supreme."
