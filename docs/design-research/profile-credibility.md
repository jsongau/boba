# Venue Profile Credibility — Without Star Ratings

Research for Boba Night venue/shop profile pages. How to make a shop page *feel trustworthy and authoritative* when we deliberately publish **no fake star ratings**. Studied editorial and institutional venue pages that earn trust through **dated, attributed, specific** information rather than a 4.3★ aggregate.

Palette contract this doc assumes: obsidian `#0B0C0E`, pearl `#F4EFE7` text, champagne `#C5A46D` hairlines/eyebrows, ONE neon hot-pink `#ff3f6f` glow per viewport, Fraunces (serif display) + Inter (UI), letterspaced eyebrows, 1px hairline borders, film grain, 2px radii. CSS-first, transform/opacity only, `prefers-reduced-motion` honored.

---

## Sources studied

- **MICHELIN Guide venue page (n/naka, LA)** — guide.michelin.com. The gold standard for "credibility without user ratings." A single distinction glyph (the star) anchors prestige; everything else is institutional prose ("serenely understated," a specific dish described down to the pickled cod roe), a named chef, a facilities inventory (valet, wheelchair, sake list), and dated linked features. No user score anywhere. Authority = specificity + institutional voice.
- **The Infatuation review pages** — theinfatuation.com. Numeric editorial score on a *proprietary* 0–10 scale (9.4, 9.7…) that reads as a considered judgment, not crowd-sourced. Every entry is **bylined and dated** ("Bryan Kim, July 2, 2026"). Situation tags ("perfect for a steamy third date"), the "Food Rundown" dish-by-dish verdict, conversational first-person voice.
- **The Infatuation design system by Center** — center.design/project/infatuation. Positioned explicitly as "the trustiest recommendation platform on the internet." Trust is built through *situation-specific* guidance and consistent authorial voice, not quantitative validation. Mobile-first editorial typography.
- **Google Places / Maps place sheet** — mapsplatform.google.com. The "editorial summary" (a one-line Google-authored description), recency-sortable reviews, operational transparency: `current_opening_hours` + a **special-days** sub-field, `secondary_opening_hours` (e.g. drive-through vs dine-in), and concrete accessibility facts ("stair-free access, entrances ≥3ft wide"). Trust from *factual freshness and granularity*.
- **Resy venue profile fields** — helpdesk.resy.com. The "Need to Know" block: the operator's own short list of house facts (dress, parking, what to order) — attributed to the venue, structured as a scannable ledger.
- **Kyle Macquarrie — Styling a description list with CSS Grid** — kylemacquarrie.co.uk. The clean `dl{display:grid;grid-template-columns:auto 1fr}` pattern that makes `<dt>/<dd>` pairs the correct semantic + visual primitive for a credibility ledger.
- **MDN `<dl>` reference** — developer.mozilla.org. Confirms `<dl>` term/description grouping is the accessible, correct element for a spec sheet of venue facts (not a `<table>`, not `<ul>`).

---

## Hot moves

### 1. The credibility ledger (`<dl>` spec sheet, not a rating widget)
**Where seen:** Michelin's facts column (cuisine/price/facilities), Resy "Need to Know," Google place attributes.
**Why it works:** A dense, aligned column of *concrete facts* (neighborhood, style, what to order, cash/card, seating, hours) reads as authoritative precisely because it's specific and checkable. It replaces the dopamine of a star number with the confidence of a data sheet. Semantic `<dl>` is also the accessible primitive — screen readers announce term→value pairs.
**Snippet:**
```html
<dl class="ledger">
  <dt>Style</dt><dd>Stone-ground matcha, no powder</dd>
  <dt>Order</dt><dd>Hojicha oat latte, less ice</dd>
  <dt>Seating</dt><dd>12 stools, no reservations</dd>
  <dt>Pay</dt><dd>Card only</dd>
</dl>
```
```css
.ledger{display:grid;grid-template-columns:max-content 1fr;
  column-gap:1.5rem;row-gap:0;font:400 .95rem/1.5 Inter,sans-serif}
.ledger dt{color:#C5A46D;font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;padding:.75rem 0;align-self:baseline}
.ledger dd{margin:0;color:#F4EFE7;padding:.75rem 0;
  border-top:1px solid rgba(197,164,109,.18)} /* hairline per row */
.ledger dt{border-top:1px solid rgba(197,164,109,.18)}
```
**Impact:** H · **Effort:** Low (static markup + ~10 lines CSS).

