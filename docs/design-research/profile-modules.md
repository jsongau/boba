# Venue Profile Modules — Open-Now/Hours, Dark Maps, What-to-Order, Nearby Rails (Design Research)

Research for **Boba Night** (bobanight.com) — dark obsidian editorial boba directory, 334 SoCal shops.
Topic: the modules that live on an individual shop page — the **open-now/hours block**, the **dark map**,
the **what-to-order rundown**, and the **nearby/similar exploration rail**. Static multi-page vanilla-JS site;
CSS-first, transform/opacity/filter only, `prefers-reduced-motion` honored, honesty brand (no fake ratings).

Palette + house rules honored in every snippet:
`--obsidian:#0B0C0E; --pearl:#F4EFE7; --champagne:#C5A46D; --neon:#ff3f6f;`
Fraunces serif + Inter, letterspaced eyebrows, hairline borders, 2px radii, film grain,
**one glowing element per viewport max**.

The map is the single riskiest module for this brand: a default Google/Mapbox tile is a bright rectangle that
detonates the obsidian mood. Most of the "hot moves" below exist to make a map feel like it was cut from the
same obsidian as the rest of the page — and to give the shop's own pin the one neon glow the viewport is allowed.

---

## Sources studied

- **CARTO — "A new look for Positron & Dark Matter basemaps"** (carto.com/blog/positron-dark-matter-new-look) —
  the canonical editorial dark basemap. Their stated principle: "fine-tune the color system, eliminate extra
  noise, introduce detail less aggressively," and improve **figure-ground** so *your* data (the pin) pops off a
  quiet base. That figure-ground goal is exactly ours: the base recedes to near-obsidian, the shop pin glows.
- **Stamen — "Introducing Positron & Dark Matter"** (stamen.com) — origin of Dark Matter; confirms the design
  intent of a near-black base with de-emphasized roads/labels built as an *overlay-friendly* canvas.
- **Mapbox — Dark style reference + "Custom map style / Monochrome"** (docs.mapbox.com/map-styles/reference/dark,
  blog.mapbox.com) — vector re-render approach: you restyle *layers* (roads, water, labels), you don't filter an
  image. Source for the road/water/label hex palette and the "suppress POI layers" move.
- **MapAtlas — "How to Style a Custom Branded Map (Dark Mode, No Watermarks)"** (mapatlas.eu/blog) — concrete
  dark vector palette (`bg #1a1a2e`, water `#0d3b66`, major road `#3a3a5c`, minor `#2d2d4a`), brand-accent road/
  label recipe with `text-halo`, and `attributionControl:false` white-labeling. Source for label-halo legibility.
- **Leaflet dark-theme CSS trick** (dev.to/deepakdevanand, glensea.com) — the *cheapest* dark map: a single CSS
  `filter` chain on the tile pane turns any light OSM tileset dark with **zero extra JS**. Source for the filter
  stack + the `.leaflet-container{background:#000}` panning-flash fix.
- **Leaflet.TileLayer.ColorFilter** (github.com/xtk93x) + **Zverik/leaflet-grayscale** — plugin-grade filter
  arrays: `grayscale:100% + invert:100%` = instant dark; `hue:180deg + invert:100%` = dark that keeps water/road
  hue sane. Source for the two-recipe filter menu.
- **Mapbox Static Images API** (docs.mapbox.com/api/maps/static-images, mapbox.com/blog/using-static-maps) —
  render the map **server-side into a PNG/WebP** at build time: no map JS on the page, perfect obsidian match,
  privacy-clean, and progressively upgradeable to interactive on click. Source for the static-first pattern.
- **The Infatuation — venue guide/review pages** (theinfatuation.com/new-york/guides) — the food-rundown gold
  standard: a tight descriptive paragraph, condensed **uppercase category + neighborhood tags**, a **"Perfect For"**
  contextual tag row (Date Nights, Late Nights, Sitting Outside), and clear "READ THE REVIEW" action links.
  Source for the what-to-order block and the "good for" chip row.
