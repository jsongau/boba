# TEMPLATE — INTENT PAGE  `/best/{intent}/{place}/`
> The money page. Renders from the export contract (DATA-SCHEMA §5). The model writes ONLY the `{{why}}` and `{{faq.a}}` editorial, constrained to real attributes. Everything else is verified data. Save as `{place}-{intent}-vN.md`.

Placeholders: `{{x}}` = data field · `{{VERIFY: ...}}` = unverified, blocks publish · `[opinion]` = labeled editorial.

---

```html
<!-- H1 = exact query -->
<h1>Best Boba for {{intent.label}} in {{place.name}}</h1>

<!-- META (head) -->
<title>Best Boba for {{intent.label}} in {{place.name}} ({{year}}) | CapyBoba</title>
<meta name="description" content="Our picks for {{intent.label}} boba in {{place.name}}: {{pick1.name}}, {{pick2.name}}, {{pick3.name}}. Why each fits, what to order, current hours. Verified {{verified_at}}.">
<link rel="canonical" href="https://capyboba.com/best/{{intent.slug}}/{{place.slug}}/">

<!-- ANSWER LEDE (40–60 words, liftable, names the picks) -->
<p class="lede">
For {{intent.label}} in {{place.name}}, the strongest picks are
<strong>{{pick1.name}}</strong>, <strong>{{pick2.name}}</strong>, and
<strong>{{pick3.name}}</strong> — {{one clause naming the shared reason, e.g. "all calm enough to talk, open late, and a short walk from dinner"}}.
Here's how each fits the night, what to order, and current hours. Last verified {{verified_at}}.
</p>

<!-- HOW WE PICKED (method + honesty) -->
<p class="method">How we picked: these are our opinions, ranked on {{intent fit criteria from rubric}}. We re-verify {{place.region}} every {{N}} weeks. Hours below were checked on the dates shown. We don't take payment for placement on this list.</p>

<!-- RANKED LIST (each pick: why-it-fits 2–3 specifics, order, relevant fact, neighborhood, link) -->
<ol class="picks">
{{#each picks}}
  <li>
    <h2>{{position}}. {{name}}</h2>
    <p class="why">[opinion] {{why}}</p>           <!-- MODEL WRITES THIS. 2–3 concrete, DISTINCT specifics tied to real attrs. No clichés. -->
    <p class="order"><strong>Order:</strong> {{order}}</p>   <!-- verified/observed signature; else {{VERIFY}} -->
    <p class="fact">{{fact}} · {{neighborhood}} · hours verified {{hours_verified_at}}</p>
    <a href="/boba/ca/{{place.slug}}/{{slug}}/">Full profile, hours & map →</a>
  </li>
{{/each}}
</ol>

<!-- FACTS TABLE (raw HTML — crawler/AI extraction candy) -->
<table class="facts">
  <thead><tr><th>Shop</th><th>Neighborhood</th><th>{{intent-relevant col, e.g. "Closes"}}</th><th>Seating</th><th>Signature</th></tr></thead>
  <tbody>
  {{#each picks}}
    <tr><td>{{name}}</td><td>{{neighborhood}}</td><td>{{relevant_fact}}</td><td>{{attr_seating}}</td><td>{{signature_drinks[0]}}</td></tr>
  {{/each}}
  </tbody>
</table>

<!-- FAQ (3–6 real long-tail / voice variants; MODEL WRITES answers from verified data) -->
<section class="faq">
{{#each faq}}
  <h3>{{q}}</h3><p>{{a}}</p>
{{/each}}
</section>

<!-- RELATED (internal links: other intents this place; same intent nearby places) -->
<nav class="related">
  Also in {{place.name}}: <a href="/best/open-late/{{place.slug}}/">open late</a>, <a href="/best/study/{{place.slug}}/">study-friendly</a> ·
  {{intent.label}} nearby: <a href="/best/{{intent.slug}}/{{nearby1.slug}}/">{{nearby1.name}}</a>
</nav>

<footer class="freshness">Updated {{verified_at}} · We re-verify {{place.region}} boba every {{N}} weeks.</footer>
```

```html
<!-- JSON-LD: ItemList + FAQPage + BreadcrumbList -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList",
 "name":"Best Boba for {{intent.label}} in {{place.name}}",
 "numberOfItems":{{picks.length}},
 "itemListElement":[
   {{#each picks}}{"@type":"ListItem","position":{{position}},"name":"{{name}}","url":"https://capyboba.com/boba/ca/{{place.slug}}/{{slug}}/"}{{,}}{{/each}}
 ]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {{#each faq}}{"@type":"Question","name":"{{q}}","acceptedAnswer":{"@type":"Answer","text":"{{a}}"}}{{,}}{{/each}}
]}
</script>
<!-- + BreadcrumbList: Home > {{place.region}} > {{place.name}} > Best for {{intent.label}} -->
```

---
### Render rules (enforced at QA)
- `why` must contain ≥2 specifics drawn from real `attr_*`/hours/neighborhood; must be DISTINCT per shop (no template sentences).
- No pick with `fit_{intent} = 0`. List only ships with ≥4 qualifying shops.
- No banned words (SITE-SPEC §5). Frame as fit. No disparagement.
- Any unverifiable specific → `{{VERIFY}}`, not a guess.
