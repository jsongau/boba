# Homepage Above-the-Fold — Directory & City-Guide Research

**Topic:** Winning the first 5 seconds on a venue-discovery / city-guide homepage — identity+proof headlines, hero search vs. browse, single trust-stat lines.
**For:** Boba Night (bobanight.com) — dark obsidian editorial boba directory, 334 SoCal shops.
**Date:** 2026-07-17
**Constraints honored below:** CSS-first, transform/opacity only, `prefers-reduced-motion`, ONE neon element per viewport, Fraunces + Inter, hairline champagne rules, film grain, 2px radii, no fake ratings (honesty brand).

---

## Sources studied

- **The Infatuation** (theinfatuation.com) — Live homepage. Headline is a conversational *promise*, not a boast: "let us help you make a decision." Browse-first (no giant hero search); curated city hubs (NYC/LA/Miami/…) and named guides ("The 23 Best Burritos In America") do the work. Rating scores (8.5/8.3) live on cards, not the hero. Lesson: **editorial voice + browse beats a search box when your value is curation.**
- **Resy** (resy.com) — Tagline "Right This Way," meta promise "Discover restaurants to love in your city and beyond." Directional, action-first brand; hero leans on a location/date **search** because the job-to-be-done is *book now*. Lesson: search-first only when the user already knows they want to transact.
- **Michelin Guide** (guide.michelin.com) — Fetch blocked (403), studied from prior knowledge: authority signaled by restraint, a single credential line ("The MICHELIN Guide"), and category/city browse rather than a loud search. Noted as blocked, moved on.
- **Monocle brand teardown** (visualjournalcraft.com) — Serif/sans pairing (Plantin headlines for "literary authority" + Helvetica Neue for data/captions), a **rigid multi-column grid**, hairline structure, restrained palette (wood/brass/dark). Authority comes from *rigorously applied consistency*, not decoration. Directly maps to Boba Night's Fraunces+Inter, champagne hairlines, obsidian.
- **Cereal magazine** (siiimple.com/cereal-magazine) — Reference for calm editorial whitespace, oversized serif display, muted palette, photography-as-anchor. Lesson: negative space *is* the luxury signal.
- **memorable.design — Hero Section Examples 2026** — Codifies the "single trust-stat bar" ("Trusted by 5,000+…" / 5-star line directly above the fold), one primary CTA + reassurance micro-copy, and Dark-Mode-High-Contrast as a named 2026 pattern. Static layouts over motion.
- **sitebuilderreport — 40+ Hero Examples (2026)** — Benefit-led headlines beat feature headlines; pair a headline with a credibility subtitle (counts / years / guarantee) for instant reassurance.
- **Codrops — kinetic typography / SVG letter reveals**; **studiomeyer / upskillist kinetic-typography 2026** — Current appetite for restrained letter/word reveals on the headline (mask + translateY), variable-font weight shifts, NOT full-screen motion. Use as garnish on one line only.
- **web.dev / MDN — fluid type & container queries** — `clamp()` for headline scaling, `text-wrap: balance/pretty` for ragged-right editorial headlines. Baseline-safe in 2026.

---

## Hot moves

### 1. Identity + proof headline (promise, not brag)
**Where:** Infatuation ("let us help you make a decision"), Resy ("Right This Way").
**Why:** The best directory heroes state *what the user gets*, in the brand's voice, in ≤7 words — then let one honest stat prove it. Boba Night's honesty brand forbids fake ratings, so the proof is the *count and coverage*, not stars.
**Snippet (copy pattern, not code):**
`Eyebrow: SOUTHERN CALIFORNIA · BOBA` → `H1: Find your after-dark boba.` → `Proof line: 334 shops. Every one visited, none paid to be here.`
**Impact:** H · **Effort:** Low (copy + one `<p>`).

### 2. Single trust-stat line (one number, hairline-framed)
**Where:** memorable.design "social proof bar"; sitebuilderreport credibility subtitle.
**Why:** One quantified line under the H1 kills skepticism before the scroll. Directories win by making the number *scope* (shops/cities), not *ratings*. Frame it in champagne hairline to read as a credential, not marketing.
```css
.hero__proof{
  display:inline-flex; gap:.75rem; align-items:center;
  padding:.5rem .9rem; border:1px solid var(--champagne,#C5A46D);
  border-radius:2px; color:var(--pearl,#F4EFE7);
  font:400 .8125rem/1 "Inter",sans-serif; letter-spacing:.02em;
}
.hero__proof b{font-variant-numeric:tabular-nums; color:#fff}
.hero__proof .dot{width:4px;height:4px;border-radius:50%;background:var(--champagne)}
```
**Impact:** H · **Effort:** Low.

