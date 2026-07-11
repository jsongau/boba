# EXAMPLE (GOLD STANDARD) — Rowland Heights · City Directory
> `/boba/ca/rowland-heights/` rendered from the city template. Reference build for the **directory backbone**: neutral, complete, trustworthy. Opinion/ranking lives on the linked `/best/...` pages, never here.
>
> **`{{VERIFY}}` markers:** shop names + addresses are real (from the SCBD seed, ROWLAND HEIGHTS section). Hours and attributes are `{{VERIFY}}` until confirmed against a primary source. In production, a shop does **not** render on this page until it passes the enrichment + QA gate (verified status, coords, dated hours — DATA-SCHEMA §3). The markers stand in for that gate. **Do not publish with `{{VERIFY}}` left in.**

Why Rowland Heights is a flagship: it's a dense node of the 626 / SGV boba mecca — ~20 shops packed onto the Colima Rd and Fullerton Rd corridors. A complete, accurate directory of this cluster is something no realtor blog or generic AI answer has (00-ANALYSIS). Win the cluster, win the queries around it.

---

```html
<h1>Boba in Rowland Heights, San Gabriel Valley</h1>

<title>Boba in Rowland Heights — 20 Shops, Hours & Map (2026) | NiteBoba</title>
<meta name="description" content="Every boba shop in Rowland Heights: 20 verified spots on the Colima Rd and Fullerton Rd corridors with addresses and hours. Names like Half & Half, Tastea, Ten Ren's, Honeymee. Updated 2026-06-26.">
<link rel="canonical" href="https://niteboba.vercel.app/boba/ca/rowland-heights/">

<p class="lede">
Rowland Heights has <strong>20 boba shops</strong> we've verified, packed almost entirely onto the <strong>Colima Rd</strong> and <strong>Fullerton Rd</strong> corridors — one of the densest boba stretches in the 626. Names you'll see a lot here: <strong>Half &amp; Half Tea Express</strong>, <strong>Tastea</strong>, <strong>Ten Ren's Tea Time</strong>, and <strong>Honeymee</strong>. Full list below with addresses and hours; for a specific vibe, jump to the filtered picks. Updated 2026-06-26.
</p>

<nav class="intents" aria-label="Find boba by vibe">
  <span>Looking for something specific?</span>
  <a href="/best/brown-sugar/rowland-heights/">Brown sugar</a>
  <a href="/best/date-night/rowland-heights/">Date night</a>
  <a href="/best/study/rowland-heights/">Study-friendly</a>
  <a href="/best/open-late/rowland-heights/">Open late</a>
  <a href="/best/with-food/rowland-heights/">Boba + food</a>
</nav>

<div class="city-layout">

  <div class="filters" role="group" aria-label="Filter shops">
    <button data-filter="all" aria-pressed="true">All (20)</button>
    <button data-filter="brown-sugar">Brown sugar</button>
    <button data-filter="fruit-tea">Fruit tea</button>
    <button data-filter="open-now">Open now</button>
    <button data-filter="food">Has food</button>
  </div>

  <!-- Ordered by corridor (Colima Rd → Fullerton Rd → Gale Ave → Nogales St), then by address. No editorialized ordering — this is a directory. -->
  <ol class="shops">

    <!-- ——— COLIMA RD CORRIDOR ——— -->
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/half-and-half-tea-express-colima/">Half &amp; Half Tea Express</a></h2><p class="shop-meta">Colima Rd · 17575 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/zero-degrees-colima/">Zero Degrees</a></h2><p class="shop-meta">Colima Rd · 17575 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/i-heart-boba-colima/">I Heart Boba</a></h2><p class="shop-meta">Colima Rd · 17418 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/mj-cafe-teahouse-colima/">MJ Cafe &amp; Teahouse</a></h2><p class="shop-meta">Colima Rd · 17521 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/tea-bar-colima/">Tea Bar</a></h2><p class="shop-meta">Colima Rd · 18178 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/honeymee-colima/">Honeymee</a></h2><p class="shop-meta">Colima Rd · 18180 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/tea-block-colima/">Tea Block</a></h2><p class="shop-meta">Colima Rd · 18311 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/quickly-colima/">Quickly</a></h2><p class="shop-meta">Colima Rd · 18353 E Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/boba-bear-colima/">Boba Bear</a></h2><p class="shop-meta">Colima Rd · 18414 E Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/boba-gogo-colima/">Boba Gogo</a></h2><p class="shop-meta">Colima Rd · 18414 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/little-bean-colima/">Little Bean</a></h2><p class="shop-meta">Colima Rd · 18415 E Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/tea-time-express-colima/">Tea Time Express</a></h2><p class="shop-meta">Colima Rd · 19725 E Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/dragonfly-tea-bar-colima/">Dragonfly Tea Bar</a></h2><p class="shop-meta">Colima Rd · 19208 Colima Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>

    <!-- ——— FULLERTON RD CORRIDOR ——— -->
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/blackball-taiwanese-dessert-fullerton/">Blackball Taiwanese Dessert</a></h2><p class="shop-meta">Fullerton Rd · 1380 Fullerton Rd · has food {{VERIFY}}</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/lollicup-fresh-fullerton/">Lollicup Fresh</a></h2><p class="shop-meta">Fullerton Rd · 1380 S Fullerton Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/bambu-fullerton/">BAMBU</a></h2><p class="shop-meta">Fullerton Rd · 1606 Fullerton Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/tastea-fullerton/">Tastea</a></h2><p class="shop-meta">Fullerton Rd · 1737 Fullerton Rd</p><p class="shop-hours">{{VERIFY: hours}}</p></li>

    <!-- ——— GALE AVE ——— -->
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/ten-rens-tea-time-gale/">Ten Ren's Tea Time</a></h2><p class="shop-meta">Gale Ave · 18912-A E Gale Ave · loose-leaf {{VERIFY}}</p><p class="shop-hours">{{VERIFY: hours}}</p></li>
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/tea-station-gale/">Tea Station</a></h2><p class="shop-meta">Gale Ave · 18558 Gale Ave</p><p class="shop-hours">{{VERIFY: hours}}</p></li>

    <!-- ——— NOGALES ST ——— -->
    <li class="shop" data-attrs="{{VERIFY}}"><h2 class="shop-name"><a href="/boba/ca/rowland-heights/bobee-5-nogales/">Bobee 5</a></h2><p class="shop-meta">Nogales St · 1756 S Nogales St</p><p class="shop-hours">{{VERIFY: hours}}</p></li>

  </ol>

  <div class="map" id="city-map" data-center-lat="{{VERIFY: Rowland Heights centroid}}" data-center-lng="{{VERIFY}}" aria-label="Map of boba shops in Rowland Heights"></div>

</div>

<section class="changes">
  <h2>Recent changes in Rowland Heights</h2>
  <p>{{VERIFY: run new-opening + closure detection for the Colima/Fullerton corridor (DATA-SCHEMA §4) before first publish. The SCBD seed is stale; expect some of the 20 to have closed and new ones to have opened.}}</p>
</section>

<section class="faq">
  <h3>How many boba shops are in Rowland Heights?</h3>
  <p>We've listed 20 in Rowland Heights, almost all on the Colima Rd and Fullerton Rd corridors. {{VERIFY: final count after the QA gate — closed shops are removed, newly verified ones added.}}</p>

  <h3>Where's the boba in Rowland Heights?</h3>
  <p>Two strips hold most of it: Colima Rd (roughly 17400–19700) and Fullerton Rd near the 60. You can walk between several shops on each. Gale Ave and Nogales St have a few more.</p>

  <h3>Is Rowland Heights a good area for boba?</h3>
  <p>It's one of the denser pockets of the San Gabriel Valley boba scene, so you're rarely more than a block or two from a shop. The trade-off is choice paralysis — which is what the filtered picks above are for.</p>

  <h3>What boba is open late in Rowland Heights?</h3>
  <p>Several Colima Rd shops keep late hours, but they change often — see <a href="/best/open-late/rowland-heights/">open-late in Rowland Heights</a> for the current verified list. {{VERIFY: hours}}.</p>
</section>

<nav class="related">
  Part of <a href="/area/sgv/">San Gabriel Valley</a> ·
  Nearby: <a href="/boba/ca/walnut/">Walnut</a> <a href="/boba/ca/diamond-bar/">Diamond Bar</a> <a href="/boba/ca/hacienda-heights/">Hacienda Heights</a> ·
  Most-asked here: <a href="/best/brown-sugar/rowland-heights/">best brown sugar boba</a>
</nav>

<footer class="freshness">Updated 2026-06-26 · 20 shops · We re-verify San Gabriel Valley boba every 3 weeks. Spot something closed or moved? <a href="/report/">Tell us.</a></footer>
```

