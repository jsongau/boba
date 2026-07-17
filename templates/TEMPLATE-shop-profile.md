# TEMPLATE — SHOP PROFILE  `/boba/{state}/{city}/{shop-slug}/`

> The canonical home for one shop. This is the only place the full record lives; every other page references it. Renders from one canonical shop record (DATA-SCHEMA §2). The model writes ONLY the one-line summary and `{{faq.a}}` editorial, constrained to real attributes. Save as `{slug}-vN.md`.

Placeholders: `{{x}}` = data field · `{{VERIFY: ...}}` = unverified, blocks publish · `[opinion]` = labeled editorial.

**Honesty spine for this page:** every fact is dated and sourced. Hours and open/closed come from a primary source. Ratings (if shown at all) are third-party, attributed, dated, linked — never first-party schema, never a Boba Night star. Attributes are only shown when substantiated; unknown ⇒ omitted, never guessed.

---

```html
<!-- H1 = "{name}" (the shop is the entity) -->
<h1>{{name}}</h1>
<p class="subhead">Boba in {{neighborhood}}, {{city}}{{#if brand_id}} · part of <a href="/brand/{{brand.slug}}/">{{brand.name}}</a>{{/if}}</p>

{{#if status_temporarily_closed}}<p class="status-banner closed">Reported temporarily closed as of {{verified_at}}. We'll re-check.</p>{{/if}}

<!-- META (head) -->
<title>{{name}} — {{city}} Boba: Hours, Menu &amp; What to Order ({{year}}) | Boba Night</title>
<meta name="description" content="{{name}} in {{neighborhood}}, {{city}}: hours, address, what to order{{#if signature_drinks}} ({{signature_drinks.0}}){{/if}}, and what it's good for. Verified {{verified_at}}.">
<link rel="canonical" href="https://www.bobanight.com/boba/{{state_slug}}/{{city_slug}}/{{slug}}/">

<!-- ONE-LINE SUMMARY (liftable, ≤30 words). MODEL writes this from real attributes — the single most useful true sentence about this shop. -->
<p class="lede">[opinion] {{summary}}</p>

<!-- FACTS BLOCK (raw, scannable, extraction-friendly) -->
<dl class="facts">
  <dt>Address</dt><dd>{{street}}, {{city}}, {{state}} {{postal_code}}{{#if gbp_url}} · <a href="{{gbp_url}}" rel="nofollow">Google Maps</a>{{/if}}</dd>
  <dt>Neighborhood</dt><dd>{{neighborhood}}{{#if region_slug}} (<a href="/area/{{region_slug}}/">{{region_label}}</a>){{/if}}</dd>
  {{#if phone}}<dt>Phone</dt><dd><a href="tel:{{phone_e164}}">{{phone}}</a></dd>{{/if}}
  {{#if price_band}}<dt>Price</dt><dd>{{price_band}}</dd>{{/if}}
  {{#if website}}<dt>Website</dt><dd><a href="{{website}}" rel="nofollow">{{website_display}}</a></dd>{{/if}}
  {{#if instagram}}<dt>Instagram</dt><dd><a href="{{instagram}}" rel="nofollow">{{instagram_handle}}</a></dd>{{/if}}
  <dt>Status</dt><dd>{{status_label}} · verified {{verified_at}}</dd>
</dl>

<!-- HOURS (per-day table; powers open-late + "open now"). Verbatim from verified data. -->
<section class="hours">
  <h2>Hours</h2>
  <p class="open-now" data-hours='{{hours_json}}'><!-- client computes Open now / Closed from this; SSR fallback below --></p>
  <table>
    <tbody>
    {{#each hours.days}}
      <tr{{#if is_today}} class="today"{{/if}}><th>{{day}}</th><td>{{range_or_closed}}</td></tr>
    {{/each}}
    </tbody>
  </table>
  <p class="hours-source">Hours verified {{hours_verified_at}}{{#if gbp_url}} via <a href="{{gbp_url}}" rel="nofollow">Google</a>{{/if}}. Holiday hours may differ.</p>
</section>

<!-- WHAT TO ORDER (verified/observed signature drinks only; never invented) -->
{{#if signature_drinks}}
<section class="order">
  <h2>What to order</h2>
  <ul>{{#each signature_drinks}}<li>{{this}}</li>{{/each}}</ul>
  {{#if order_note}}<p>[opinion] {{order_note}}</p>{{/if}}   <!-- MODEL may add ONE concrete sentence tied to a real drink/attr -->
</section>
{{/if}}

<!-- GOOD TO KNOW (attribute chips — ONLY substantiated attrs render; unknown = omitted) -->
<section class="attributes">
  <h2>Good to know</h2>
  <ul class="attr-list">
    {{#if attr_seating}}<li>Seating: {{attr_seating}}</li>{{/if}}
    {{#if attr_wifi}}<li>Wifi</li>{{/if}}
    {{#if attr_outlets}}<li>Outlets</li>{{/if}}
    {{#if attr_drive_thru}}<li>Drive-thru</li>{{/if}}
    {{#if attr_food}}<li>Food (popcorn chicken / Taiwanese eats)</li>{{/if}}
    {{#if attr_loose_leaf}}<li>Brews loose-leaf tea</li>{{/if}}
    {{#if attr_brown_sugar}}<li>Notable brown sugar boba</li>{{/if}}
    {{#if attr_fruit_tea}}<li>Strong fresh fruit tea</li>{{/if}}
    {{#if attr_matcha}}<li>Matcha program</li>{{/if}}
    {{#if attr_non_dairy}}<li>Non-dairy options</li>{{/if}}
  </ul>
</section>

<!-- BEST FOR (links to the intent pages this shop QUALIFIES for — fit_* ≥ 2. Internal-link engine. Never assert a fit the rubric didn't earn.) -->
{{#if qualifying_intents}}
<section class="best-for">
  <h2>Good for</h2>
  <p>Based on our visit/verification, {{name}} fits:
  {{#each qualifying_intents}}<a href="/best/{{slug}}/{{../city_slug}}/">{{label}}</a>{{/each}}.</p>
</section>
{{/if}}

<!-- THIRD-PARTY RATINGS (REFERENCE ONLY — optional. Attributed, dated, linked. NOT schema. NOT a Boba Night score.) -->
{{#if external_ratings}}
<section class="ratings-ref">
  <h2>Ratings elsewhere</h2>
  <p>For reference (we don't compute our own rating):
  {{#each external_ratings}}{{source}} {{value}} as of {{checked_on}} (<a href="{{url}}" rel="nofollow">link</a>){{#unless @last}}; {{/unless}}{{/each}}.</p>
</section>
{{/if}}

<!-- MAP -->
<div class="map" id="shop-map" data-lat="{{lat}}" data-lng="{{lng}}" aria-label="Map showing {{name}}"></div>

<!-- NEARBY (other verified shops near this one — distance-sorted; internal links) -->
<section class="nearby">
  <h2>Other boba nearby</h2>
  <ul>{{#each nearby_shops}}<li><a href="/boba/{{state_slug}}/{{city_slug}}/{{slug}}/">{{name}}</a> · {{distance_mi}} mi · {{neighborhood}}</li>{{/each}}</ul>
</section>

<!-- FAQ (3–5 real per-shop long-tail: "does {name} have …", "is {name} open …", "what should I get at {name}". MODEL writes answers from verified data.) -->
<section class="faq">
{{#each faq}}
  <h3>{{q}}</h3><p>{{a}}</p>
{{/each}}
</section>

<nav class="related">
  More boba in <a href="/boba/{{state_slug}}/{{city_slug}}/">{{city}}</a> · <a href="/area/{{region_slug}}/">{{region_label}}</a>
</nav>

<footer class="freshness">Profile updated {{verified_at}} · hours {{hours_verified_at}}. Something wrong? <a href="/report/">Report it.</a></footer>
```