### 3. Letterspaced eyebrow/kicker above the H1
**Where:** Monocle, Cereal, most editorial guides.
**Why:** A tiny uppercase tracked label ("SOUTHERN CALIFORNIA · BOBA GUIDE") sets category + place in one glance and reads as journalism, not ads. It is the cheapest "editorial authority" signal there is.
```css
.hero__eyebrow{
  font:600 .75rem/1 "Inter",sans-serif;
  text-transform:uppercase; letter-spacing:.22em;
  color:var(--champagne,#C5A46D); margin-bottom:1rem;
}
```
**Impact:** M · **Effort:** Low.

### 4. Fluid serif display headline with `clamp()` + balanced wrap
**Where:** Cereal/Monocle oversized serif; web.dev fluid-type guidance.
**Why:** One big Fraunces line that scales smoothly from phone to desktop with no breakpoints, and wraps ragged-right like a magazine masthead. `text-wrap:balance` prevents an orphan word; `pretty` for the proof line.
```css
.hero__h1{
  font-family:"Fraunces",serif; font-weight:340;
  font-size:clamp(2.5rem, 6vw + 1rem, 5.5rem);
  line-height:1.02; letter-spacing:-.015em;
  text-wrap:balance; color:var(--pearl,#F4EFE7);
  font-optical-sizing:auto; /* Fraunces is optical */
}
```
**Impact:** H · **Effort:** Low.

### 5. Browse-first hero (chips), not a naked search box
**Where:** Infatuation (curated city hubs + named guides).
**Why:** When the value is *curation*, a row of destination chips (cities / "open now" / "late-night") out-converts a search field — users don't know what to type, but they'll tap "Late-night · San Gabriel." Search can live in the nav; the hero sells the map.
```css
.hero__chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.75rem}
.hero__chip{
  padding:.55rem .95rem; border:1px solid rgba(197,164,109,.35);
  border-radius:2px; background:transparent; color:var(--pearl);
  font:500 .875rem/1 "Inter",sans-serif; cursor:pointer;
  transition:border-color .18s ease, transform .18s ease;
}
.hero__chip:hover{border-color:var(--champagne); transform:translateY(-1px)}
```
**Impact:** H · **Effort:** Low–Med (wire chips to existing city/filter routes).

### 6. Search-first hero — only if the job is "go now"
**Where:** Resy (location/date fields front and center).
**Why:** Counter-move to #5. If Boba Night's primary intent is "what's open near me *right now*," a single location/near-me input beats browse. Given the "after-dark" positioning, a lightweight **"Open now near me"** field is defensible — but pick ONE of #5 or #6 as the hero's spine, don't show both loudly.
```html
<form class="hero__near" role="search" aria-label="Find boba near you">
  <input type="search" placeholder="City or neighborhood" aria-label="Location">
  <button type="submit">Open now →</button>
</form>
```
**Impact:** M · **Effort:** Med (needs geolocation/route logic).

### 7. THE one neon element — a single glowing accent (brand rule)
**Where:** memorable.design "Dark-Mode-High-Contrast"; your brief's one-neon rule.
**Why:** On obsidian, exactly one `#ff3f6f` glow earns all the attention — put it on the primary CTA or a single live "Open now" dot. Everything else stays pearl/champagne. Scarcity is what makes it read as premium, not gamer-RGB.
```css
.hero__cta{
  color:#fff; background:transparent;
  border:1px solid #ff3f6f; border-radius:2px;
  padding:.8rem 1.4rem; font:600 .9375rem "Inter",sans-serif;
  box-shadow:0 0 0 rgba(255,63,111,0);
  transition:box-shadow .25s ease, background .25s ease;
}
.hero__cta:hover{background:rgba(255,63,111,.08); box-shadow:0 0 24px -4px rgba(255,63,111,.55)}
/* live dot alt: a single pulsing #ff3f6f dot next to "Open now" */
@media (prefers-reduced-motion:reduce){ .hero__cta{transition:none} }
```
**Impact:** H · **Effort:** Low.

### 8. Champagne hairline as structure (rules, not boxes)
**Where:** Monocle rigid grid; editorial guides generally.
**Why:** Thin `1px` champagne rules dividing eyebrow / headline / proto-nav do the framing that heavy cards would, keeping the fold airy and expensive-looking. Use `0.5px`-feel via low-opacity champagne on hi-dpi.
```css
.hero__rule{height:1px;background:linear-gradient(90deg,rgba(197,164,109,.55),rgba(197,164,109,0));border:0}
```
**Impact:** M · **Effort:** Low.

