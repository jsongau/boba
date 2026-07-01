# BUILD-PLAN — THE 20 WORKSTREAMS (how to actually parallelize this)
> "20 agents" = 20 narrow workstreams, each run in its own Cowork session with MASTER.md + the relevant template + the relevant data slice injected, gated by the QA checklist. This is the realistic path. One session = one workstream = one coherent output set. Do not mix workstreams in a session — that's how you get generic output.

---

## DEPENDENCY ORDER (what blocks what)
```
FOUNDATION  ── A (data) ──┬── B (design system) ── C (templates → already drafted)
                          │
                          └── then fan out: D..S in parallel once their data slice is verified
                                            └── T (QA + ship) gates everything
```
You cannot build pages on unverified data. **Workstream A is the gate for everything content.** B and C can run in parallel with A.

---

## THE 20 WORKSTREAMS

### Foundation (run first / in parallel)
- **A1 — Full data extraction.** Re-extract every row from all SCBD tabs (incl. address-only rows) into the seed CSV. Output: complete seed.
- **A2 — Enrichment & verification.** Run the DATA-SCHEMA pipeline: geocode, GBP match, status, hours, attributes, fit scores. Output: `shops` table marked publishable. *Gate for all content workstreams.*
- **A3 — Freshness engine.** Stand up new-opening detection + closed-flagging jobs + `openings`/`closures` tables. Output: live feeds data.
- **B — Design system build.** Turn SITE-SPEC tokens into the actual CSS + base components (header, search, shop card, map split, facts table, FAQ accordion, footer). Output: component library + base stylesheet. (Reuse CoverCapy components where possible.)
- **C — Template hardening.** Take the three drafted templates → production HTML templates with JSON-LD wired to the export contract. Output: render-ready templates. *(Drafts already in /templates — this finalizes them.)*

### Content fan-out (parallel, once A2 verifies that slice)
Split by region so sessions don't collide and each holds tight, real local context:
- **D — SGV city pages** (Arcadia, Rowland Heights, San Gabriel, Monterey Park, Temple City, Pasadena)
- **E — SGV shop profiles**
- **F — OC city pages** (Irvine, Westminster, Garden Grove, Fountain Valley, Fullerton, Tustin, Costa Mesa)
- **G — OC shop profiles**
- **H — SD city pages** (San Diego Convoy/Mira Mesa clusters)
- **I — SD shop profiles**
- **J — LA + Long Beach + Cerritos/Artesia city pages + profiles**
- **K — Riverside + San Bernardino city pages + profiles** (thin seed → pair with extra new-shop research; low competition = fast wins)
- **L — Region hubs** (sgv, little-saigon, convoy, + 2)
- **M — Intent pages: date-night + first-date** across qualifying places
- **N — Intent pages: open-late** across qualifying places (highest-intent; do this one well)
- **O — Intent pages: brown-sugar + fruit-tea** (SGV authority showcase)
- **P — Intent pages: study + with-food**
- **Q — Landmark pages** (UC Irvine, Cal State Fullerton, Disneyland, UCLA/Westwood, SDSU, Cal Poly Pomona, malls)
- **R — Brand hubs** (Sunright, Sharetea, 7 Leaves, Tapioca Express, Quickly, Ten Ren's, Tiger Sugar, etc.)
- **S — Editorial guides + homepage copy + /llms.txt + verification ("how we verify") page**

### Ship gate
- **T — QA, schema validation, sitemap, internal-link audit, deploy.** Nothing publishes without passing T.

> Mapping to "20 agents": A1, A2, A3, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T = 22 buckets; collapse A1+A2 and M-into-one-session if you want exactly 20. The point is **narrow scope per session + verified data in + QA gate out.**

---

## PER-SESSION OPERATING PROCEDURE (paste into each workstream session)
1. Inject: `MASTER.md`, this `BUILD-PLAN.md` (just your workstream), the relevant `TEMPLATE-*.md`, and the verified data slice for your scope.
2. State the workstream ID and the exact files this session may write. Nothing else.
3. Build only from verified data. Unknown fact → `{{VERIFY: ...}}`. Never invent.
4. Run the QA checklist (below) on every page before marking done.
5. Output goes to versioned files (`{slug}-v1.md` → never overwrite).

---

## QA CHECKLIST (every page must pass — this is the anti-generic gate)
**Facts & honesty**
- [ ] Zero fabricated facts; every shop-specific claim traces to verified data or is marked `{{VERIFY}}`
- [ ] No third-party rating presented as first-party; any rating has attribution + date + link
- [ ] `Updated {date}` present; hours show `verified {date}`
- [ ] Editorial ranking labeled as opinion + "how we picked" method visible

**GEO/AEO structure**
- [ ] H1 = the target query
- [ ] Answer lede in first 40–60 words, liftable, names the picks
- [ ] Facts table present (raw HTML, not image)
- [ ] FAQ block present (3–6 real long-tail Qs)
- [ ] JSON-LD present and valid: `ItemList`/`CafeOrCoffeeShop`/`FAQPage` + `BreadcrumbList` as applicable
- [ ] No `aggregateRating` in schema (until Phase 3 first-party data)

**Voice & brand**
- [ ] No banned words/clichés (SITE-SPEC §5)
- [ ] Each pick has *distinct* specifics (no copy-paste sentences across shops)
- [ ] Design tokens only; no rogue colors; `--taro` reserved for its one role
- [ ] Frames as fit, not better/worse; no shop disparaged

**Plumbing**
- [ ] Canonical URL correct; links to canonical profile (no duplicate profiles)
- [ ] Internal links up (city/region) and across (intents/nearby) present
- [ ] Page exists only if ≥4 verified qualifying shops (no thin pages)
- [ ] `lastmod` in sitemap reflects real verification date

---

## SEQUENCING (fastest path to "ranks + gets cited")
1. **Week 1:** A1, A2 (SGV + Irvine slices first), B, C. Stand up homepage shell + 2 region hubs.
2. **Week 2:** D, E, F, G on the verified SGV + Irvine data. Ship `open-late` (N) and `date-night` (M) for those places — the two highest-intent money pages — as the flagship proof.
3. **Week 3:** A3 freshness engine live + `/new/` feeds; O (brown-sugar/fruit-tea) to flex SGV authority; Q landmark pages (UCI, CSUF, Disneyland).
4. **Week 4+:** scale matrix to all cities/intents; brand hubs; guides; begin Phase 3 Passport spec.

Flagship-first beats breadth-first: a handful of *excellent, verified, schema-rich* intent pages in the SGV + Irvine will start earning AI citations faster than 1,000 thin pages — and they become the quality bar every other workstream copies.