### 2. Dateline + attribution stamp ("Verified July 2026 · by the Boba Night desk")
**Where seen:** Infatuation bylines ("Bryan Kim, July 2, 2026"), Michelin dated features, Google "hours confidence."
**Why it works:** A visible *as-of date* and a named source is the single strongest honesty signal you can ship. It tells the reader the facts were checked by someone at a point in time — the opposite of an anonymous crowd average. Pairs perfectly with our "no fake ratings" brand.
**Snippet:**
```html
<p class="stamp">
  <span class="stamp__eyebrow">Verified</span>
  <time datetime="2026-07">July 2026</time>
  <span class="stamp__sep">·</span> visited by the Boba Night desk
</p>
```
```css
.stamp{font:400 .8rem/1 Inter;color:rgba(244,239,231,.6);
  letter-spacing:.02em;display:flex;gap:.5rem;align-items:center}
.stamp__eyebrow{color:#C5A46D;text-transform:uppercase;
  letter-spacing:.16em;font-size:.68rem}
.stamp time{font-variant-numeric:tabular-nums}
```
**Impact:** H · **Effort:** Low. Drive `datetime` from the Supabase `last_verified` field.

### 3. Distinction glyphs instead of stars (one badge = one earned meaning)
**Where seen:** Michelin star / Bib Gourmand / Green Star system — each glyph is a *named distinction*, not a score.
**Why it works:** A small set of hairline-outlined badges ("Editor's Pick," "Open Late," "Own-Brewed Tea," "Cash-Free") each carry a single, honest, binary meaning. No inflation, no averaging. This is our on-brand answer to the ★ — and the ONE neon-pink glow rule means at most one badge per viewport can be the pink "hero" distinction.
**Snippet:**
```html
<span class="glyph glyph--hero">◆ Editor's Pick</span>
<span class="glyph">◇ Open past midnight</span>
```
```css
.glyph{display:inline-flex;gap:.4rem;align-items:center;
  padding:.35rem .7rem;border:1px solid rgba(197,164,109,.4);
  border-radius:2px;font:500 .72rem/1 Inter;letter-spacing:.1em;
  text-transform:uppercase;color:#F4EFE7}
.glyph--hero{border-color:#ff3f6f;color:#ff3f6f;
  box-shadow:0 0 12px rgba(255,63,111,.35)} /* the ONE glow */
```
**Impact:** H · **Effort:** Low.

### 4. Institutional first-person verdict block (the "Point of View")
**Where seen:** Michelin's inspector prose; Infatuation's "The Sitch."
**Why it works:** One short, opinionated, *specific* paragraph in a consistent house voice does what 200 anonymous reviews can't: it demonstrates that a knowledgeable human went and formed a view. Specificity ("the abalone spaghetti," "they oxidize the oolong on-site") is the proof-of-work. Set it in Fraunces to signal "this is editorial, read it."
**Snippet:**
```css
.pov{font:italic 400 1.4rem/1.5 Fraunces,serif;color:#F4EFE7;
  max-width:38ch;position:relative;padding-left:1.25rem}
.pov::before{content:"";position:absolute;left:0;top:.35em;bottom:.35em;
  width:2px;background:#C5A46D} /* champagne editorial rule */
```
**Impact:** H · **Effort:** Low (design) / Med (someone must write real copy per shop).

### 5. "What to order" as a named, attributed pick — not a menu dump
**Where seen:** Infatuation "Food Rundown," Resy "Need to Know."
**Why it works:** A single confident recommendation ("Get the: hojicha oat latte") reads as insider knowledge. Attributing it ("— our pick") keeps it honest and human. It's the highest-utility line on the whole page.
**Snippet:**
```html
<div class="pick">
  <span class="pick__eyebrow">Get the</span>
  <p class="pick__item">Hojicha oat latte, easy sweet</p>
  <span class="pick__by">— Boba Night pick</span>
</div>
```
**Impact:** H · **Effort:** Low.

