# Homepage — Scroll Narrative & Pacing (Design Research)

Research for **Boba Night** (bobanight.com) — dark obsidian editorial boba directory, 334 SoCal shops.
Topic: tasteful scroll-driven reveals, section rhythm, horizontal snap rails with peek, sticky chapter
cues, and View Transitions on a **static multi-page vanilla-JS** site. Goal is award-tier pacing that
stays honest and calm — no fake urgency, no motion carnival.

Palette + house rules honored in every snippet below:
`--obsidian:#0B0C0E; --pearl:#F4EFE7; --champagne:#C5A46D; --neon:#ff3f6f;`
CSS-first, **transform/opacity/filter only**, `prefers-reduced-motion` gated, hairline borders, 2px radii,
film grain, Fraunces + Inter, letterspaced eyebrows, **one glowing element per viewport max**.

Everything here is CSS-native scroll-driven animation (`animation-timeline`) — **no GSAP, no Locomotive,
no ScrollTrigger, no IntersectionObserver JS**. That's the whole point: award-tier pacing at ~0 KB of JS.

---

## Sources studied

- **web.dev / Josh W. Comeau — "Scroll-Driven Animations"** (joshwcomeau.com/animation/scroll-driven-animations)
  — the clearest field guide to `animation-timeline: view()`, `animation-range: entry/cover/exit`, the
  `backwards` fill-mode gotcha, and `scroll()` for page progress bars. Source for the reveal + range snippets.
- **Smashing Magazine — "An Introduction to CSS Scroll-Driven Animations"** (Bramus, Dec 2024) — named
  `view-timeline` + `timeline-scope` recipe that lets a *distant* element (a sticky chapter cue, a progress
  bar) be driven by a section it doesn't contain. This is the key to sticky chapter cues without JS.
- **Chrome for Developers — "Carousels with CSS"** (Adam Argyle) — the 2025+ pure-CSS carousel spec:
  `scroll-marker-group`, `::scroll-marker` + `:target-current`, and generated `::scroll-button(left/right)`.
  Real `<button>`s the browser creates for you, keyboard-navigable, zero JS. Chrome/Edge 135+ only today.
- **Chrome for Developers — "Scroll-Triggered Animations"** — the *next* layer: `timeline-trigger` /
  `animation-trigger` (Chrome 145) that fires an animation once on entry and plays it on its own clock
  (replaces IntersectionObserver for "play once when it appears"). Bleeding-edge; noted as a future move.
- **Chrome for Developers + CSS-Tricks — Cross-Document View Transitions** — `@view-transition { navigation: auto }`
  turns same-origin MPA navigations into shared-element morphs. Exactly our situation (1,000+ static pages):
  directory card → shop profile can share a `view-transition-name` and morph across the page load.
- **Ryan Mulligan — "Scrolling Rails and Button Controls"** (ryanmulligan.dev/blog/scrolly-rail) — the
  robust flex + `scroll-snap-type: x mandatory` + `overscroll-behavior-x: contain` rail skeleton, plus the
  `scroll-behavior: smooth` gating. Source for the horizontal rail base.
- **MDN — Scroll Snap, `::scroll-marker-group`, View Transition API** — spec backing for snap alignment,
  `scroll-padding` peek math, and `prefers-reduced-motion` kill-switches.
- **Awwwards — Scrolling / Storytelling / Horizontal-scroll collections** (mid-2026 SOTD: *Units*, *NRG*,
  *Ten Years Away*, *Dragonfly Redux* by Studio Freight) — surveyed the current *vocabulary*: one idea per
  panel, generous vertical rest, sticky media with scrolling captions, horizontal chapters inside a vertical
  page. Confirms the taste direction; the CSS below is authored to hit that look without their JS stacks.

---

## Hot moves

### 1. Reveal-on-enter (the everywhere move) with `view()` + `backwards`
**Where seen:** every SOTD editorial site (Units, Ten Years Away); documented by Comeau/Smashing.
**Why it works:** content rises + fades as it crosses into view, driven by *scroll position* not a timer, so it
tracks the user's pace exactly and can't fire early/late. `backwards` fill applies the start frame *before* the
range so nothing flashes un-styled at the top of a section.
```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      animation: rise-in both;
      animation-timeline: view();
      animation-range: entry 5% cover 22%;   /* finish while comfortably on-screen */
      animation-timing-function: cubic-bezier(.22,.61,.36,1); /* soft ease-out */
    }
  }
}
@keyframes rise-in {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
```
Set a sensible non-animated default (`.reveal{opacity:1}`) so no-JS / unsupported browsers just show content.
**Impact:** H · **Effort:** Low.