### 9. Masked line reveal on the headline (transform/opacity only)
**Where:** Codrops letter/word reveals; studiomeyer kinetic-type 2026 (restrained).
**Why:** One headline that rises out of a mask on load reads as crafted without any layout jank. Pure CSS, GPU-only, and fully gated by reduced-motion. Do it on the H1 *only* — not the whole fold.
```css
.reveal{overflow:hidden}
.reveal>span{display:inline-block; transform:translateY(105%); opacity:0;
  animation:rise .7s cubic-bezier(.16,1,.3,1) forwards}
.reveal>span:nth-child(2){animation-delay:.08s}
@keyframes rise{to{transform:translateY(0);opacity:1}}
@media (prefers-reduced-motion:reduce){
  .reveal>span{animation:none;transform:none;opacity:1}}
```
**Impact:** M · **Effort:** Low (wrap 2–3 line spans).

### 10. Film-grain + subtle vignette over obsidian (depth without images)
**Where:** Cereal/Monocle material warmth; dark-editorial trend.
**Why:** A fixed grain layer + radial vignette gives the black background texture and focuses the eye center-fold, so the hero doesn't need a hero *photo* to feel rich. Keep it a non-interactive overlay at low opacity.
```css
.grain{position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.05;
  background-image:url("data:image/svg+xml,...fractalNoise..."); mix-blend-mode:overlay}
.hero{background:radial-gradient(120% 90% at 50% 30%, #14161a 0%, #0B0C0E 70%)}
```
**Impact:** M · **Effort:** Low (SVG `feTurbulence` grain, or 1 tiny PNG).

### 11. Tabular-numeral stat + "how we count" honesty micro-link
**Where:** Infatuation's on-card scores done honestly; your no-fake-ratings brand.
**Why:** Directories cheat with invented star averages. The honest, *more* trustworthy move is a hard count in tabular figures with a tiny "how we rank" link right in the fold — proof of method, not a fake average.
```css
.hero__proof b{font-variant-numeric:tabular-nums lining-nums}
.hero__method{font-size:.75rem;color:var(--champagne);text-decoration:underline;text-underline-offset:3px}
```
**Impact:** H · **Effort:** Low (link already exists: /how-we-rank).

### 12. Reduced-motion & container-query safety net
**Where:** MDN/web.dev baseline 2026.
**Why:** Everything above is transform/opacity and degrades to a static, legible fold. Use a container query so the hero reflows on the *hero's* width, not the viewport — robust inside any layout the other agents build.
```css
@container hero (max-width:640px){ .hero__chips{gap:.4rem} .hero__h1{letter-spacing:-.01em} }
```
**Impact:** M · **Effort:** Low.

---

## What now reads dated (avoid)

- **Full-screen autoplay hero video / carousels.** Slow, distracting, penalized; Infatuation and Michelin both avoid them. (memorable.design flags <5MB muted-only; better to skip.)
- **Giant centered search box as the *entire* hero** (2015 Yelp/Airbnb clone) when your value is curation — feels like a database, not a guide.
- **Fake star averages / "4.8 ★ (imported)" rows.** Off-brand and increasingly distrusted. Use counts + method instead.
- **Multi-CTA button clusters.** One primary action; everything else is a text link. (memorable.design.)
- **Rainbow neon / glow everywhere.** Kills the one-neon premium effect. Exactly one glowing element per viewport.
- **Heavy drop-shadowed cards & big border-radii** in the fold — fights the hairline editorial system. Keep 2px radii, hairline rules.
- **Gradient-mesh blobs / glassmorphism** as decoration — 2021-era, reads generic now.
- **Parallax mouse-follow backgrounds** — motion-sickness risk, breaks reduced-motion intent, GPU cost for little payoff.

---

## Recommended for Boba Night (the 3–5 to actually apply)

1. **Identity+proof headline stack (#1 + #3 + #11):** letterspaced champagne eyebrow → Fraunces `clamp()` H1 promise → one hairline-framed honest stat line ("334 shops · every one visited · none paid") with a small "how we rank" link. This is the whole fold's spine and is nearly free.
2. **Browse-first chip row (#5):** 4–6 champagne-hairline chips routing to existing city / "open now" / late-night filters — sells the map, matches the curation value, out-converts a bare search for this brand. (Keep search in the nav.)
3. **The one neon CTA or live "Open now" dot (#7):** the single `#ff3f6f` glow in the viewport, honoring the one-neon rule; hover-glow gated by reduced-motion.
4. **Editorial dark surface: grain + vignette + hairline rules (#8 + #10):** gives the obsidian fold texture and structure with zero hero photo, on-brand with Monocle/Cereal restraint.
5. **Optional polish — masked H1 line reveal (#9)** on load only, fully reduced-motion-safe. Ship only if it stays subtle.

**One-line spec:** `[EYEBROW] · [Fraunces promise H1, clamp+balance] · [hairline honest-stat line + how-we-rank link] · [champagne chip row] · [one neon CTA/dot]` on a grained, vignetted obsidian surface — no photo, no carousel, no fake ratings.
