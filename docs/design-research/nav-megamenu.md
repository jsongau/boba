# Navigation — Mega Menus & Headers (Design Research)

Research for **Boba Night** (bobanight.com) — dark obsidian editorial boba directory.
Topic: award-tier multi-panel mega menus and sticky headers on dark / editorial / luxury sites.
Scope: panel entrance choreography, left-rail → right-pane region swaps, progressive-blur scrims,
hover-intent, focus-visible, disclosure semantics.

Palette reminders used in snippets below:
`--obsidian:#0B0C0E; --pearl:#F4EFE7; --champagne:#C5A46D; --neon:#ff3f6f;`
House rules honored: CSS-first, transform/opacity only, `prefers-reduced-motion`, hairline borders,
2px radii, **one glowing element per viewport max**.

---

## Sources studied

- **W3C ARIA APG — Disclosure Navigation** (w3.org/WAI/ARIA/apg) — the canonical accessible pattern:
  `<button aria-expanded aria-controls>` per top item, `hidden` panels, Escape returns focus, focus
  leaving the region closes panels (satisfies WCAG 1.4.13). This is the skeleton every move below hangs on.
- **kennethnym.com — "Progressive blur in CSS"** — exact 7-layer stacked `backdrop-filter` + `mask-image`
  recipe (blur 1→64px, overlapping gradient bands). The reference implementation of the Apple scrim.
- **devslovecoffee.com — "Making Apple Progressive Blur on the Web"** — same stacked-layer technique plus a
  key gotcha: Chromium mis-renders `border-radius` when many stacked backdrop-filters + mask + `overflow:hidden`
  combine; Safari/Firefox are clean. Keep progressive-blur scrims on flat (non-rounded) edges.
- **Max Mega Menu — "What is Hover Intent"** — the intent algorithm: don't open on raw `mouseenter`; wait for the
  cursor to slow/settle (~300ms timeout, ~100ms sample interval) and give a grace period on exit so a diagonal
  trip to the panel doesn't dismiss it.
- **Awwwards — Menu / Navigation collections** (awwwards.com/websites/navigation, /awwwards/collections/menu)
  — current award-tier surveys the choreography vocabulary: full-bleed overlay panels, staggered link reveals,
  left-rail category → right-pane image swap, clip-path/mask wipes.
- **Digital Silk & RSA Creative — 2026 mega-menu roundups** — real named examples (ASOS multi-column + right-side
  imagery; Figma product-mirrored columns; Adidas full-width panel with breakpoint-stable spacing) and a solid
  "what to avoid" list (vague labels, everything-equal hierarchy, mobile as an afterthought).
- **MDN / CSS-Tricks — `:focus-visible`, `inert`, View Transitions** — spec backing for keyboard-only focus rings,
  trapping background interaction, and cross-state morphing.

---

## Hot moves

### 1. Progressive-blur sticky header scrim (the Apple move)
**Where seen:** Apple Music/Photos headers; kennethnym + devslovecoffee recreations.
**Why it works:** A hard `backdrop-filter: blur()` band has a visible seam where it ends. A *progressive* scrim
fades blur from strong (behind the logo/nav) to zero, so content dissolves under the header instead of hitting a
line. On a dark editorial site it reads expensive and keeps pearl text legible over any hero.

Two implementations — pick by budget:

Cheap single-layer (one seam, masked so the seam is soft):
```css
.site-header{
  position: sticky; top: 0;
  -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
  background: linear-gradient(180deg, rgba(11,12,14,.72), rgba(11,12,14,.30));
  /* fade the blur out at the bottom edge so there's no hard cut */
  -webkit-mask-image: linear-gradient(180deg, #000 62%, transparent);
          mask-image: linear-gradient(180deg, #000 62%, transparent);
}
```

True progressive blur (stacked layers, Apple-grade) — a pseudo-element or fixed overlay of thin bands, each with
more blur, each masked to a lower slice, overlapping so it ramps smoothly:
```css
.blur-scrim{ position:fixed; inset:0 0 auto 0; height:96px; pointer-events:none; z-index:40; }
.blur-scrim > i{ position:absolute; inset:0; }
.blur-scrim > i:nth-child(1){ backdrop-filter:blur(1px);  mask-image:linear-gradient(#000 0%,#000 30%,transparent 40%);}
.blur-scrim > i:nth-child(2){ backdrop-filter:blur(2px);  mask-image:linear-gradient(transparent 10%,#000 20%,#000 40%,transparent 50%);}
.blur-scrim > i:nth-child(3){ backdrop-filter:blur(4px);  mask-image:linear-gradient(transparent 20%,#000 40%,#000 60%,transparent 70%);}
.blur-scrim > i:nth-child(4){ backdrop-filter:blur(8px);  mask-image:linear-gradient(transparent 40%,#000 60%,#000 80%,transparent 90%);}
.blur-scrim > i:nth-child(5){ backdrop-filter:blur(16px); mask-image:linear-gradient(transparent 60%,#000 80%);}
```
**Gotcha (from devslovecoffee):** don't wrap stacked backdrop-filters in `overflow:hidden` + `border-radius` —
Chromium mangles the corners. Keep the scrim a flat full-bleed band (fine for a header).
**Impact:** H — **Effort:** M (single-layer is S).

