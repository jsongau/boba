# Nav, Mobile & Command Search — Design Research

Topic owner deliverable for **Boba Night** (bobanight.com). Scope: 4-slot bottom bars,
full-screen drawers with accordions, and cmd-K / command-palette search over a static index.
Everything below is synthesized from live 2025–2026 sources (studied, not pasted) and re-authored
as minimal, original snippets tuned to a static vanilla-JS site. Palette assumed: obsidian
`#0B0C0E`, pearl `#F4EFE7`, champagne hairline `#C5A46D`, one neon `#ff3f6f` per viewport.

---

## Sources studied

- **UX Patterns for Developers — Command Palette** (uxpatterns.dev) — canonical anatomy (trigger,
  input, grouped results, item, empty state) + the full ARIA combobox/listbox contract. Best single
  spec reference for the overlay.
- **dev.to — "I Rebuilt the Cmd-K Command Palette in ~60 Lines of JavaScript"** — the whole thing in
  vanilla JS: keydown trigger with `preventDefault`, subsequence fuzzy match, wraparound arrow nav.
  Directly portable to our stack.
- **buildmvpfast — "How to Add a Cmd+K Command Palette to Your SaaS (2026)"** — cmdk/shadcn patterns:
  hide-empty-groups, Backspace pops nested pages, and the key mobile truth: "there is no Cmd+K on a
  phone — give it a visible trigger."
- **Algolia — Autocomplete Keyboard Navigation** (algolia.com/doc) — Enter navigates, Cmd/Ctrl+Enter
  opens new tab, Shift+Enter new window; keyboard nav treated as core, not optional.
- **Algolia DocSearch — GitHub issue #1014 (WAI-ARIA 1.2 combobox)** — real-world gotchas of the
  combobox pattern; why `aria-activedescendant` (virtual focus) beats moving real focus into the list.
- **phone-simulator.com — "Mobile Navigation Patterns in 2026"** — bottom bar sizing (4–5 slots,
  48×48px targets), `env(safe-area-inset-bottom)`, hide-on-scroll, one-handed-reach stat.
- **UXPin — "Mobile Navigation Design: 8 Types (2026)"** & **Phone Simulator** — when a full-screen
  drawer beats a bottom bar (6+ destinations, deep IA), auto-close-on-select.
- **Destiner.io — "Designing a Command Palette"** — empty-state should suggest/recent, show shortcut
  hints ("waste of real estate not to show them"), highlight matched characters, alphabetical is bad.
- **Raycast Manual — Action Panel / Keyboard Shortcuts** — trailing shortcut pills, section grouping,
  and the aesthetic of a keyboard-first, dense-but-calm result list.
- **Codrops — navigation tag** (tympanus.net/codrops) — reference gallery for full-screen overlay
  menus with staggered/clip-path reveals (technique named below, snippet re-authored).

---

## Hot moves

### 1. Four-slot thumb bar with safe-area padding
**Where:** phone-simulator 2026, UXPin, near-universal in luxury commerce mobile (bottom bar for the
2–4 money destinations, hamburger for the long tail). **Why it works:** 60% of mobile use is
one-handed; the bottom 1/3 of the screen is the reachable zone. Four slots is the sweet spot — five
starts to crowd 44px targets on a 360px viewport. **Impact H / Effort L.**

```css
.tabbar{
  position:fixed; inset:auto 0 0 0; z-index:40;
  display:grid; grid-template-columns:repeat(4,1fr);
  background:color-mix(in srgb,#0B0C0E 88%, transparent);
  backdrop-filter:blur(14px) saturate(1.1);
  border-top:1px solid rgba(197,164,109,.28);        /* champagne hairline */
  padding-bottom:env(safe-area-inset-bottom);        /* home-indicator gap */
}
.tabbar a{min-height:48px; display:grid; place-items:center; gap:2px;
  font:500 11px/1 Inter; letter-spacing:.02em; color:#F4EFE7; text-decoration:none;}
.tabbar a[aria-current="page"]{color:#ff3f6f;}       /* the one neon per viewport */
```
Slots for Boba Night: **Directory · Near me · Search · Roulette**. Icons + 1-word labels, never
icons alone.

### 2. `aria-current="page"` active indicator, not a JS class
**Where:** editorial/luxury commerce nav. **Why:** the active tab is server-knowable on a static
multi-page site, so mark it in HTML — no JS, screen-reader-correct, and it doubles as your style hook
(`[aria-current="page"]`). The single neon glow lives here and nowhere else on screen. **Impact M /
Effort L.**