### 2. Staggered list cascade (cards deal in like a hand)
**Where seen:** editorial card grids on Awwwards scrolling collection.
**Why it works:** giving each card its *own* view timeline means the stagger is spatial, not a fixed 60ms JS
delay — a card 3 rows down animates only when *it* arrives. Feels physical, never front-loads a janky burst.
```css
.grid > * {
  animation: rise-in both;
  animation-timeline: view();          /* each element tracks itself */
  animation-range: entry 0% entry 60%;
}
/* subtle per-column lag using range offset, still one keyframe set */
.grid > *:nth-child(3n+2){ animation-range: entry 8% entry 66%; }
.grid > *:nth-child(3n)  { animation-range: entry 14% entry 72%; }
```
**Impact:** H · **Effort:** Low.

### 3. Sticky chapter cue driven by a distant section (`timeline-scope`)
**Where seen:** scrollytelling long-reads (Smashing named-timeline demo); the "II / III / IV" chapter marks on
editorial narratives.
**Why it works:** a small fixed eyebrow ("II — Open Late") can be *animated by* a section it doesn't wrap,
because `timeline-scope` hoists the named timeline to a shared ancestor. Pure CSS section-progress, no observer.
```css
main { timeline-scope: --ch-latenight; }         /* hoist the name */
#latenight { view-timeline: --ch-latenight block; }
.chapter-cue {                                    /* fixed/sticky eyebrow elsewhere in DOM */
  position: sticky; top: 1.2rem;
  animation: cue-on both;
  animation-timeline: --ch-latenight;
  animation-range: entry 0% exit 100%;            /* visible only while section is in play */
}
@keyframes cue-on { 0%,100%{opacity:0} 12%,88%{opacity:1} }
```
**Impact:** M · **Effort:** Medium.

### 4. Scroll progress hairline (champagne thread that fills as you read)
**Where seen:** long-form reading indicators everywhere; `scroll()` timeline in the Chrome/Comeau docs.
**Why it works:** one fixed 1px champagne line under the header that scaleX-fills with document progress. Cheap,
GPU-only, and reinforces the "editorial long-read" feel. Does **not** count as the neon glow — keep it champagne.
```css
.read-progress{
  position: fixed; inset: 0 0 auto 0; height: 1px;
  background: var(--champagne); transform-origin: left; transform: scaleX(0);
  animation: fill linear both; animation-timeline: scroll(root);
}
@keyframes fill { to { transform: scaleX(1); } }
```
**Impact:** M · **Effort:** Low.

### 5. Horizontal snap rail *with peek* inside the vertical page
**Where seen:** Awwwards horizontal-scroll chapters; Ryan Mulligan's scrolly-rail.
**Why it works:** a "Featured tonight" or "By region" strip that scrolls sideways breaks the vertical rhythm for
one beat and signals *there's more here*. The **peek** — showing a sliver of the next card — is the whole trick;
a flush edge looks finished, a peek invites the drag. `scroll-padding-inline` + a card width < 100% does it.
```css
.rail{
  display:flex; gap:1rem; overflow-x:auto;
  scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain;
  scroll-padding-inline: 1.25rem;                 /* rest position + peek gutter */
  scrollbar-width:none;                           /* hide bar; keep keyboard/drag */
}
.rail > *{
  flex: 0 0 clamp(15rem, 78%, 22rem);             /* <100% ⇒ next card peeks in */
  scroll-snap-align: start;
}
@media (prefers-reduced-motion:no-preference){ .rail{ scroll-behavior:smooth; } }
```
**Impact:** H · **Effort:** Low.

### 6. Native scroll-markers + scroll-buttons on that rail (0-JS controls)
**Where seen:** Chrome "Carousels with CSS" (Argyle).
**Why it works:** the browser generates real, focusable `<button>`s and dot markers for a `overflow` rail — no
JS, full keyboard support, `:target-current` styles the active dot. Progressive enhancement: unsupported
browsers just get the draggable rail from move 5.
```css
.rail{ scroll-marker-group: after; }
.rail::scroll-button(left){  content: "‹" / "Previous"; }
.rail::scroll-button(right){ content: "›" / "Next"; }
.rail::scroll-button(*){ /* hairline pill, pearl on obsidian */
  border:1px solid color-mix(in srgb, var(--champagne) 40%, transparent);
  color:var(--pearl); background:transparent; border-radius:2px;
}
.rail::scroll-button(*):focus-visible{ outline:2px solid var(--neon); outline-offset:3px; }
.rail > *::scroll-marker{ content:""; width:6px; height:6px; border-radius:50%;
  border:1px solid var(--champagne); }
.rail > *::scroll-marker:target-current{ background:var(--champagne); } /* filled = current */
```
**Impact:** M · **Effort:** Low (Chrome/Edge 135+; graceful fallback elsewhere).

