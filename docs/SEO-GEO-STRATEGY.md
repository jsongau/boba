# SEO + GEO STRATEGY — HOW NITEBOBA BECOMES THE SOURCE AI CITES
> This is the document that wins. Traditional SEO gets you ranked; GEO/AEO gets you *quoted* by ChatGPT, Perplexity, Google AI Overviews, and Gemini. Build every page to be liftable.

---

## 0. THE ONE IDEA
When someone asks an AI "where should we get boba for a date night in Irvine?", the AI scans sources for **a structured, sourced, fresh answer to that exact question** and reproduces/cites the best one. NiteBoba wins by being the page that:
1. **Answers in the first 40–60 words**, declaratively, in a liftable shape.
2. **Backs it with structured data** the crawler can parse (`ItemList`, `LocalBusiness`, `FAQPage`).
3. **Is demonstrably fresh** (dated, recently verified).
4. **Has attributes that exist nowhere else** (date-night fit, study fit, late-night, non-dairy) — so we're the *only* place with the structured answer.

Everything below operationalizes those four.

---

## 1. ANSWER-FIRST PAGE STRUCTURE (every intent + city page)
Order is non-negotiable:

1. **H1** = the exact query. `Best Boba for a Date Night in Irvine`
2. **Answer lede (40–60 words, liftable).** Lead with the answer, name the top picks, promise the reasoning. This is the block AI engines extract verbatim. Example shape:
   > For a date night in Irvine, the strongest picks are **{A}**, **{B}**, and **{C}** — chosen for calm seating, later hours, and walkability to dinner. Below is how each one fits the night, what to order, and current hours. Last verified {date}.
3. **"How we picked" note** (1–2 sentences, the method + honesty signal).
4. **The ranked list** — editorial, labeled as opinion, each pick with: why-it-fits (2–3 specifics), signature order, the relevant fact (hours/seating/walkability), distance/neighborhood, link to canonical profile.
5. **A scannable facts table** (shop · neighborhood · open late? · seating · signature) — crawler candy; AI engines love tables for extraction.
6. **FAQ block** (3–6 Q&As targeting the real long-tail/voice variants).
7. **Related** internal links (other intents for this city; same intent nearby cities).
8. **Updated {date} + review cadence** footer.

**Liftability test:** can a stranger copy your answer lede + table and have a correct, complete answer with zero other context? If not, rewrite.

---

## 2. STRUCTURED DATA (JSON-LD) — the parse layer
Emit JSON-LD on every page. Three workhorses:

### 2a. Intent / city ranked list → `ItemList`
```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"ItemList",
  "name":"Best Boba for a Date Night in Irvine",
  "itemListOrder":"https://schema.org/ItemListOrderAscending",
  "numberOfItems":5,
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"{Shop A}",
     "url":"https://niteboba.vercel.app/boba/ca/irvine/{slug-a}/"},
    {"@type":"ListItem","position":2,"name":"{Shop B}",
     "url":"https://niteboba.vercel.app/boba/ca/irvine/{slug-b}/"}
  ]
}
</script>
```

### 2b. Shop profile → `CafeOrCoffeeShop` (a `LocalBusiness` subtype)
Only fields you have VERIFIED. Omit anything unverified — never pad schema with guesses.
```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"CafeOrCoffeeShop",
  "name":"{Verified Name}",
  "address":{"@type":"PostalAddress","streetAddress":"{...}","addressLocality":"Irvine","addressRegion":"CA","postalCode":"{...}","addressCountry":"US"},
  "geo":{"@type":"GeoCoordinates","latitude":{lat},"longitude":{lng}},
  "telephone":"{verified}",
  "url":"{official site}",
  "sameAs":["{Google Business Profile URL}","{Instagram}"],
  "openingHoursSpecification":[
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Friday","Saturday"],"opens":"11:00","closes":"23:00"}
  ],
  "servesCuisine":["Bubble Tea","Taiwanese"],
  "priceRange":"$$"
}
</script>
```
> ⚠️ Do NOT add `aggregateRating` here until NiteBoba has its own first-party review/check-in data (Phase 3). Putting third-party ratings in your schema as if they're yours is both a trust violation (your Locked Rule #2) and a schema-spam risk.

### 2c. FAQ block → `FAQPage`
```html
<script type="application/ld+json">
{
  "@context":"https://schema.org","@type":"FAQPage",
  "mainEntity":[
    {"@type":"Question","name":"Which boba shops in Irvine are open late?",
     "acceptedAnswer":{"@type":"Answer","text":"{Verified, dated answer naming shops + closing times.}"}},
    {"@type":"Question","name":"Where can I get brown sugar boba near UCI?",
     "acceptedAnswer":{"@type":"Answer","text":"{...}"}}
  ]
}
</script>
```
Also add `BreadcrumbList` on every nested page. Region/landmark pages can use `ItemList` of cities/shops.

---

## 3. THE INTENT × PLACE MATRIX (the scale engine)
This is the programmatic SEO machine. Pages = (places with enough shops) × (intents that apply).