### 6. Hours with a "special days" / confidence treatment
**Where seen:** Google `current_opening_hours` + special-days sub-field; hours confidence.
**Why it works:** Boba is a *night* brand — "open till 1am Fri/Sat" is a load-bearing fact. Showing today's hours with a live open/closed pill and flagging holiday exceptions signals the data is maintained, not stale. Compute "open now" client-side from a static JSON so it's honest without a backend.
**Snippet:**
```js
// hours: [{d:5,open:"11:00",close:"01:00"}...] ; handles past-midnight close
function isOpenNow(hours, now = new Date()){
  const day = now.getDay(), mins = now.getHours()*60+now.getMinutes();
  return hours.some(h=>{
    const [oh,om]=h.open.split(":").map(Number), [ch,cm]=h.close.split(":").map(Number);
    let o=oh*60+om, c=ch*60+cm; if(c<=o)c+=1440;            // crosses midnight
    const t = h.d===day ? mins : (h.d===(day+6)%7 ? mins+1440 : -1);
    return t>=o && t<c;
  });
}
```
```css
.pill--open{color:#ff3f6f}          /* reserve the glow for "open now" */
.pill--closed{color:rgba(244,239,231,.5)}
```
**Impact:** H · **Effort:** Med.

### 7. Hero = photo + name + one distinction, ratings-free
**Where seen:** Michelin/Infatuation heroes lead with the room and the name, never a big number.
**Why it works:** The eye lands on the place and its single earned distinction, not a manufactured metric. Full-bleed image, Fraunces name overlaid on a bottom gradient scrim, one glyph, the dateline. Restraint = credibility.
**Snippet:**
```css
.hero{position:relative;aspect-ratio:16/10;border-radius:2px;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;
  background:linear-gradient(0deg,#0B0C0E 4%,transparent 55%)}
.hero__name{position:absolute;left:1.25rem;bottom:1.1rem;z-index:1;
  font:600 clamp(2rem,6vw,3.4rem)/.95 Fraunces,serif;color:#F4EFE7}
```
**Impact:** H · **Effort:** Low.

### 8. Provenance line: cite where the fact came from
**Where seen:** Google editorial-summary attribution; Michelin's linked features.
**Why it works:** "Hours confirmed via the shop's Instagram, 12 Jul" or "Price checked in person" turns a claim into a sourced claim. Tiny type, champagne label. This is the receipts-showing move — it makes the *absence* of star ratings feel like rigor, not a gap.
**Snippet:**
```html
<p class="src"><span>Source</span> In person · hours via @shop IG, 12 Jul 26</p>
```
```css
.src{font-size:.72rem;color:rgba(244,239,231,.45)}
.src span{color:#C5A46D;letter-spacing:.12em;text-transform:uppercase;
  margin-right:.5rem}
```
**Impact:** M · **Effort:** Low (needs the data captured during enrichment).

### 9. Tabular-nums alignment for every number on the page
**Where seen:** Michelin/Infatuation typographic discipline; the Infatuation score treatment.
**Why it works:** Prices, distances, hours, counts that align in a monospaced-figure column look *maintained and audited*. It's a 1-line change with an outsized "this data is real" effect.
**Snippet:**
```css
.ledger dd, .stamp time, .price, .distance{font-variant-numeric:tabular-nums}
```
**Impact:** M · **Effort:** Low.

### 10. Situation tags ("perfect for") as scannable chips
**Where seen:** Infatuation's situation-based guidance ("third date," "with parents").
**Why it works:** Context beats score. "Late-night study," "first-date quiet," "grab-and-go" tells a reader if *this* place fits *their* moment — a more useful signal than 4.3★. Chips are cheap and very shareable.
**Snippet:**
```css
.tags{display:flex;flex-wrap:wrap;gap:.5rem}
.tag{padding:.3rem .65rem;border:1px solid rgba(244,239,231,.15);
  border-radius:2px;font:400 .78rem Inter;color:rgba(244,239,231,.85)}
```
**Impact:** M · **Effort:** Low.