- **W3C ARIA APG — Disclosure (Show/Hide) pattern** (w3.org/WAI/ARIA/apg/patterns/disclosure) — the correct,
  minimal accessible primitive for "today's hours → tap to see the week": `<button aria-expanded>` + `aria-controls`
  + `hidden`, Enter/Space toggle. Source for the hours accordion a11y.
- **web.dev / MDN — `<time>`, `Intl.DateTimeFormat`, `scroll-snap`** — spec backing for honest machine-readable
  hours, timezone-correct "open now" math, and the horizontal nearby rail.

---

## Hot moves

### 1. Honest "Open now" status pill computed from real hours (never a fake badge)
**Where seen:** Google/Yelp/Resy all show a live open/closed state; the discipline (below) is ours.
**Why it works:** the pill is *derived* from structured hours at render time, so it can never lie — it degrades to
"Hours unknown" when data is missing instead of guessing. Ties directly to the honesty brand. The neon is spent
**only** on the "Open" dot, and only if the map pin isn't already the viewport's one glow.
```html
<p class="status" data-hours='{"tue":[["11:00","21:30"]]}' data-tz="America/Los_Angeles">
  <span class="dot" aria-hidden="true"></span><b class="status__label">Checking…</b>
  <span class="status__sub"></span>
</p>
```
```js
function shopStatus(hours, tz){
  const now = new Date();
  const p = new Intl.DateTimeFormat('en-US',{weekday:'short',hour:'2-digit',minute:'2-digit',
    hour12:false,timeZone:tz}).formatToParts(now);
  const day = p.find(x=>x.type==='weekday').value.toLowerCase();
  const mins = +p.find(x=>x.type==='hour').value*60 + +p.find(x=>x.type==='minute').value;
  const toM = s => +s.slice(0,2)*60 + +s.slice(3);
  const spans = (hours[day]||[]);
  for (const [o,c] of spans){
    if (mins >= toM(o) && mins < toM(c)){
      const left = toM(c) - mins;
      return {open:true, sub: left<=45 ? `Closes in ${left} min` : `Open until ${c}`};
    }
  }
  const next = spans.find(([o])=>toM(o)>mins);
  return {open:false, sub: next ? `Opens ${next[0]}` : 'Closed today'};
}
```
```css
.status{display:inline-flex;gap:.5rem;align-items:baseline;font:500 .8rem/1 Inter,sans-serif}
.dot{width:7px;height:7px;border-radius:50%;background:#5b5f66;translate:0 -1px} /* default: muted */
.status.is-open .dot{background:var(--neon);box-shadow:0 0 8px 1px color-mix(in oklab,var(--neon) 70%,transparent)}
.status.is-open .status__label{color:var(--pearl)}
.status__sub{color:var(--champagne);letter-spacing:.02em}
```
**Impact:** H · **Effort:** M (one small JS fn; data already structured for schema.org anyway)

### 2. "Closes soon" is a state, not a color scream
**Where seen:** Google's amber "Closing soon · 9:30 PM"; ours stays monochrome + champagne.
**Why it works:** urgency without alarm — the honesty brand can't afford a red panic bar, so the *word* "Closes in
40 min" carries the signal and the champagne sub-text carries the eye. No extra hue enters the palette.
```css
.status.closing .status__sub{color:var(--neon);font-weight:600} /* text only, never a fill/badge */
```
Pair with move #1's `left<=45` branch. Keep it text; do **not** add a filled chip — a filled neon chip would
steal the viewport's one-glow budget from the map pin.
**Impact:** M · **Effort:** L

