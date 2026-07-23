# Night-Market Charms — the bottom bar icon system

The mobile bottom bar is four custom SVG "charms" on a jeweler's tray: **Account** (a signet medallion on a chain stub), **Shops** (a paper lantern with a flame gem), **Map** (a folded night map with a four-point compass star), **Saved** (a faceted gem — saving a shop is pocketing a jewel). All four live in `components/nav.html` (and the homepage's baked header); styling in `css/nav-midnight.css`; behavior in `js/nav-midnight.js`. The four-column grid is now fully occupied, so the bar centers itself.

## The four states

**Idle.** Champagne stroke at 55% opacity, accent path (the gem/flame/star) dimmed. Quiet by design — the bar recedes until wanted.

**Hover (Apple Pencil).** On iPad Pro (M2 and later, iPadOS 16.4+), hovering the Pencil above a tab fires real `:hover` — the charm pre-lights: stroke warms to pale gold, a three-layer champagne glow blooms (`drop-shadow` stack, never `box-shadow` — it follows the icon's shape), and the icon lifts 2px. When the pointer is specifically a pen (`pointerover` with `pointerType === "pen"`), a small neon-pink dot pulses at the tab's corner — a wink only Pencil users ever see. Gated behind `@media (hover: hover)` so touch phones never get sticky hover states.

**Press.** The "haptic" read without haptics: the charm squashes to 88% width / 94% height in 50ms linear (instant, like contact), then releases over 400ms on an overshoot curve `cubic-bezier(.3,.7,.4,1.5)` (springs past rest, settles). The asymmetry — fast down, springy up — is what makes it feel physical. On Android, `navigator.vibrate(8)` adds a real tick; iOS ignores it harmlessly.

**Active page.** Set via `aria-current="page"` (semantics carry the state, not just color): the charm's accent path fills neon pink and pops in (`scale 0 → 1.2 → 1`), the label turns pale gold, and the **sliding pill** — one absolutely-positioned rounded indicator, moved only with `transform: translateX(0/100%/200%/300%)` — glides under the tab on a bouncy ease. Transform-only means zero layout shift and compositor-only animation.

## Behavior wiring (js/nav-midnight.js, "Night-Market Charms" module)

Active tab resolves from the path: `/account` → 0, `/directory` → 1, `/near-me` or `/nearby` → 2; Saved (`/#blackbook`) and the homepage show no pill. The module binds pen-hover classes, the vibrate tick, and the pill position; it retries briefly so it works on component pages where the nav injects after load.

## House rules

1. Never restyle `.bn-bb`, `.bn-bbpill`, `.ch`, `.st`, or `.acc` from page CSS — the bar is chrome, owned by `nav-midnight.css`.
2. Every icon is two layers: structure paths (`class="st"`) and ONE accent path (`class="acc"`). New tabs follow the same anatomy or the active-state animation won't apply.
3. The bar respects `env(safe-area-inset-bottom)` (padding, not offset, so the obsidian fills the iPhone home-indicator zone) and `prefers-reduced-motion` (all motion collapses to instant color changes).
4. Four tabs is the budget. A fifth means removing one, not shrinking five in.

## Technique credits

Press timing asymmetry: Josh Comeau's 3D button work. Sliding pill: Aaron Iker's CSS-only tab indicator. Safe-area handling: Samuel Kraft's Safari bottom-bar notes.