### 11. Scroll-reveal the ledger rows (subtle, reduced-motion-safe)
**Where seen:** Center's editorial motion for Infatuation (typography/scroll reveals).
**Why it works:** Rows fading up in sequence reads as "being typeset just now" — quietly premium. Transform/opacity only; killed entirely under reduced motion.
**Snippet:**
```css
@media (prefers-reduced-motion:no-preference){
  .ledger dd, .ledger dt{opacity:0;transform:translateY(8px);
    animation:rise .5s cubic-bezier(.2,.7,.2,1) forwards}
  .ledger>*:nth-child(n){animation-delay:calc(var(--i,0)*60ms)}
}
@keyframes rise{to{opacity:1;transform:none}}
```
Use `IntersectionObserver` to add a `.in` class rather than autoplaying, so it fires on scroll-in. **Impact:** L–M · **Effort:** Med.

### 12. Film-grain + hairline frame around the whole profile card
**Where seen:** Editorial print heritage of Michelin; our own brand contract.
**Why it works:** A 1px champagne hairline frame + a low-opacity grain overlay makes the profile feel like a printed guide entry — an authority object, not a database row. Grain via a tiny tiling PNG or an SVG `feTurbulence`, `mix-blend-mode:overlay`, ~4% opacity.
**Snippet:**
```css
.profile{border:1px solid rgba(197,164,109,.25);border-radius:2px;position:relative}
.profile::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:url("/img/grain.png");opacity:.04;mix-blend-mode:overlay}
```
**Impact:** M · **Effort:** Low.

---

## What now reads dated (avoid list)

- **A big aggregate star rating / 4.7★ pill.** The whole point — and it's the tell of a scraped, ungoverned directory. We publish none.
- **Anonymous "1,204 reviews" crowd counts** and 5-bar histograms. Volume ≠ trust; it reads as Yelp-circa-2014.
- **Undated everything.** Any fact with no "as of" date now reads as stale/scraped. Dateline or it didn't happen.
- **Gold gradient "PREMIUM" / glossy badge shields** with bevels and drop shadows. Our distinction glyphs are flat, hairline, one meaning each.
- **Emoji rating rows (🧋🧋🧋🧋).** Cute, but it's a fake score in a costume. Violates the honesty brand.
- **Faux "AI summary of reviews" boxes** with a sparkle icon. Reads as 2024 filler; contradicts our attributed-human-voice positioning.
- **Auto-playing hero video / parallax on the venue photo.** Heavy, fights the editorial calm, breaks on reduced-motion.
- **Multiple glowing/neon elements.** Brand rule: one pink glow per viewport, max. Two neon badges = carnival, not obsidian editorial.
- **`<table>` for the facts sheet.** Wrong semantics and hard to make responsive; use `<dl>`.
- **Skeuomorphic "receipt" or "ticket" framing.** Overused; the hairline frame + grain does the print-authority job cleanly.

---

## Recommended for Boba Night (apply these 3–5)

1. **Credibility ledger + dateline stamp (moves 1, 2, 9).** The core swap for the star rating: a semantic `<dl>` spec sheet of concrete, tabular-aligned facts, topped by a "Verified July 2026 · Boba Night desk" stamp driven off the Supabase `last_verified` field. This alone makes profiles feel audited. Highest impact, lowest effort.
2. **Distinction glyphs as the ★ replacement (move 3).** A small fixed vocabulary of flat hairline badges — "Editor's Pick" (the single pink-glow hero), "Open Late," "Own-Brewed," "Cash-Free." Honest, non-inflatable, on-palette, and it enforces the one-glow-per-viewport rule for us.
3. **Institutional verdict + "what to order" (moves 4, 5).** One Fraunces-set, first-person, *specific* paragraph plus one attributed pick per shop. This is the human-voice authority that the whole no-fake-ratings brand rests on. Design is trivial; the real cost is writing genuine copy per venue — worth it.
4. **Night-aware hours with open-now pill (move 6).** Boba Night lives on "who's open at 11pm." Client-side open/closed computed from static JSON (handles past-midnight closes), with the open pill as an allowed pink accent. Directly serves the brand's core use case.
5. **Provenance line (move 8)** as the closer on each profile. "Source: in person · hours via @shop IG, 12 Jul." Cheap once enrichment captures it, and it reframes our missing star rating as *rigor*, not omission.

Hero restraint (move 7), situation tags (move 10), grain frame (move 12) and the reveal animation (move 11) are the supporting layer — apply once the five above are in.