### 3. Hours: today expanded, the week behind an accessible disclosure
**Where seen:** Yelp/Resy show today's hours inline with a "See all hours" expander; a11y per W3C APG disclosure.
**Why it works:** 90% of visits only need *today*; the full week is one tap away and fully keyboard/SR accessible.
Uses the exact APG primitive (`aria-expanded` + `aria-controls` + `hidden`) — no library.
```html
<button class="hours__toggle" aria-expanded="false" aria-controls="wk">
  <span>Today · 11:00 AM – 9:30 PM</span><svg class="chev" aria-hidden="true">…</svg>
</button>
<table id="wk" class="hours__week" hidden>
  <tr aria-current="true"><th>Tue</th><td>11:00 AM – 9:30 PM</td></tr> …
</table>
```
```js
const t = document.querySelector('.hours__toggle');
t.addEventListener('click', ()=>{
  const open = t.getAttribute('aria-expanded')==='true';
  t.setAttribute('aria-expanded', String(!open));
  document.getElementById('wk').toggleAttribute('hidden');
});
```
```css
.hours__toggle{display:flex;justify-content:space-between;width:100%;background:none;border:0;
  border-bottom:1px solid color-mix(in oklab,var(--champagne) 30%,transparent);color:var(--pearl);
  padding:.7rem 0;font:inherit;cursor:pointer}
.chev{transition:rotate .22s cubic-bezier(.2,.7,.2,1)}
.hours__toggle[aria-expanded="true"] .chev{rotate:180deg}
.hours__week [aria-current="true"]{color:var(--pearl)} /* today; other rows dimmed */
.hours__week th,.hours__week td{color:color-mix(in oklab,var(--pearl) 62%,transparent);
  padding:.4rem 0;font:400 .85rem/1.3 Inter}
@media (prefers-reduced-motion:reduce){.chev{transition:none}}
```
**Impact:** H · **Effort:** L