```html
<!-- JSON-LD: ItemList (20 shops, referencing canonical profile URLs) + BreadcrumbList + FAQPage. No aggregateRating anywhere. -->
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList",
 "name":"Boba shops in Rowland Heights, San Gabriel Valley",
 "numberOfItems":20,
 "itemListElement":[
   {"@type":"ListItem","position":1,"url":"https://niteboba.vercel.app/boba/ca/rowland-heights/half-and-half-tea-express-colima/","name":"Half & Half Tea Express"},
   {"@type":"ListItem","position":2,"url":"https://niteboba.vercel.app/boba/ca/rowland-heights/zero-degrees-colima/","name":"Zero Degrees"},
   {"@type":"ListItem","position":3,"url":"https://niteboba.vercel.app/boba/ca/rowland-heights/i-heart-boba-colima/","name":"I Heart Boba"}
   /* …positions 4–20 for the remaining shops, same shape… */
 ]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://niteboba.vercel.app/"},
  {"@type":"ListItem","position":2,"name":"San Gabriel Valley","item":"https://niteboba.vercel.app/area/sgv/"},
  {"@type":"ListItem","position":3,"name":"Rowland Heights","item":"https://niteboba.vercel.app/boba/ca/rowland-heights/"}
]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"How many boba shops are in Rowland Heights?","acceptedAnswer":{"@type":"Answer","text":"We've listed 20, almost all on the Colima Rd and Fullerton Rd corridors."}},
  {"@type":"Question","name":"Where's the boba in Rowland Heights?","acceptedAnswer":{"@type":"Answer","text":"Two strips hold most of it: Colima Rd (roughly 17400–19700) and Fullerton Rd near the 60, with a few more on Gale Ave and Nogales St."}},
  {"@type":"Question","name":"Is Rowland Heights a good area for boba?","acceptedAnswer":{"@type":"Answer","text":"It's one of the denser pockets of the San Gabriel Valley boba scene — you're rarely more than a block or two from a shop."}}
]}
</script>
```