### 7. Cross-document View Transitions: directory card → shop profile morph
**Where seen:** Chrome/CSS-Tricks cross-document VT guides; SPA-feel MPA sites.
**Why it works:** we have 1,000+ *static* pages. Opting in makes same-origin navigations cross-fade, and any two
elements sharing a `view-transition-name` **morph** across the load — a shop card can expand into the profile
hero. Turns a hard page reload into a considered cut. One at-rule + matching names, zero routing JS.
```css
@view-transition { navigation: auto; }            /* both pages must ship this */
/* give the SAME name to the card on the list and the hero on the profile */
.shop-card[data-slug="taro-yuan"] .thumb,
.shop-hero.taro-yuan img { view-transition-name: shop-taro-yuan; }
/* default is a cross-fade; customize the root fade timing */
::view-transition-group(root){ animation-duration:.35s; }
@media (prefers-reduced-motion: reduce){
  ::view-transition-old(*), ::view-transition-new(*){ animation:none !important; }
}
```
Note: names must be **unique per page** — generate `view-transition-name: shop-<slug>` per card in the build,
and only assign it to the *clicked* card (via `:target`/JS on click) if many cards share the viewport.
**Impact:** H · **Effort:** Medium (build-time name plumbing across two page templates).

### 8. Sticky media, scrolling caption (the "pinned still, moving story" beat)
**Where seen:** Ten Years Away, Dragonfly Redux, most hospitality SOTD.
**Why it works:** one tall section where an image/panel stays `position: sticky` while 2–3 short captions scroll
past it. It's the single most "premium editorial" pacing device and needs no timeline at all — just sticky +
tall spacers. Use once on the homepage as the emotional center (e.g. "What a boba night looks like").
```css
.pin-scene{ display:grid; grid-template-columns: 1fr 1fr; gap: clamp(2rem,6vw,6rem); }
.pin-scene__media{ position: sticky; top: 12vh; height: 76vh; }
.pin-scene__steps > *{ min-height: 80vh; display:flex; align-items:center; } /* each caption owns a screen */
```
Layer move 1's reveal on each caption for the fade-in. **Impact:** H · **Effort:** Medium.

### 9. Scroll-linked hero settle (type + grain ease as you leave the fold)
**Where seen:** editorial heroes on Awwwards scrolling collection.
**Why it works:** instead of parallax (dated, jittery), let the hero *settle* — headline drifts up a touch and
the film-grain/vignette deepens as the first screen exits, handing off to the content. `exit` range, tiny
transform, opacity only. Restrained; reads as focus, not motion.
```css
.hero__title{
  animation: settle both; animation-timeline: view(); animation-range: exit 0% exit 90%;
}
@keyframes settle{ to{ transform: translateY(-10px); opacity:.72; } }
```
Keep displacement ≤12px — anything more feels like parallax. **Impact:** M · **Effort:** Low.

### 10. Section rhythm: one idea per panel, breathing room as a feature
**Where seen:** the shared DNA of every cited SOTD — Units, NRG, Ten Years Away.
**Why it works:** pacing is mostly *whitespace and cadence*, not effects. Alternate full-bleed and inset
panels; give each a letterspaced eyebrow; use a consistent vertical scale so the eye learns the beat. The
reveals above only land because there's rest between them.
```css
:root{ --panel-pad: clamp(4.5rem, 12vh, 9rem); }
.panel{ padding-block: var(--panel-pad); }
.panel + .panel{ border-top: 1px solid color-mix(in srgb, var(--champagne) 22%, transparent); } /* hairline chapter break */
.panel__eyebrow{ font: .72rem/1 Inter; letter-spacing:.22em; text-transform:uppercase;
  color: color-mix(in srgb, var(--champagne) 85%, var(--pearl)); }
```
**Impact:** H · **Effort:** Low.

### 11. The single neon "night" moment, revealed on scroll (glow budget honored)
**Where seen:** the "one hero interaction" convention on hospitality SOTD; our own one-glow rule.
**Why it works:** reserve the `--neon` hot-pink for exactly one element and let *scroll* be what ignites it —
e.g. the "Open Late" tag or a CTA that gains its glow only when its panel is centered. Because only one panel is
centered at a time, the one-glow-per-viewport rule holds automatically.
```css
.night-mark{
  animation: ignite both; animation-timeline: view(); animation-range: cover 35% cover 60%;
}
@keyframes ignite{
  from{ color:var(--pearl); text-shadow:none; }
  to  { color:var(--neon);  text-shadow:0 0 18px color-mix(in srgb,var(--neon) 55%, transparent); }
}
```
**Impact:** M · **Effort:** Low.