```css
.tabbar a[aria-current="page"]{position:relative;}
.tabbar a[aria-current="page"]::after{
  content:""; position:absolute; top:6px; width:4px; height:4px; border-radius:50%;
  background:#ff3f6f; box-shadow:0 0 8px 1px #ff3f6f;   /* the glow */
}
```

### 3. Hide-on-scroll-down, reveal-on-scroll-up bar
**Where:** Medium pattern cited by phone-simulator 2026. **Why:** gives content the full viewport
while reading a shop page, brings nav back the instant the user reverses intent. Transform-only, so
it's cheap and honors reduced-motion by simply not animating. **Impact M / Effort L.**

```css
.tabbar{transition:transform .28s cubic-bezier(.4,0,.2,1); will-change:transform;}
.tabbar.is-hidden{transform:translateY(110%);}
@media (prefers-reduced-motion:reduce){.tabbar{transition:none;}}
```
```js
let lastY = 0;
addEventListener('scroll', () => {
  const y = scrollY;
  bar.classList.toggle('is-hidden', y > lastY && y > 120); // hide going down, past hero
  lastY = y;
}, {passive:true});
```

### 4. Full-screen drawer with hairline accordions
**Where:** UXPin 2026 (drawer wins at 6+ destinations / deep IA), luxury editorial menus. **Why:**
Boba Night has 334 shops across cities/areas/best-of — too many for a bar. A full-screen overlay with
`<details>` accordions gives one calm scroll, groups collapsed by default, zero JS for open/close.
**Impact H / Effort L–M.**

```css
.drawer{position:fixed; inset:0; z-index:60; background:#0B0C0E;
  transform:translateY(-8px); opacity:0; visibility:hidden;
  transition:opacity .32s ease, transform .32s ease, visibility 0s .32s;}
.drawer[data-open]{opacity:1; visibility:visible; transform:none; transition-delay:0s;}
.drawer details{border-bottom:1px solid rgba(197,164,109,.22);}
.drawer summary{list-style:none; cursor:pointer; padding:18px 4px;
  font:400 22px/1.1 Fraunces,serif; color:#F4EFE7; display:flex; justify-content:space-between;}
.drawer summary::-webkit-details-marker{display:none;}
.drawer summary::after{content:"+"; color:#C5A46D; transition:transform .2s ease;}
.drawer details[open] summary::after{transform:rotate(45deg);}   /* + becomes x */
```
Native `<details>` = free accordion, keyboard-operable, works with JS off. Animate the panel height
only if you want polish (see move 8).

### 5. Staggered item reveal on drawer open (`--i` custom property)
**Where:** Codrops full-screen overlay menus. **Why:** the editorial "curtain" feel — items cascade
in 40ms apart. One CSS custom property per item drives the delay; no per-item JS. **Impact M /
Effort L.**

```css
.drawer li{opacity:0; transform:translateY(10px);
  transition:opacity .4s ease, transform .4s ease;
  transition-delay:calc(var(--i) * 40ms);}
.drawer[data-open] li{opacity:1; transform:none;}
@media (prefers-reduced-motion:reduce){
  .drawer li{transition:none; opacity:1; transform:none;}}
```
```html
<li style="--i:0">Directory</li><li style="--i:1">Best of</li><li style="--i:2">Cities</li>
```

### 6. cmd-K palette: global trigger with `preventDefault`
**Where:** dev.to 60-line rebuild, Linear/Vercel/Raycast. **Why:** ⌘K/Ctrl+K is the universal
"search everything" reflex now; `preventDefault()` stops the browser stealing it for native find.
On a static site the whole index (334 shops + city/area pages) can live in one JSON blob loaded once.
**Impact H / Effort M.**

```js
addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k'){ e.preventDefault(); palette.open(); }
  if (e.key === 'Escape') palette.close();
});
```

### 7. Subsequence fuzzy match over a static index
**Where:** dev.to rebuild (single-pointer subsequence), the Fuse.js-free approach. **Why:** "boba"
should surface "**B**iz **O**ff **B**rew **A**lley"-style non-adjacent matches without a library. A
scored variant (reward adjacency + word-start) ranks better than pure boolean. **Impact H / Effort L.**

