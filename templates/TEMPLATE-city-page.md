# TEMPLATE — CITY DIRECTORY  `/boba/{state}/{city}/`

> The programmatic backbone. One per city with ≥1 verified shop. Renders from a per-city export object (DATA-SCHEMA §5, list form). The model writes ONLY the answer-lede gloss and the `{{faq.a}}` editorial, both constrained to real data. Everything else is verified fields. Save as `{city}-city-vN.md`.

Placeholders: `{{x}}` = data field · `{{VERIFY: ...}}` = unverified, blocks publish · `[opinion]` = labeled editorial.

This page is a **directory**, not a ranking. It lists every verified shop in the city plainly. Ranking/opinion lives on `/best/{intent}/{city}/` and is linked from here. Keep the two jobs separate (the directory earns trust by being complete and neutral; the intent page earns clicks by being opinionated).

---

```html
<!-- H1 = primary query -->
<h1>Boba in {{place.name}}, {{place.region_label}}</h1>

<!-- META (head) -->
<title>Boba in {{place.name}} — {{shops.count}} Shops, Hours & Map ({{year}}) | Boba Night</title>
<meta name="description" content="Every boba shop in {{place.name}}: {{shops.count}} verified spots with addresses, hours, and what to order. Looking for date night, study, or open-late? Filtered picks inside. Updated {{verified_at}}.">
<link rel="canonical" href="https://www.bobanight.com/boba/{{place.state_slug}}/{{place.slug}}/">

<!-- ANSWER LEDE (40–60 words, liftable). States the count, the clusters, and 2–3 standouts by name. MODEL writes the gloss clause; counts/names are data. -->
<p class="lede">
{{place.name}} has <strong>{{shops.count}} boba shops</strong> we've verified{{#if place.clusters}}, concentrated around {{place.clusters_phrase}}{{/if}}.
Names you'll see a lot here: <strong>{{standout1.name}}</strong>, <strong>{{standout2.name}}</strong>, and <strong>{{standout3.name}}</strong>{{#if standout_gloss}} — {{standout_gloss}}{{/if}}.
Full list below with hours and addresses; for a specific vibe, jump to the filtered picks. Updated {{verified_at}}.
</p>

<!-- INTENT JUMP-OFF (internal links — only intents with ≥4 qualifying shops in this city render as links) -->
<nav class="intents" aria-label="Find boba by vibe">
  <span>Looking for something specific?</span>
  {{#each available_intents}}
    <a href="/best/{{slug}}/{{../place.slug}}/">{{label_short}}</a>
  {{/each}}
</nav>

<!-- LIST + MAP SPLIT (list-left / map-right on desktop; stacked on mobile) -->
<div class="city-layout">

  <!-- FILTER BAR (client-side; filters the list + map markers together. No data fetched — operates on rendered shops.) -->
  <div class="filters" role="group" aria-label="Filter shops">
    <button data-filter="all" aria-pressed="true">All ({{shops.count}})</button>
    {{#if any.attr_brown_sugar}}<button data-filter="brown-sugar">Brown sugar</button>{{/if}}
    {{#if any.attr_fruit_tea}}<button data-filter="fruit-tea">Fruit tea</button>{{/if}}
    {{#if any.attr_non_dairy}}<button data-filter="non-dairy">Non-dairy</button>{{/if}}
    {{#if any.attr_drive_thru}}<button data-filter="drive-thru">Drive-thru</button>{{/if}}
    {{#if any.open_now_supported}}<button data-filter="open-now">Open now</button>{{/if}}
    {{#if any.attr_food}}<button data-filter="food">Has food</button>{{/if}}
  </div>

  <!-- SHOP LIST. Each item: name → profile, neighborhood, signature, hours (today), attribute chips. Plain, complete, neutral. -->
  <ol class="shops">
  {{#each shops}}
    <li class="shop" data-attrs="{{attr_filter_tokens}}" data-lat="{{lat}}" data-lng="{{lng}}">
      <h2 class="shop-name"><a href="/boba/{{../place.state_slug}}/{{../place.slug}}/{{slug}}/">{{name}}</a>{{#if is_new}} <span class="tag-new">Recently opened</span>{{/if}}</h2>
      <p class="shop-meta">{{neighborhood}} · {{street}}{{#if price_band}} · {{price_band}}{{/if}}</p>
      {{#if signature_drinks}}<p class="shop-order"><strong>Known for:</strong> {{signature_drinks_joined}}</p>{{/if}}
      <p class="shop-hours">{{today_hours_string}}{{#if hours_verified_at}} <span class="verified">· verified {{hours_verified_at}}</span>{{/if}}</p>
      {{#if attribute_chips}}<ul class="chips">{{#each attribute_chips}}<li>{{this}}</li>{{/each}}</ul>{{/if}}
      <a class="shop-link" href="/boba/{{../place.state_slug}}/{{../place.slug}}/{{slug}}/">Hours, menu &amp; map</a>
    </li>
  {{/each}}
  </ol>

  <!-- MAP. Static-first (renders markers from the same shop coords; no blocking JS for first paint). Mirror CoverCapy find-a-dentist list/map split. -->
  <div class="map" id="city-map" data-center-lat="{{place.center_lat}}" data-center-lng="{{place.center_lng}}" aria-label="Map of boba shops in {{place.name}}"></div>

</div>

<!-- RECENTLY OPENED / CLOSED (freshness signal — pulls from openings/closures for this city) -->
{{#if recent_changes}}
<section class="changes">
  <h2>Recent changes in {{place.name}}</h2>
  {{#each recent_openings}}<p class="opened">Opened {{opened_on_or_verify}}: <a href="/boba/{{../place.state_slug}}/{{../place.slug}}/{{slug}}/">{{name}}</a> ({{neighborhood}}).</p>{{/each}}
  {{#each recent_closures}}<p class="closed">Closed {{closed_on}}: {{name}} — {{neighborhood}}.</p>{{/each}}
</section>
{{/if}}

<!-- FAQ (3–6 real city-level long-tail; MODEL writes answers from verified data only) -->
<section class="faq">
{{#each faq}}
  <h3>{{q}}</h3><p>{{a}}</p>
{{/each}}
</section>

<!-- RELATED (region hub up; neighbor cities sideways; the city's strongest intent page) -->
<nav class="related">
  Part of <a href="/area/{{place.region_slug}}/">{{place.region_label}}</a> ·
  Nearby: {{#each neighbor_cities}}<a href="/boba/{{state_slug}}/{{slug}}/">{{name}}</a>{{/each}} ·
  {{#if top_intent}}Most-asked here: <a href="/best/{{top_intent.slug}}/{{place.slug}}/">best for {{top_intent.label}}</a>{{/if}}
</nav>

<footer class="freshness">Updated {{verified_at}} · {{shops.count}} shops · We re-verify {{place.region_label}} boba every {{N}} weeks. Spot something closed or moved? <a href="/report/">Tell us.</a></footer>
```

