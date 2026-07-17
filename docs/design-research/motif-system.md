# The Boba Motif System

An original family of boba-ingredient marks for Boba Night, plus the behaviour
that brings them to life. Nine small SVGs drawn to one grid and one hairline
weight in the lacquer palette, a section divider drawn from the set, and a
click "surprise" that spills pearls. Ships as two files you drop in and forget:

- `css/motif.css` — palette, layout, and all motion (transform/opacity only)
- `js/motif.js` — self-initializing; injects the inline SVG and wires behaviour

No external asset requests. No animation library. No dependency on the sound
system (it uses it if present, stays silent if not).

## Vocabulary

The family is the boba cup, taken apart. Each mark is a single ingredient,
drawn as elegant line plus controlled fill, not clip-art:

| `data-motif` | Mark | Palette note |
|---|---|---|
| `pearl` | Tapioca sphere with a porcelain highlight | pearl + champagne stroke |
| `jelly` | Isometric lacquered cube, top facet lit | champagne translucency |
| `grass-jelly` | Near-black jade cubes stacked over a chawan | dark jade fill |
| `red-bean` | A cluster of azuki beans with gold seams | garnet |
| `taro` | The milk-tea swirl, aubergine and cream | aubergine (no neon purple) |
| `egg-tart` | Fluted shell, custard disc, one caramel spot | gold + one cinnabar spot |
| `foam` | A dome of milk-foam bubbles, two rising | pearl |
| `drizzle` | Three streams pouring into gold drops | champagne + gold |
| `matcha` | A chawan of whisked jade froth with a swirl | jade |

Design rules that hold the set together:
- One 44x44 grid, centred on (22,22). One hairline stroke weight (1.5,
  `vector-effect:non-scaling-stroke` so it stays crisp at any size).
- Roughly 90% obsidian / 7% champagne-gold / 3% cinnabar. Cinnabar appears
  exactly once, as the egg-tart caramel spot. Garnet carries the red bean so
  the one true accent stays rare.
- Taro is rendered in **aubergine**, a defined luxury token, never neon purple.
  The locked featured pill is the only purple on the site.
- Fills resolve from `luxury-homepage.css` / `nav-midnight.css` tokens when
  those load, with self-contained fallbacks so a mark renders on any page.

## Class API

Everything is drop-in markup. `motif.js` fills in the SVG on load.

**A single motif**
```html
<button class="boba-motif" data-motif="matcha" aria-label="Matcha"></button>
```
Any element works. On a non-button/link the script adds `role="button"` and
`tabindex="0"` and, if there's no text or label, an `aria-label` from the motif
name. Size with `--bm-size` (default 44px) or wrap it and set font-size:
```html
<span class="boba-motif" data-motif="pearl" style="--bm-size:64px"></span>
```

**A section divider drawn from the set**
```html
<div class="boba-divider"></div>
```
Renders as champagne hairlines flanking three tapioca pearls on a gold thread.
Marked `role="separator"`, decorative. Beads bob on hover.

**A surprise element**
```html
<button class="boba-surprise">Tap for pearls</button>
```
On click it sprays six pearls that fan upward and fade, then removes them.
Use it on a CTA, a card, a footer flourish. Your own content stays untouched.

**Behaviour**
- Hover / focus: the mark floats up gently (jelly wobbles, taro tips, drizzle
  drips, foam bubbles rise). 200ms, expo-out.
- Click / Enter / Space on a `.boba-motif`: a one-shot "surprise" — the pearl
  drops and bounces, the jelly wobbles, taro and matcha spin, foam bubbles
  rise, drizzle pours. The class clears after ~760ms so it re-fires next click.
- If `window.BobaSound` exists and is enabled, a surprise calls
  `BobaSound.pop()`. Absent or off, it stays silent. Never autoplay.

**Dynamic content**: after injecting markup at runtime, call
`window.BobaMotif.refresh()` to wire the new nodes. It is idempotent.

## Motion and performance

- Transform and opacity only. Nothing animates `fill`, `stroke`, or path `d`,
  so the compositor does the work and there are no repaints or layout thrash.
- Hover uses CSS transitions (120–240ms, expo-out). The surprise uses short
  one-shot keyframes. No infinite idle loops burning battery.
- The SVG is promoted once with `translateZ(0)`; `will-change:transform` sits
  only on the animated group.
- All motion is gated behind `@media (prefers-reduced-motion: no-preference)`.
  Under reduced motion the marks are fully static; a click still plays the
  sound (if enabled) but nothing moves, and the burst is skipped.
- Payload is tiny: nine inline SVGs of a few paths each, one stylesheet, one
  small script. No sprites to fetch, no fonts, no images.

## Accessibility

- The `.boba-motif` element is the focus target and carries the label; the SVG
  is `aria-hidden` and `focusable="false"`.
- Keyboard: Enter and Space fire the surprise. Focus-visible shows a champagne
  outline. The divider is a decorative `separator`.

## Sources studied (technique, not copies)

- Awwwards — SVG Animation and UI Animation / Microinteractions collections,
  for the resting-state calm plus one deliberate reveal on interaction.
  https://www.awwwards.com/inspiration/svg-animation
  https://www.awwwards.com/awwwards/collections/animation/
- SVG Animation Encyclopedia (svgai.org) — confirmation that only `transform`
  and `opacity` are compositor-accelerated, that animating `fill`/`stroke`/`d`
  forces CPU repaints, and the case for one-shot elastic/spring reveals over
  duration-tweened everything. Drove the transform-only rule here.
  https://www.svgai.org/blog/research/svg-animation-encyclopedia-complete-guide
- High-end tea and dessert brand marks (Behance luxury tea packaging, tea logo
  surveys) — for the line-plus-restrained-fill register and the discipline of a
  single accent, translated into the lacquer palette rather than borrowed.

Blended into an original set: nothing here is traced or copied. The marks are
drawn from the ingredients themselves, on Boba Night's own grid and palette.

## How a page author uses it

1. Load the two files (script deferred):
   ```html
   <link rel="stylesheet" href="/css/motif.css">
   <script src="/js/motif.js" defer></script>
   ```
2. Drop in `.boba-motif[data-motif=...]`, `.boba-divider`, or `.boba-surprise`.
   The script wires them on `DOMContentLoaded`.
3. Size with `--bm-size`. That's the whole surface.