- **Places (Phase 1 core):** SGV cities (Arcadia, Rowland Heights, San Gabriel, Monterey Park, Temple City, Pasadena), Irvine, Westminster, Garden Grove, Fountain Valley, San Diego (Convoy/Mira Mesa), + region hubs (sgv, little-saigon, convoy). ~15–18 places.
- **Intents (Phase 1):** date-night, open-late, brown-sugar, study, with-food. 5 intents.
- **Gate:** page ships only if ≥4 verified qualifying shops. No thin pages.

Phase 1 ≈ 15 places × 5 intents (minus thin combos) ≈ **60–70 money pages** + ~15 city pages + ~150 shop profiles + 3 new-openings feeds. Phase 2 scales to all 45 cities × all 13 intents × landmark pages = **thousands**. That's the CoverCapy county-page playbook applied to boba.

**Generation = data + template, never freehand.** Pages are rendered from `stores-seed.csv` (enriched) through the templates. The model's job per page is the *editorial layer* (why-it-fits reasoning, FAQ answers) on top of verified facts — not inventing facts. This is what keeps 1,000 pages from reading generic: the facts are real and local, and the editorial is constrained to real attributes.

---

## 4. THE FRESHNESS ENGINE (the durable moat)
Competitors update by hand "quarterly." Beat them permanently:

- **New-opening detection** → `/new/{region}/` feeds. Weekly pass: search per region for newly opened shops (Google "new boba {city}", Yelp "Hot & New," Instagram/TikTok geotags), queue to verification, publish dated entries. Each opening also spawns/updates the relevant city + intent pages.
- **Closed-flagging.** Quarterly (min) re-check of each shop's Google Business Profile status. Mark `status: closed`, suppress from lists, keep a redirected/archived profile noting closure date (so you never send anyone to a dead shop — the fastest way to lose local-SEO trust).
- **Visible recency.** Every page: `Updated {date}` + "we re-verify {region} every {N} weeks." Shop profiles: `Hours verified {date}`.
- **Why it's a moat:** a competitor can scrape your list once. They cannot replicate a system that knows what opened last week and what closed last month. Recency is a ranking signal *and* the thing humans actually need from a boba directory.

---

## 5. ENTITY + AUTHORITY (E-E-A-T for a directory)
- **NAP consistency** across every reference (Locked Rule #6). Entity authority compounds.
- **Author/credibility.** A visible "how NiteBoba verifies" page + per-page verification dates = the "experience" and "trustworthiness" signals Google rewards. The honesty rule is doing double duty as an SEO asset.
- **Source attribution.** When surfacing a third-party rating, attribute + date + link. This is honest AND it builds the outbound-citation graph that AI engines trust.
- **Internal linking.** Dense, intentional: city ↔ its intents ↔ its shops ↔ region hub ↔ nearby cities ↔ relevant guides. Every shop profile links up to its city and across to the intents it qualifies for.

---

## 6. CRAWLABILITY + AI ACCESS
- **Static, fast pages** (your Vercel static stack is ideal — pre-rendered HTML, no JS-gated content; AI crawlers and Google parse raw HTML, so the answer + tables + JSON-LD must be in the HTML, not hydrated client-side).
- **`/sitemap.xml`** auto-generated, segmented (cities, shops, intents, regions), with `lastmod` reflecting real verification dates.
- **`/llms.txt`** at root: a plain-text map of the site's high-value answer pages for LLM crawlers (emerging convention; cheap to add, signals "here's the good structured stuff").
- **`robots.txt`** allowing the major AI crawlers (GPTBot, PerplexityBot, Google-Extended, etc.) — you *want* to be ingested and cited.
- **Tables + lists in raw HTML** (not images) so extraction works.

---

## 7. CONVERSION + ENGAGEMENT (so authority compounds into a business)
The UX-conversion layer (the "conversion analyst" job):
- **Above the fold on every page = the answer + a map pin/CTA.** Don't make them scroll to get value; AI-referred and search-referred users bounce fast if the answer isn't instant.
- **One primary action per page**, matched to intent: date-night page → "see it on the map / get directions"; shop profile → "directions + hours + order"; new-openings → "follow {region} for new spots."
- **Filters that match intents** (open now, near me, brown sugar, non-dairy, late) — turning a reader into a returning tool-user is the retention flywheel.
- **Boba Passport (Phase 3):** check-ins, streaks, "shops you've tried," nominate-a-shop. This is the UGC loop that (a) generates first-party ratings → unlocks first-party `aggregateRating` schema, (b) creates the engagement moat, (c) mirrors CoverCapy's gamification thesis.
- **Revenue (win-win framing, Locked Rule #9):** featured/member shop placements (clearly labeled), affiliate links to ordering platforms, sponsored "new opening" spotlights — never framed as ad-free/commission-free. Featured shops get the reserved `--taro` treatment, exactly one badge, like CoverCapy tiering.

---

## 8. MEASUREMENT
- GA4 (reuse the Capy GA4 property or a new one — decide in BUILD-PLAN).
- Track: AI-referral traffic (referrers: chatgpt.com, perplexity.ai, gemini, etc. — watch these grow as GEO lands), intent-page → directions-click rate, filter usage, new-openings follow rate.
- The north-star early metric is **"are we getting cited / referred by AI engines"** — monitor AI referrers and run periodic manual checks ("ask ChatGPT/Perplexity 'best boba date night Irvine' and see if NiteBoba appears").