---
### Why this is the gold standard (what to copy)
- **Directory ≠ ranking.** Not one "best" on the page; shops are ordered by corridor, not opinion. Trust comes from being complete and neutral. The opinionated work is *linked* (the `/best/...` jump-offs), keeping the two jobs cleanly separated.
- **The lede names prominent shops as a fact, not a rating** ("names you'll see a lot here"), so it stays honest while still being useful and liftable.
- **Corridor structure is the local-knowledge moat** — "Colima Rd 17400–19700, Fullerton near the 60" is exactly the specificity a generic source lacks.
- **The freshness block is built in,** because a stale seed of 20 shops in a fast-moving cluster *will* be wrong without it.

### Before this publishes (the verification checklist for THIS page)
1. Run the enrichment pipeline on all 20 seed rows: confirm open/closed status + address via Google Business Profile, drop the closed ones, capture hours + coords.
2. Run new-opening detection on the Colima/Fullerton corridor — add verified shops the 2020-era seed misses.
3. Fill `today_hours_string` + `hours_verified_at` per shop; only verified shops render.
4. Confirm ≥4 qualifying shops for each intent jump-off (date-night, brown-sugar, study, open-late, with-food) before those links go live.
5. Compute the city centroid for the map; resolve every `{{VERIFY}}`. Then the QA gate passes.