### 12. `timeline-trigger` "play once on entry" (future-proofing, Chrome 145+)
**Where seen:** Chrome "Scroll-Triggered Animations."
**Why it works:** some reveals should play *once on their own clock* (a count-up of "334 shops", a line-draw)
rather than scrub with scroll. New `timeline-trigger` fires declaratively — the CSS replacement for a one-shot
IntersectionObserver. Treat as enhancement only; wrap in `@supports` and keep a static fallback.
```css
@supports (animation-trigger: --t) {
  .count { timeline-trigger: --t view() entry 20% exit 0%; }
  .count__num { animation: count-up 900ms both; animation-trigger: --t play-forwards; }
}
```
**Impact:** L (today) · **Effort:** Low — but low browser reach; ship as sugar, not structure.

---

## What now reads dated (avoid list)

- **Heavy JS scroll libs by default** — GSAP ScrollTrigger / Locomotive / AOS as the *engine* for basic fade-ups.
  In 2026 that's a payload and a jank source; `animation-timeline` does 90% of it at ~0 KB. Reserve JS libs for
  genuine pinning/inertia we can't get natively.
- **Full-page hijack / smooth-scroll interception** (`scroll-behavior` faked in JS, `wheel` handlers). Fights the
  user, breaks find-in-page and reduced-motion, tanks accessibility. Native snap + native smooth only.
- **Big-displacement parallax** (backgrounds sliding 40–100px, multi-layer depth). Reads 2018, causes vestibular
  discomfort. If any, ≤12px transform, opacity-led (move 9).
- **Everything fades in at once on load** (blanket `[data-aos] {opacity:0}` flashing FOUC, or a 40-item burst).
  Replaced by per-element view-timelines that reveal *as reached* (move 2).
- **Number counters that spin on page load** regardless of visibility, and looping marquees of logos. Distracting;
  if used, trigger on entry and run once (move 12).
- **Mandatory full-viewport vertical snap** (`scroll-snap-type: y mandatory` on the whole page). Trapping the user
  one-screen-at-a-time feels gimmicky and hostile on a content/directory site. Use snap only inside horizontal
  rails; `proximity` at most if ever vertical.
- **Scroll-triggered autoplay video/audio** and cursor-chasing blobs — off-brand for an honest, calm directory.
- **Bouncy/overshoot easing** (`cubic-bezier` with big overshoot, spring wobble on text). Off for an editorial
  serif brand; use soft ease-outs (`.22,.61,.36,1`).

---

## Recommended for Boba Night (the 3–5 to actually apply)

1. **Move 1 + 2 — reveal-on-enter & staggered card cascade** as the site-wide baseline. One `.reveal` utility
   and per-child view-timelines on the directory/featured grids. Highest impact, lowest effort, fully static,
   degrades to plain content. This alone lifts the homepage from "static list" to "paced editorial."

2. **Move 10 — deliberate section rhythm** (one idea per panel, hairline chapter breaks, letterspaced eyebrows,
   generous `--panel-pad`). This is the frame the reveals hang in; do it first structurally so pacing reads even
   with motion off. Pure layout, zero risk.

3. **Move 5 (+6 as enhancement) — one horizontal snap rail with peek** for "Featured tonight" or "By region."
   Provides the single rhythm-break the page needs. Ship the CSS rail everywhere; let scroll-markers/buttons
   progressively enhance on Chromium. Keeps mobile drag natural.

4. **Move 8 — one sticky-media / scrolling-caption scene** as the homepage's emotional center ("What a boba
   night looks like"), using our film grain + a real photo. This is the "expensive" moment; use it exactly once.

5. **Move 7 — cross-document View Transitions** for directory card → shop profile, built at generation time
   (`view-transition-name: shop-<slug>`). Turns 1,000 static pages into an SPA-smooth experience with one at-rule.
   Slightly more plumbing, but it's the move that makes a *multi-page* site feel authored end to end.

**Guardrails for all five:** everything wrapped in `@media (prefers-reduced-motion: no-preference)` **and**
`@supports (animation-timeline: view())`; transform/opacity/filter only; the champagne progress hairline and
rails never spend the neon glow — reserve `--neon` for the single "night" ignite (move 11), one per viewport.