```html
<!-- JSON-LD: ItemList (the shops) + BreadcrumbList + FAQPage -->
<!-- NOTE: full LocalBusiness/CafeOrCoffeeShop schema lives on each shop PROFILE, not here. -->
<!--       This page emits ItemList referencing the canonical profile URLs only. No aggregateRating anywhere (no first-party ratings until Phase 3). -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList",
 "name":"Boba shops in {{place.name}}, {{place.region_label}}",
 "numberOfItems":{{shops.count}},
 "itemListElement":[
   {{#each shops}}{"@type":"ListItem","position":{{position}},"url":"https://www.bobanight.com/boba/{{../place.state_slug}}/{{../place.slug}}/{{slug}}/","name":"{{name}}"}{{,}}{{/each}}
 ]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://www.bobanight.com/"},
  {"@type":"ListItem","position":2,"name":"{{place.region_label}}","item":"https://www.bobanight.com/area/{{place.region_slug}}/"},
  {"@type":"ListItem","position":3,"name":"{{place.name}}","item":"https://www.bobanight.com/boba/{{place.state_slug}}/{{place.slug}}/"}
]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {{#each faq}}{"@type":"Question","name":"{{q}}","acceptedAnswer":{"@type":"Answer","text":"{{a}}"}}{{,}}{{/each}}
]}
</script>
```

---
### Render rules (enforced at QA)
- **Directory = neutral and complete.** List every verified shop in the city. No fit scores, no "best," no ranking language on this page — that's the intent page's job. The only ordering is sensible (e.g. by cluster/neighborhood, then alpha), not editorialized.
- **Only verified shops render.** `status ∈ {open, temporarily_closed}`, lat/lng present, hours present + dated. Seed-only/unverified shops do NOT appear (they sit in the enrichment queue, not on the live page).
- Lede `standout_gloss` and every `faq.a` is `[opinion]`/editorial → must draw only on real attributes; no clichés (SITE-SPEC §5); no banned words.
- An intent renders as a jump-off link ONLY if that intent has ≥4 qualifying shops in this city (matches the thin-page rule on intent pages).
- Map and list render from the SAME shop coordinates — never a second data source that could drift.
- `today_hours_string`, `hours_verified_at` are verbatim from data. If hours unknown for a shop, it isn't publishable → it isn't on the page.
- No `aggregateRating` / star schema anywhere on this page. Third-party ratings, if shown at all, live on the profile as attributed reference text.