```html
<!-- JSON-LD: CafeOrCoffeeShop (LocalBusiness subtype) + BreadcrumbList + FAQPage -->
<!-- CRITICAL: NO aggregateRating / review schema. We don't own first-party ratings until Phase 3 (Boba Passport). -->
<!--           openingHoursSpecification is emitted ONLY from verified hours. -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CafeOrCoffeeShop",
 "name":"{{name}}",
 "@id":"https://www.bobanight.com/boba/{{state_slug}}/{{city_slug}}/{{slug}}/#shop",
 "url":"https://www.bobanight.com/boba/{{state_slug}}/{{city_slug}}/{{slug}}/",
 "address":{"@type":"PostalAddress","streetAddress":"{{street}}","addressLocality":"{{city}}","addressRegion":"{{state}}","postalCode":"{{postal_code}}","addressCountry":"US"},
 "geo":{"@type":"GeoCoordinates","latitude":{{lat}},"longitude":{{lng}}},
 {{#if phone}}"telephone":"{{phone_e164}}",{{/if}}
 {{#if website}}"sameAs":["{{website}}"{{#if instagram}},"{{instagram}}"{{/if}}],{{/if}}
 "servesCuisine":"Bubble Tea",
 {{#if price_band}}"priceRange":"{{price_band}}",{{/if}}
 "openingHoursSpecification":[
   {{#each hours.spec}}{"@type":"OpeningHoursSpecification","dayOfWeek":"{{day_schema}}","opens":"{{opens}}","closes":"{{closes}}"}{{,}}{{/each}}
 ]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://www.bobanight.com/"},
  {"@type":"ListItem","position":2,"name":"{{region_label}}","item":"https://www.bobanight.com/area/{{region_slug}}/"},
  {"@type":"ListItem","position":3,"name":"{{city}}","item":"https://www.bobanight.com/boba/{{state_slug}}/{{city_slug}}/"},
  {"@type":"ListItem","position":4,"name":"{{name}}","item":"https://www.bobanight.com/boba/{{state_slug}}/{{city_slug}}/{{slug}}/"}
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
- **Page exists only for verified shops.** `status ∈ {open, temporarily_closed}` + lat/lng + dated hours. A permanently-closed shop becomes an archived profile with a closure date and is removed from lists, not deleted (preserves the URL + the freshness signal).
- `summary` and every `faq.a` are `[opinion]`/editorial → real attributes only; no clichés; no banned words (SITE-SPEC §5).
- **Attributes:** render only what's substantiated. Unknown attribute ⇒ omit the `<li>`. Never output "wifi: unknown" and never guess.
- **Hours:** verbatim + dated. `openingHoursSpecification` is generated from the same verified hours object — schema and visible table can never disagree.
- **No first-party rating of any kind.** No `aggregateRating`, no stars, no Boba Night score. Third-party ratings only as attributed reference text in the optional ratings block.
- `qualifying_intents` lists an intent ONLY if `fit_{intent} ≥ 2` per the documented rubric. The profile must not claim a fit the shop didn't earn.
- All outbound links to GBP/website/IG carry `rel="nofollow"`.