```js
// returns -1 (no match) or a score (higher = better)
function fuzzyScore(q, text){
  q = q.toLowerCase(); text = text.toLowerCase();
  let qi = 0, score = 0, streak = 0;
  for (let ti = 0; ti < text.length && qi < q.length; ti++){
    if (text[ti] === q[qi]){
      streak++; score += streak;                        // reward consecutive hits
      if (ti === 0 || text[ti-1] === ' ') score += 4;   // reward word-start hits
      qi++;
    } else streak = 0;
  }
  return qi === q.length ? score : -1;
}
// results = index.map(x=>[x,fuzzyScore(q,x.name)]).filter(r=>r[1]>=0).sort((a,b)=>b[1]-a[1]);
```

### 8. The ARIA combobox/listbox contract + virtual focus
**Where:** uxpatterns.dev, Algolia DocSearch issue #1014. **Why:** the correct, tested accessibility
model. Real focus **stays in the input**; the "highlighted" result is tracked with
`aria-activedescendant` pointing at the option's id (virtual focus). Moving real DOM focus into the
list is the common bug (DocSearch #1014) — it breaks typing. **Impact H / Effort M.**

```html
<input role="combobox" aria-expanded="true" aria-controls="cmd-list"
       aria-activedescendant="opt-3" autocomplete="off">
<ul id="cmd-list" role="listbox">
  <li role="option" id="opt-3" aria-selected="true">Tiger Sugar — Irvine</li>
</ul>
<p role="status" aria-live="polite" class="sr-only">12 results</p>
```
Arrow keys mutate `aria-activedescendant` + a `.is-active` class; Enter runs the active option;
`role="status"` announces the result count politely.

### 9. Wraparound arrow-key navigation
**Where:** dev.to rebuild. **Why:** modulo arithmetic makes Down-from-last wrap to first and
Up-from-first wrap to last — one line each, feels like Raycast/Linear. Keep the active row scrolled
into view. **Impact M / Effort L.**

```js
function move(delta){
  sel = (sel + delta + shown.length) % shown.length;   // wraparound
  rows.forEach((r,i)=>r.classList.toggle('is-active', i===sel));
  input.setAttribute('aria-activedescendant', rows[sel].id);
  rows[sel].scrollIntoView({block:'nearest'});
}
// ArrowDown -> move(1); ArrowUp -> move(-1); Enter -> shown[sel].run();
```

### 10. Grouped results with auto-hiding section headings
**Where:** buildmvpfast/cmdk, Raycast Action Panel. **Why:** split results into buckets — **Shops ·
Cities · Areas · Pages** — so a 40-result list stays scannable. When a group filters to zero, hide
its heading (orphan headings look broken). **Impact M / Effort L.**

```js
for (const g of groups){
  const hits = g.items.filter(matches);
  g.el.hidden = hits.length === 0;      // heading + list hidden together
  g.headEl.hidden = hits.length === 0;
}
```
Optional: cap each group (e.g. top 5) with a "+18 more shops → search" affordance.

### 11. Trailing shortcut / meta pills on result rows
**Where:** Raycast, Destiner.io. **Why:** the right edge of each row is free real estate — show the
neighborhood, the "OPEN" status, or a ⏎ hint. Champagne micro-caps keep it editorial, not techy.
**Impact M / Effort L.**

```css
.cmd-row{display:flex; align-items:center; gap:12px; padding:11px 14px;}
.cmd-row .meta{margin-left:auto; font:600 10px/1 Inter; letter-spacing:.14em;
  text-transform:uppercase; color:#C5A46D;}
.cmd-row.is-active{background:rgba(255,63,111,.08);
  box-shadow:inset 2px 0 0 #ff3f6f;}   /* left neon rule = the one glow */
```

### 12. Empty-state that suggests instead of going blank
**Where:** Destiner.io (blank input field = bad), GitHub/Raycast. **Why:** before the user types,
show recent searches (localStorage) and 3–4 curated jumps ("Open now near me", "Taro drinks",
"Best of LA"). Turns a dead overlay into a discovery surface. **Impact M / Effort L.**

```js
function render(q){
  const list = q ? results(q) : recent().concat(SUGGESTED);
  emptyEl.hidden = !(q && list.length === 0);   // real "no matches" only when typed
  paint(list);
}
```

### 13. Highlight matched characters in results
**Where:** Destiner.io. **Why:** shows the user *why* a fuzzy result matched — builds trust in the
search. Wrap matched indices in `<mark>`; style with champagne underline, not a highlighter block.
**Impact L–M / Effort L.**

```css
.cmd-row mark{background:none; color:#F4EFE7;
  border-bottom:1px solid #C5A46D; padding-bottom:1px;}
```

### 14. One visible search trigger (because phones have no ⌘K)
**Where:** buildmvpfast ("there is no Cmd+K on a phone"). **Why:** the palette is a core path on
mobile, so it needs a real tappable entry — the center bottom-bar slot doubles as the ⌘K opener on
desktop and the search button on touch. Show the `⌘K` hint pill only on pointer:fine. **Impact H /
Effort L.**

```css
.kbd-hint{display:none;}
@media (pointer:fine){.kbd-hint{display:inline-block;
  border:1px solid rgba(197,164,109,.4); border-radius:2px; padding:1px 5px;
  font:600 10px/1 Inter; color:#C5A46D;}}
```

### 15. Scrim + scroll-lock + focus-trap when overlay is open
**Where:** uxpatterns.dev focus-management guidance. **Why:** an open drawer or palette must trap
Tab, lock body scroll, and restore focus to the trigger on close — the difference between "modal" and
"broken". **Impact M / Effort M.**

```js
function open(){
  lastFocused = document.activeElement;
  document.body.style.overflow = 'hidden';
  el.dataset.open = ''; input.focus();
}
function close(){
  delete el.dataset.open; document.body.style.overflow = '';
  lastFocused?.focus();          // return focus where it came from
}
// trap: on Tab, if focus leaves el, loop to first/last focusable inside el
```

---

## What now reads dated (avoid list)

- **Icons-only bottom bars** with no labels — 2026 guidance is icon **+** 1-word label; unlabeled
  glyphs test badly.
- **Five+ crammed tab slots** on a 360px viewport — targets fall below 44px. Cap at 4 here.
- **Slide-in-from-left hamburger drawer that only covers 80% width** with a peek of page behind —
  reads as a 2018 template. Go full-screen or use the bottom bar.
- **Nested multi-level dropdowns on touch** (hover-intent menus) — undiscoverable, un-tappable. Use
  `<details>` accordions instead.
- **Bouncy spring / overshoot menu animations** — clashes with an obsidian editorial tone. Use short
  ease-out, transform+opacity only.
- **Search that only matches from the start of the string** (`startsWith`) — feels dumb next to any
  fuzzy palette. Also: alphabetical-only result ordering (Destiner: "equally useless").
- **Moving real DOM focus into the results list** — the DocSearch #1014 bug; breaks typing. Use
  `aria-activedescendant` virtual focus.
- **A modal search that blanks to an empty input** — waste of the surface; always seed with
  recent/suggested.
- **Blur-heavy frosted glass everywhere** — reserve `backdrop-filter` for the one bar/overlay;
  full-page blur tanks scroll perf on mid phones.

---

## Recommended for Boba Night (apply these 5)

1. **Four-slot thumb bar — Directory · Near me · Search · Roulette** (moves 1, 2, 3, 14). Fixed,
   safe-area-padded, hide-on-scroll, `aria-current` neon dot as the single glow. The center Search
   slot is also the ⌘K opener on desktop. Highest ROI, lowest effort.

2. **Full-screen drawer built on native `<details>` accordions** (moves 4, 5, 15) for the long tail —
   Cities, Areas, Best-of, About/How-we-rank. Fraunces summaries, champagne hairline dividers,
   staggered `--i` reveal, `+`→`×` marker. Works with JS off.

3. **cmd-K / tap-to-search command palette over a static JSON index** (moves 6, 7, 8, 9) — one index
   of 334 shops + city/area/guide pages, subsequence scored fuzzy match, wraparound arrows, correct
   combobox/listbox ARIA with virtual focus. This is the flagship interaction.

4. **Grouped, pill-annotated results** (moves 10, 11, 13) — Shops · Cities · Areas · Pages, each row
   with a champagne micro-caps neighborhood/OPEN pill and matched-char underlines, active row marked
   by an inset neon left-rule (the overlay's one glow). Honesty brand: the pill shows real
   open/closed status, never a fake rating.

5. **Discovery-first empty state** (move 12) — recent searches (localStorage) plus curated jumps
   ("Open now near me", "Taro drinks", "Best of LA"). Turns the palette into a browse surface, not
   just a lookup.

All five are CSS-first, transform/opacity-only, `prefers-reduced-motion`-honored, and degrade
gracefully with JavaScript disabled (bar + `<details>` drawer keep working; the palette becomes a
plain link to a `/search` page).