---

### 2. Hover-intent gate (open on settle, not on brush-past)
**Where seen:** Amazon "aim triangle"; Max Mega Menu hover-intent docs.
**Why it works:** Opening a panel the instant the cursor grazes a tab is the #1 thing that makes a mega menu feel
cheap and twitchy. Waiting for the pointer to *slow down* before committing, and forgiving a diagonal exit toward
the panel, is the single biggest perceived-quality upgrade.
```js
function hoverIntent(trigger, {onOpen, onClose, openDelay=140, closeDelay=260}={}){
  let openT, closeT, lastX, lastY, slow=false;
  trigger.addEventListener('pointermove', e=>{
    const fast = Math.hypot(e.clientX-(lastX??e.clientX), e.clientY-(lastY??e.clientY)) > 8;
    lastX=e.clientX; lastY=e.clientY; slow=!fast;
  });
  trigger.addEventListener('pointerenter', ()=>{
    clearTimeout(closeT);
    openT=setTimeout(()=>{ if(slow) onOpen(); }, openDelay); // only if cursor settled
  });
  trigger.addEventListener('pointerleave', ()=>{
    clearTimeout(openT);
    closeT=setTimeout(onClose, closeDelay); // grace period to reach the panel
  });
}
```
Pair with `pointer` events so touch falls through to a click/tap toggle instead of firing hover.
**Impact:** H — **Effort:** S.

---

### 3. Staggered link reveal (choreographed entrance, not a fade-in blob)
**Where seen:** Awwwards navigation collection overlays; standard award-tier vocabulary.
**Why it works:** Panel items rising + fading in sequence reads as *composed*. The trick is a single CSS custom
property `--i` per item driving `transition-delay`, so no JS timers and it reverses cleanly on close.
```css
.panel [data-item]{
  opacity:0; transform:translateY(8px);
  transition:opacity .38s ease, transform .38s cubic-bezier(.2,.7,.2,1);
  transition-delay: calc(var(--i) * 40ms);
}
.panel[data-open] [data-item]{ opacity:1; transform:none; }
@media (prefers-reduced-motion: reduce){
  .panel [data-item]{ transition:opacity .2s; transform:none; transition-delay:0ms; }
}
```
```html
<a data-item style="--i:0">Best Boba</a>
<a data-item style="--i:1">By City</a>
<a data-item style="--i:2">Near Me</a>
```
Cap the stagger (~6–8 items × 40ms = ~320ms) so the last item isn't slow. **Impact:** H — **Effort:** S.

---