### 4. Dark map, cheapest tier: CSS-filter the tile pane (zero map-vendor JS beyond Leaflet)
**Where seen:** dev.to/deepakdevanand, glensea.com, Leaflet.TileLayer.ColorFilter, Zverik/leaflet-grayscale.
**Why it works:** turns any free light OSM/raster tileset into a dark base with **one CSS rule** — no Mapbox token,
no vector style JSON, no cost. `hue-rotate(180deg)` after `invert` keeps water/greens from going radioactive.
The container `background:#000` kills the white flash while panning.
```css
.leaflet-tile-pane{
  /* two recipes — pick one: */
  filter: invert(1) hue-rotate(180deg) brightness(.92) contrast(.9);       /* keeps hues sane */
  /* filter: grayscale(1) invert(1) brightness(.85) contrast(1.05); */      /* colder / graphite */
}
.leaflet-container{background:var(--obsidian)}
.leaflet-control-attribution{filter:invert(1) hue-rotate(180deg);opacity:.5;font-size:10px}
```
Caveat: filtering re-tints *everything* including your own overlay tiles — add the shop pin as an **SVG marker
element** (not a tile) so it sits *above* the filtered pane and keeps true neon (see #7).
**Impact:** H · **Effort:** L (best cost/quality ratio for a static site)

### 5. Dark map, best tier: vector re-render (CARTO Dark Matter / Mapbox dark) with POI layers suppressed
**Where seen:** CARTO Dark Matter, Mapbox dark reference, MapAtlas branded-dark guide.
**Why it works:** a true vector dark style controls each layer, so you can push the base to near-obsidian, **delete
the noisy default POI pins** (other coffee shops, ATMs) that would compete with your one pin, and set a champagne
road/label accent. This is the figure-ground CARTO explicitly designed for: quiet base, loud data.
```js
// starting from a dark style, mute the base to match obsidian and remove POI clutter
map.on('load', () => {
  map.setPaintProperty('background','background-color','#0B0C0E');
  map.setPaintProperty('water','fill-color','#0e1620');
  map.setPaintProperty('road-primary','line-color','#2a2b2f');
  ['poi-label','poi','transit-label'].forEach(id => map.getLayer(id) && map.removeLayer(id));
});
```
Label legibility on near-black uses a **halo** (MapAtlas): `text-color:#C5A46D`, `text-halo-color:#0B0C0E`,
`text-halo-width:1`. Cost: a Mapbox/CARTO token + their JS. Reserve for the flagship shop template, not all 334.
**Impact:** H · **Effort:** M–H

### 6. Static map image at build time — no map JS at all, then hydrate on intent
**Where seen:** Mapbox Static Images API; "improve perceived performance with static" tutorial.
**Why it works:** the fastest, most privacy-clean, most obsidian-faithful option — bake the dark map to a WebP at
build with your exact style, ship it as an `<img>` (0 KB JS, no third-party runtime, no cookies), and only load
the interactive map when the user actually clicks it. Ideal for a 334-page static directory where most map views
are never touched.
```html
<button class="map-static" aria-label="Show interactive map">
  <img src="/maps/shop-142.webp" width="640" height="360" alt="Map showing shop location" loading="lazy">
  <span class="map-static__cue">Tap to explore</span>
</button>
```
```js
document.querySelector('.map-static')?.addEventListener('click', function once(){
  this.removeEventListener('click', once);
  loadLeaflet().then(()=> initMap(this));   // hydrate only on demand
});
```
**Impact:** H · **Effort:** M (needs a build step to pre-render the PNGs; huge perf win)

### 7. The pin IS the viewport's one neon glow — every other dot is muted
**Where seen:** our house rule "one glowing element per viewport max," applied to the map.
**Why it works:** on the shop page the map exists to answer "where is *this* shop." So the shop's marker gets the
single neon pulse; any nearby-shop dots render as hollow champagne rings. Because the marker is an SVG element
layered above a filtered/vector pane, it keeps true `--neon` regardless of the base treatment.
```css
.pin{width:16px;height:16px;border-radius:50%;background:var(--neon);
  box-shadow:0 0 0 4px color-mix(in oklab,var(--neon) 22%,transparent),
             0 0 14px 2px color-mix(in oklab,var(--neon) 65%,transparent)}
.pin--other{background:transparent;box-shadow:none;border:1.5px solid var(--champagne);
  width:9px;height:9px;opacity:.65}
@media (prefers-reduced-motion:no-preference){
  .pin{animation:pulse 2.6s ease-in-out infinite}
  @keyframes pulse{0%,100%{scale:1}50%{scale:1.12}} /* transform-only */
}
```
Guard: if the neon status dot (#1) is visible in the same viewport as the map, the map is almost certainly its own
viewport — but audit scroll positions so two neon sources never share a screen.
**Impact:** H · **Effort:** L

### 8. "What to order" rundown — editorial, opinionated, scannable
**Where seen:** The Infatuation review blocks (tight prose + labeled picks); adapted to boba.
**Why it works:** a directory that just lists shops is a phone book; a directory that says *"get the brown sugar
oat milk, skip the slush"* is a friend. A serif lead-in dish name + Inter descriptor, with a condensed uppercase
micro-label ("THE MOVE" / "IF IT'S HOT OUT"), reads as editorial confidence — not a menu dump. No ratings, no
stars: just a point of view.
```html
<section class="order">
  <p class="eyebrow">What to order</p>
  <ul class="order__list">
    <li>
      <span class="order__tag">The move</span>
      <h3 class="order__dish">Brown Sugar Oat Milk</h3>
      <p class="order__note">Caramelized tiger stripes, oat over dairy — the reason people queue at 10pm.</p>
    </li>
  </ul>
</section>
```
```css
.order__list{list-style:none;margin:0;padding:0;display:grid;gap:1.4rem}
.order__list li{border-left:1px solid color-mix(in oklab,var(--champagne) 40%,transparent);padding-left:1rem}
.order__tag{font:600 .66rem/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:var(--champagne)}
.order__dish{font:500 1.25rem/1.2 Fraunces,serif;color:var(--pearl);margin:.25rem 0}
.order__note{font:400 .92rem/1.5 Inter;color:color-mix(in oklab,var(--pearl) 74%,transparent);max-width:46ch}
```
**Impact:** H · **Effort:** L (design is cheap; the *content* is the work — but it's the differentiator)

### 9. "Good for" context chip row (the honest replacement for a star rating)
**Where seen:** Infatuation's "Perfect For" tags (Date Nights, Late Nights, Sitting Outside).
**Why it works:** communicates *fit* instead of a fake score — "Late-night · Study-friendly · Big group" tells a
user more than 4.3 stars and can't be gamed. On a night-boba brand, "Open past midnight" is the killer chip.
```html
<ul class="chips" aria-label="Good for">
  <li>Open past midnight</li><li>Study-friendly</li><li>Terrace seating</li>
</ul>
```
```css
.chips{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin:0;padding:0}
.chips li{font:500 .74rem/1 Inter;letter-spacing:.02em;color:color-mix(in oklab,var(--pearl) 82%,transparent);
  border:1px solid color-mix(in oklab,var(--champagne) 34%,transparent);border-radius:2px;padding:.42rem .7rem}
```
**Impact:** M · **Effort:** L

### 10. Nearby / similar rail — horizontal snap with a peek, distance chip on each card
**Where seen:** Infatuation related links; every venue page's "you might also like"; CSS snap per MDN.
**Why it works:** turns a dead-end shop page into onward exploration without a full page of cards. `scroll-snap`
with `scroll-padding` shows a **peek** of the next card so the rail reads as scrollable. Each card carries a
computed distance chip ("0.4 mi · ~8 min walk") so "nearby" is literal, not decorative.
```css
.rail{display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:1.25rem;
  overscroll-behavior-x:contain;scrollbar-width:none}
.rail::-webkit-scrollbar{display:none}
.rail > *{flex:0 0 clamp(220px,72vw,300px);scroll-snap-align:start}
.rail .dist{font:500 .72rem/1 Inter;letter-spacing:.03em;color:var(--champagne)}
@media (prefers-reduced-motion:no-preference){.rail{scroll-behavior:smooth}}
```
Pair with generated CSS `::scroll-button()` / `::scroll-marker-group` (Chrome 135+) for zero-JS arrows where
supported; the rail is fully usable without them.
**Impact:** H · **Effort:** L

### 11. Distance + walk-time chips computed client-side (haversine, no API)
**Where seen:** map apps' "0.4 mi away"; ours computed locally from lat/lng already in the dataset.
**Why it works:** no geocoding call, no key — you already store each shop's coordinates, so the rail can label
distance from the *current* shop (or the user, if they opt into geolocation). ~13 walking min/mile is a fair
constant.
```js
const R=3958.8, rad=d=>d*Math.PI/180;
function miles(a,b){const dLat=rad(b.lat-a.lat),dLng=rad(b.lng-a.lng);
  const h=Math.sin(dLat/2)**2+Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.sin(dLng/2)**2;
  return 2*R*Math.asin(Math.sqrt(h));}
const label = m => `${m.toFixed(1)} mi · ~${Math.round(m*13)} min walk`;
```
**Impact:** M · **Effort:** L

### 12. Directions/Apple-Maps handoff as text links, not embedded widgets
**Where seen:** Infatuation "Google Maps" link; Yelp's "Get Directions" deep link.
**Why it works:** you don't need a live routing widget on a static page — a plain deep-link to the user's native
maps app is faster, cookieless, and stays on-brand (no injected Google chrome). Universal geo links handle both
iOS and Android; a Google fallback covers desktop.
```html
<a class="link-out" href="https://maps.apple.com/?q=Shop+Name&ll=34.06,-118.30">Directions</a>
<!-- or the vendor-neutral geo: URI on mobile -->
<a class="link-out" href="geo:34.06,-118.30?q=Shop+Name">Open in Maps</a>
```
```css
.link-out{color:var(--pearl);border-bottom:1px solid var(--neon);padding-bottom:1px;text-decoration:none}
.link-out:hover{border-bottom-color:var(--champagne)} /* neon underline is text-scale, not a "glow" */
```
**Impact:** M · **Effort:** L

### 13. Machine-readable hours via `<time>` + schema.org (SEO + honesty in one)
**Where seen:** Google rich results for local businesses; spec via MDN `<time>` / schema `openingHours`.
**Why it works:** the same structured hours that drive the "Open now" pill (#1) also feed `LocalBusiness`
`openingHoursSpecification` JSON-LD — so the honest status on-page and the status Google shows come from **one
source of truth**. Wrap displayed times in `<time>` for parsers and assistive tech.
```html
<time datetime="11:00">11:00 AM</time>–<time datetime="21:30">9:30 PM</time>
<script type="application/ld+json">
{ "@type":"CafeOrCoffeeShop","openingHoursSpecification":[
  {"@type":"OpeningHoursSpecification","dayOfWeek":"Tuesday","opens":"11:00","closes":"21:30"} ]}
</script>
```
**Impact:** M (SEO/GEO) · **Effort:** L

### 14. No-JS + reduced-motion fallbacks baked into every module
**Where seen:** house rule; MDN `prefers-reduced-motion`.
**Why it works:** static-site resilience — the status pill, hours, and map must degrade gracefully. Render a
server-side "Today: 11–9:30" string so hours read without JS; ship the static map image (#6) as the baseline so
the map exists with zero script; kill the pin pulse under reduced-motion.
```css
@media (prefers-reduced-motion:reduce){ .pin{animation:none} .rail{scroll-behavior:auto} }
```
```html
<noscript><p class="status">Today · 11:00 AM – 9:30 PM</p></noscript>
```
**Impact:** M · **Effort:** L

---

## What now reads dated (avoid list)

- **A raw, unstyled Google Maps embed** — the bright default tile + Google's blue chrome is the single fastest way
  to shatter a dark editorial mood. If you must embed Google, it can't be styled dark on the free embed; prefer
  static image or filtered Leaflet.
- **Star ratings / "4.3 ★ (2,104)"** — off-brand (honesty: no fake ratings) *and* visually 2015. Replace with
  "Good for" context chips (#9).
- **Neon-drenched everything** — glowing pins *and* glowing status *and* glowing buttons in one view. One glow.
- **A full 7-row hours table always expanded** — noisy; collapse to today + disclosure (#3).
- **Fake urgency** ("🔥 Popular now", "12 people viewing") — banned by the brand; the honest "Closes in 40 min"
  is the only urgency allowed, and it's text.
- **Emoji pins / cartoon map markers** — reads consumer-app, not editorial. Use a single geometric SVG dot.
- **Carousels that autoplay** the nearby rail — let the user drive; snap + peek is enough affordance.
- **Heavy map-library JS loaded eagerly on all 334 pages** — ship static, hydrate on click (#6).
- **Rounded 12–16px "card" chips with drop shadows** — the house language is 2px radii + hairline borders, no
  shadows except the single pin glow.

---

## Recommended for Boba Night (the 3–5 to actually apply)

1. **Honest "Open now" pill + "Closes in N min" (moves #1, #2, #13).** The signature module for a *night* boba
   brand — "Open past midnight" is the whole pitch. One neon dot, champagne sub-text, driven by the same
   structured hours that feed schema.org. Highest brand payoff, low effort.
2. **Static dark map image, hydrate-on-click, single neon pin (moves #6, #7, #4).** Baseline is a build-time WebP
   in exact obsidian — 0 KB JS across 334 pages, privacy-clean, perfect mood match. Upgrade to filtered Leaflet
   (or vector Dark Matter for the flagship template) only when the user taps. The shop's pin is the viewport's one
   glow; nearby shops are hollow champagne rings.
3. **Hours disclosure — today inline, week on tap (move #3).** Correct W3C APG disclosure, keyboard/SR clean,
   no library. Cheap and immediately makes the page feel considered.
4. **"What to order" editorial rundown (move #8).** The real differentiator vs. every other boba list — an
   opinionated pick with a serif dish name and a condensed uppercase label. Design is trivial; the *content* is
   the moat.
5. **Nearby rail with computed distance chips (moves #10, #11).** Turns the shop page into onward exploration with
   CSS snap + peek and locally-computed "0.4 mi · ~8 min walk" — no API, no key, honest and literal.

Deferred but noted: full vector Dark Matter re-styling (#5) is the prettiest map but carries a token + runtime
cost — reserve it for a single flagship/hero template rather than the whole directory.