### 4. Left-rail → right-pane region swap (the editorial mega-menu spine)
**Where seen:** ASOS (categories left, imagery right); luxury fashion nav; Awwwards menu collection.
**Why it works:** A two-region panel — a slim left rail of categories, a large right pane that swaps content as
you move down the rail — turns a flat link list into a browsable surface. For Boba Night the right pane is a live
preview: hovering "By City" shows the LA/OC/SGV split; hovering "Best" shows the editorial pick with a shop card.
Only the right pane crossfades, so the rail stays a stable anchor.
```html
<div class="mega" role="group">
  <ul class="mega__rail" role="menu">
    <li><button role="menuitem" aria-controls="pane-cities" data-rail>By City</button></li>
    <li><button role="menuitem" aria-controls="pane-best"   data-rail>Best Of</button></li>
  </ul>
  <div class="mega__pane">
    <section id="pane-cities" data-pane>…</section>
    <section id="pane-best"   data-pane hidden>…</section>
  </div>
</div>
```
```css
.mega{ display:grid; grid-template-columns:minmax(200px,1fr) 2.4fr; }
.mega__rail{ border-right:1px solid rgba(197,164,109,.22); } /* champagne hairline */
[data-pane]{ opacity:0; transition:opacity .3s ease; }
[data-pane].is-active{ opacity:1; }
[data-rail][aria-current="true"]{ color:var(--pearl); }
```
JS: on `pointerenter`/`focus` of a rail item, `hidden` off the target pane, crossfade, set `aria-current`.
Debounce the swap through the same hover-intent gate (move #2) so dragging down the rail doesn't strobe.
**Impact:** H — **Effort:** M.

---

### 5. Clip-path / mask wipe panel entrance (instead of height animation)
**Where seen:** Awwwards overlay menus; Codrops menu-reveal demos.
**Why it works:** Animating `height` or `max-height` is janky (layout thrash) and the classic dated tell. A
`clip-path: inset()` or masked wipe animates on the compositor, stays buttery, and gives a directional
"unfurl" that feels intentional. The panel is always laid out at full size; only its reveal region animates.
```css
.mega{
  clip-path: inset(0 0 100% 0);              /* collapsed from the bottom */
  transition: clip-path .42s cubic-bezier(.16,1,.3,1);
  will-change: clip-path;
}
.mega[data-open]{ clip-path: inset(0 0 0 0); }
```
Because the box keeps its real height, the header hairline and drop shadow settle in place — no reflow bounce.
**Impact:** M — **Effort:** S.

---

### 6. Full-page progressive-blur scrim behind the open panel
**Where seen:** iOS sheets; luxury site overlay menus.
**Why it works:** When a mega panel opens, blurring + darkening the rest of the page focuses attention and makes
the panel feel like a layer, not a box glued to the header. Progressive (stronger toward the panel) beats a flat
dim. This is also where Boba Night can spend its *one glow*: a faint `--neon` hairline on the panel's leading
edge against the blurred obsidian.
```css
.scrim{
  position:fixed; inset:0; z-index:30; opacity:0; pointer-events:none;
  background: radial-gradient(120% 80% at 50% 0%, rgba(11,12,14,.2), rgba(11,12,14,.85));
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
  transition: opacity .3s ease;
}
.scrim[data-open]{ opacity:1; pointer-events:auto; }
```
Clicking the scrim closes the menu; give it `aria-hidden="true"` and drive close from a real Escape handler too.
**Impact:** M — **Effort:** S.

---

### 7. `inert` the background while a panel/overlay is open
**Where seen:** modern a11y-forward nav overlays; MDN `inert`.
**Why it works:** When a full overlay menu is open, Tab should stay inside it — not wander into the page behind
the scrim. `inert` removes everything else from the tab order and pointer/AT reach in one attribute, replacing
fragile focus-trap loops.
```js
function openMenu(){
  panel.hidden = false; panel.dataset.open = '';
  document.getElementById('main').inert = true;   // everything else untabbable
  panel.querySelector('a,button')?.focus();
}
function closeMenu(){
  panel.dataset.open ? delete panel.dataset.open : 0;
  document.getElementById('main').inert = false;
  trigger.focus();                                 // return focus to opener (WCAG)
}
```
**Impact:** M (accessibility) — **Effort:** S.

---

### 8. `:focus-visible` keyboard-only glow ring
**Where seen:** MDN/CSS-Tricks; every current accessible nav.
**Why it works:** Mouse users never see an ugly outline; keyboard users get a crisp, high-contrast ring. On dark
obsidian a champagne or thin neon ring reads as designed, not default-browser. Keep the ring for keyboard only so
it doesn't fight the "one glow per viewport" rule during mouse use.
```css
.nav a, .nav button{ outline:none; }
.nav a:focus-visible, .nav button:focus-visible{
  outline:2px solid var(--champagne);
  outline-offset:3px; border-radius:2px;
}
```
**Impact:** M — **Effort:** S.

---

### 9. Shrink-on-scroll header (compact after threshold, not per-frame)
**Where seen:** editorial/luxury sticky headers; 2026 sticky-header roundups.
**Why it works:** Header starts tall and airy at the top of the page, then collapses to a compact bar once you
scroll past the hero — more reading room, and the transition signals "you've left the top." Do it with a class
toggled by `IntersectionObserver` (a sentinel at the top), animating `transform`/`padding`, NOT a scroll listener
that runs every frame.
```js
const sentinel = document.querySelector('#top-sentinel');
new IntersectionObserver(([e])=>{
  document.body.classList.toggle('is-scrolled', !e.isIntersecting);
},{rootMargin:'-8px 0px 0px 0px'}).observe(sentinel);
```
```css
.site-header{ transition: padding .3s ease, background .3s ease; padding-block:20px; }
.is-scrolled .site-header{ padding-block:10px; background:rgba(11,12,14,.8); }
.is-scrolled .brand{ transform:scale(.9); transform-origin:left center; }
```
**Impact:** M — **Effort:** S.

---

### 10. Champagne hairline underline wipe on nav hover
**Where seen:** editorial nav bars; Awwwards menu detailing.
**Why it works:** A hairline that wipes in from the left under the active/hovered tab is the quiet luxury detail —
it uses `transform:scaleX` (compositor-only) and `transform-origin` flips so it retracts the way it came. Pairs
with the champagne hairline system already in the brand.
```css
.nav a{ position:relative; }
.nav a::after{
  content:""; position:absolute; left:0; right:0; bottom:-4px; height:1px;
  background:var(--champagne); transform:scaleX(0); transform-origin:right;
  transition:transform .32s cubic-bezier(.2,.7,.2,1);
}
.nav a:hover::after, .nav a[aria-current="page"]::after{ transform:scaleX(1); transform-origin:left; }
```
**Impact:** M — **Effort:** S.

---

### 11. Single shared close-choreography (reverse-on-close for free)
**Where seen:** polished overlay menus generally.
**Why it works:** Cheap menus snap shut instantly (or worse, mid-animation). Driving open/close from one
`data-open` attribute and letting the *same* transitions run in reverse — plus `hidden` only applied on
`transitionend` — makes closing feel as considered as opening.
```js
function toggle(open){
  if(open){ panel.hidden=false; requestAnimationFrame(()=>panel.dataset.open=''); }
  else{
    delete panel.dataset.open;
    panel.addEventListener('transitionend', ()=>{ if(!('open' in panel.dataset)) panel.hidden=true; }, {once:true});
  }
  trigger.setAttribute('aria-expanded', String(open));
}
```
**Impact:** M — **Effort:** S.

---

### 12. View Transitions for the mobile full-screen menu (progressive enhancement)
**Where seen:** 2025–26 sites adopting the View Transitions API.
**Why it works:** On the mobile full-screen takeover, a same-document view transition morphs the hamburger into
the panel and back with a crossfade the browser choreographs — no manual keyframes. Fully progressive: wrap in a
capability check and it silently no-ops on unsupported browsers.
```js
function openMobile(){
  if(!document.startViewTransition){ return openMenu(); }
  document.startViewTransition(()=> openMenu());
}
```
```css
@media (prefers-reduced-motion: reduce){ ::view-transition-group(*){ animation:none; } }
```
**Impact:** M — **Effort:** S.

---

## What now reads dated (avoid list)

- **Open-on-`mouseenter` with zero intent gate** — the twitchy panel that fires when you brush past. Instant tell.
- **Animating `height` / `max-height`** for panel open — janky, non-composited, bouncy. Use `clip-path`/mask/opacity.
- **Flat hard `backdrop-filter` band** with a visible seam where the blur ends — replace with a masked or
  progressive scrim.
- **`transition: all`** on nav elements — animates layout props, stutters. Name `opacity, transform, clip-path` only.
- **jQuery hoverIntent + slideToggle** stacks — heavy, and the slide is the dated motion. Vanilla + CSS now.
- **Removing focus outlines entirely** (`outline:none` with no `:focus-visible` replacement) — breaks keyboard use.
- **Everything-equal mega panels** — 40 links at one weight, vague headers ("Solutions", "Resources", "More").
  Group, weight, and label concretely (Digital Silk roundup).
- **Mobile as a collapsed desktop menu** — award-tier treats mobile as its own full-screen takeover, not an
  accordion of the desktop tree.
- **Big neon drop-shadows / glows on multiple elements** — off-brand here anyway (one glow rule) and reads 2019.
- **Scroll-jacked headers** that recompute on every `scroll` event — use `IntersectionObserver` + a class toggle.

---

## Recommended for Boba Night (apply these 5)

1. **Hover-intent gate (#2) + shared open/close choreography (#11 / #1 single-layer scrim).** The foundation:
   panels that open when you *mean it* and close as gracefully as they open. Biggest perceived-quality jump for
   the least code. Effort S.
2. **Left-rail → right-pane region swap (#4)** for the primary "Explore" mega menu. The right pane previews a real
   shop card / city split — turns navigation into browsing, which is the whole point of a directory. This is the
   marquee move. Effort M.
3. **Progressive-blur sticky header scrim (#1).** Dark editorial content dissolving under a soft-fading header is
   the single most "expensive-looking" cheap win, and it keeps pearl nav text legible over any hero. Start with
   the single-layer masked version; upgrade to stacked only if the seam bugs you. Effort M.
4. **Accessibility spine: ARIA disclosure semantics + `inert` background (#7) + `:focus-visible` champagne ring
   (#8) + Escape-returns-focus.** Non-negotiable and cheap; makes the fancy panels keyboard- and SR-usable. This
   is also on-brand (honesty brand → don't fake accessibility either). Effort S.
5. **Staggered link reveal (#3) + champagne hairline underline wipe (#10)** as the signature motion texture,
   with the panel's single neon leading-edge hairline as the *one glow per viewport*. Both are transform/opacity
   only and reduced-motion safe. Effort S.

Hold in reserve: clip-path wipe (#5), shrink-on-scroll (#9), and View Transitions mobile takeover (#12) — all
strong, but layer them in after the five above land so the nav doesn't over-animate.
