# Boba Night — Front-Page Design Research

20 web-research agents scouted CSS/JS technique, boba and luxury-tea brand design, discovery UX, and component sources on 2026-07-20. Each lane below has a takeaway, concrete techniques with the library or CSS/JS approach, how it fits Boba Night, real sources, and specific ideas to steal.

## Award-winning site motion & layout

Award-winning dark-luxury and beverage sites (Awwwards' luxury and food/drink collections) earn their premium feel less from heavy WebGL and more from a small, disciplined kit: buttery smooth scroll, staggered reveal timing, split-text display headlines, one pinned "editorial" moment, and restrained micro-interactions with expensive easing. The current move is to push those reveals onto native CSS scroll-driven animations so they stay fast and jank-free on mobile. For Boba Night, the win is treating the shop list like a luxury magazine spread — slow, confident motion on a Fraunces headline and a single hero "cover story" — rather than a Yelp grid.

**Techniques**

- **Split-text display headline reveal** — The hero headline animates in line-by-line or word-by-word with a soft mask/rise, the single most repeated 'premium' signal across Awwwards type-led luxury winners. It makes a serif display feel authored and editorial rather than dropped in.
  - How: GSAP SplitText (or free SplitType) to wrap each line in an overflow-hidden clip, then GSAP timeline animating y:110%0 and opacity with a slow custom ease (e.g. expo.out / cubic-bezier(0.16,1,0.3,1)), ~0.9s, staggered 0.08s per line. Gate the whole thing behind @media (prefers-reduced-motion: no-preference).
  - Fit: Run it once on the Fraunces H1 (e.g. 'Boba, after dark') on load. Slow, confident line reveal in pearl on obsidian instantly reads luxury-magazine, not directory — and it's the cheapest high-impact upgrade to the front page.
- **Native CSS scroll-driven reveals** — Cards and sections fade + rise as they enter the viewport, but driven by the scroll position natively instead of a JS library. Winners increasingly use this because it runs off the main thread, so mobile scrolling stays glassy.
  - How: CSS animation-timeline: view() with animation-range: entry 0% cover 40%; on a keyframe that goes opacity 0/translateY(24px) 1/0. Zero JS. Wrap in @supports (animation-timeline: view()) and leave elements fully visible by default so unsupported browsers just show static content; disable under prefers-reduced-motion.
  - Fit: Use it for the staggered reveal of boba-shop cards down the SoCal list. You get the awards-site 'everything gracefully arrives' feel with no library weight — critical for a mobile-first, performant site with long, city-filtered result lists.
- **One pinned editorial 'cover story'** — A single sticky/pinned section where the copy scrolls while a featured image holds, or an image is revealed via an expanding clip-path. This is the 'magazine spread' beat that separates editorial winners from block-stacked templates.
  - How: CSS position: sticky for the pinned media column (cheap, no lib) OR GSAP ScrollTrigger pin:true for finer control; reveal the image with an animated clip-path: inset(...) or a mask wipe timed to scroll progress. Keep it to ONE such moment.
  - Fit: Make it the 'Featured tonight' hero for one standout shop — champagne/gold captions and jade accents over a held photo while the story text scrolls. Reserve the orchid accent strictly for this featured slot, matching your 'featured only' rule.
- **Buttery smooth scroll + expensive easing** — Award sites feel premium partly because the scroll itself is weighted and the motion uses slow, decelerating easing rather than snappy defaults. It reframes speed as calm confidence.
  - How: Lenis (lightweight, ~a few KB, the current winner default per Orpetron) for smooth scroll; standardize every transition on one luxe ease token (cubic-bezier(0.16,1,0.3,1)) and 400–900ms durations. Respect prefers-reduced-motion by skipping Lenis init. Note: test on iOS — some prefer to skip smooth-scroll on touch and keep native momentum.
  - Fit: Applied site-wide it ties the whole front page together into one 'after dark' mood. If you'd rather not ship a scroll lib on mobile, keep native momentum and just standardize the easing token — that alone lifts perceived quality.
- **Restrained micro-interactions on cards & CTAs** — Small, physical feedback — a card lifting slightly, a gold underline drawing in, a subtle image scale on hover/tap — is what makes luxury cards feel tactile without being loud.
  - How: CSS transitions on transform/opacity only (GPU-friendly): translateY(-4px) + a soft shadow on hover; an ::after gold underline that scales x 01 from left; image transform: scale(1.03) inside overflow:hidden. For richer spring feel use Framer Motion if React. Keep durations ~200–300ms.
  - Fit: Give each boba-shop card a quiet champagne underline draw and a 4px lift; on mobile use the tap/active state. This delivers the 'considered' Airbnb/Spotify-card feel and keeps the list from reading like a Yelp row.
- **Horizontal editorial rail** — A single horizontally-scrolling strip for a curated set, used by beverage winners like Done Drinks to encourage lateral browsing and break the vertical monotony.
  - How: Native CSS scroll-snap (overflow-x:auto; scroll-snap-type: x mandatory; each card scroll-snap-align:start) — no JS, thumb-friendly on mobile. Only reach for GSAP horizontal pinning on desktop if you want the scroll-to-scrub effect.
  - Fit: Use it for a curated 'Open late near you' or 'Tonight in Rowland Heights' rail near the top — snappy swipe on mobile, a tasteful lateral moment that echoes Done Drinks without copying its whole layout.

**Steal this**

- Done Drinks' formula: deep near-black base + exactly ONE saturated accent + GSAP motion — map directly onto obsidian + champagne gold, with orchid held back for featured only.
- Animate the Fraunces H1 line-by-line on load with an overflow-clip mask and expo.out easing — the single highest-ROI 'this is an award site' cue.
- Move card/section reveals to native CSS animation-timeline: view() so mobile scroll stays 60fps and you ship no scroll library.
- Budget motion to ONE pinned/cover-story moment on the front page; everything else is quiet reveals — restraint is what separates luxury winners from templates.
- Standardize every transition on one easing token cubic-bezier(0.16,1,0.3,1) and 400–900ms durations so the whole site moves like one object.
- Wrap all of it in @media (prefers-reduced-motion) and @supports fallbacks so the page is fully usable and fast with motion off — accessible-by-default, not bolted on.

**Sources**

- [Awwwards — Luxury Websites collection](https://www.awwwards.com/websites/luxury/) — Real, current roster of dark/editorial luxury SOTD winners (YLEM watches, Delvaux flagship, Depo Luxe, Pelizzari Studio) to study for restrained motion and type-driven layout.
- [Awwwards — Done Drinks (Honorable Mention)](https://www.awwwards.com/sites/done-drinks) — Real dark beverage brand (deep brown #3A1D17 + one accent, GSAP on Webflow, horizontal exploration) — a direct analog for a premium drink site that isn't a directory.
- [Award-Winning Animation Techniques for Websites — Bootcamp/Medium](https://medium.com/design-bootcamp/awwward-winning-animation-techniques-for-websites-cb7c6b5a86ff) — Breaks the winners' toolkit into 8 techniques with the exact libraries (GSAP ScrollTrigger, SplitText/SplitType, Lenis, Lottie/Rive) and prefers-reduced-motion notes.
- [10 Award-Winning Websites Perfecting Animation on Scroll — Orpetron](https://medium.com/orpetron/10-award-winning-websites-perfecting-animation-on-scroll-ec71a111789f) — Confirms the dominant stack across recent winners is GSAP + Lenis smooth scroll, useful for choosing a proven, tasteful setup over gimmicks.
- [Animate elements on scroll with Scroll-driven animations — Chrome for Developers](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) — Official guide to native CSS animation-timeline: view() reveals that run off the main thread — the performant, mobile-first way to get the reveal effect without shipping a scroll library.
- [Scroll-driven animations — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Reference for view-timeline/scroll-timeline syntax and progressive-enhancement fallbacks so the effect degrades gracefully where unsupported.

## Scroll-driven animation

In 2026 you no longer need a JS library for most tasteful scroll motion: native CSS animation-timeline with scroll() and view() covers reveal-on-scroll, reading-progress bars, and parallax with zero JS and GPU-accelerated performance, and it's supported in Chrome/Edge/Safari with a Firefox flag (~85% global). Reserve GSAP ScrollTrigger + Lenis for the one or two genuinely cinematic moments — a pinned hero-to-city transition — where scrubbed, orchestrated sequencing is worth the weight. For Boba Night the winning move is native CSS for the whole editorial reveal system, one restrained GSAP pinned section as the signature, and Lenis only if the smooth-scroll feel is on-brand and gated behind prefers-reduced-motion.

**Techniques**

- **Native reveal-on-scroll with animation-timeline: view()** — Cards fade/slide in as they cross into the viewport, driven purely by scroll position rather than a JS observer. Each element tracks its own progress, so staggering is automatic.
  - How: Pure CSS: @keyframes reveal{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}} then .card{animation:reveal linear both; animation-timeline:view(); animation-range:entry 0% cover 35%}. Wrap in @media (prefers-reduced-motion: no-preference). No library, GPU-accelerated (transform/opacity only).
  - Fit: Replaces the typical IntersectionObserver reveal on the venue grid and editorial blocks with zero JS — keeps the site fast and mobile-smooth. Use slow, short-range easing (cubic-bezier(.2,.7,.3,1)) so obsidian cards surface like a magazine page turning, never a bouncy Yelp list.
- **Scroll progress indicator with animation-timeline: scroll()** — A thin fixed bar that fills as the reader moves down the page — a reading-progress / 'night unfolding' cue.
  - How: Pure CSS: .progress{position:fixed;top:0;left:0;height:2px;transform-origin:left;animation:grow linear both;animation-timeline:scroll(root)} @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}. One element, no JS.
  - Fit: A 2px champagne/gold (#C5A46D) hairline against obsidian reads as a luxe editorial detail, not a utility bar. Reinforces the 'after dark, one long scroll' narrative and orients users on long city pages without adding weight.
- **Tasteful CSS parallax via view() ranges** — Background imagery drifts slower than foreground text as a section passes through the viewport, adding depth without a JS scroll loop.
  - How: Pure CSS: give a section's background layer animation-timeline:view() and animate transform:translateY over a small range (e.g. -6% to 6%) across animation-range: cover. Transform only. Gate behind prefers-reduced-motion.
  - Fit: On the hero and city-intro imagery (steam over a cup, neon signage), a 6–8% drift gives cinematic depth for the luxury 'after dark' feel while staying 60fps on phones. Small ranges avoid the vestibular-discomfort trap of heavy parallax.
- **One signature pinned section with GSAP ScrollTrigger (scrubbed)** — A single hero moment that pins in place while its children animate to scroll — e.g. a headline that dissolves into the featured-venue reveal, scrubbed 1:1 to the scrollbar.
  - How: GSAP + ScrollTrigger (now fully free): gsap.timeline({scrollTrigger:{trigger:'.hero',pin:true,scrub:1,start:'top top',end:'+=80%'}}). Animate nested children, not the pinned element; scrub:1 for smooth catch-up. Lazy-load GSAP only above a breakpoint / when reduced-motion is off.
  - Fit: Gives Boba Night ONE Spotify/Airbnb-grade cinematic beat — the orchid (#b46bd6) featured venue emerging from the fold — without turning the whole site into a scroll-jacked demo. Reserving GSAP for a single moment keeps the bundle off every other page.
- **Staggered grid reveals with ScrollTrigger.batch()** — When several venue cards enter together, they animate in a coordinated wave (batched) instead of firing independently, avoiding janky overlapping triggers.
  - How: ScrollTrigger.batch('.venue-card',{onEnter:b=>gsap.to(b,{opacity:1,y:0,stagger:0.08,overwrite:true}),start:'top 85%'}). Set initial state with gsap.set. Only needed if you want tighter choreography than native view() gives.
  - Fit: For the 'boba places near you' grid, a batched 80ms stagger feels curated and editorial rather than a data dump — but only reach for this if native CSS staggering isn't controlled enough; otherwise prefer the zero-JS view() version.
- **Lenis smooth scroll — optional, brand-dependent** — Momentum/inertia smoothing on the scroll itself so the whole page glides. Pairs with GSAP so scrubbed animations stay in sync.
  - How: const lenis=new Lenis({lerp:0.1}); lenis.on('scroll',ScrollTrigger.update); gsap.ticker.add(t=>lenis.raf(t*1000)); gsap.ticker.lagSmoothing(0). Disable on touch (syncTouch unstable on iOS<16) and skip entirely when prefers-reduced-motion is set.
  - Fit: Can add a 'quiet luxury' glide that suits the brand — but it overrides native scroll, can feel laggy on low-end Android, and hurts accessibility if forced. Only adopt if the featured/hero experience clearly benefits; keep lerp gentle (~0.1) and always provide a hard opt-out.

**Steal this**

- Build the entire reveal system in native CSS (animation-timeline: view()) and drop IntersectionObserver — faster, less JS, ships in Chrome/Edge/Safari; Firefox degrades to instantly-visible content.
- Author reveals with 'both' fill wrapped in @media (prefers-reduced-motion: no-preference) so reduced-motion users get the final state instantly — accessibility built in, not bolted on.
- Use a 2px champagne-gold scroll() progress hairline as a signed editorial detail instead of a generic loading bar; keep parallax displacement tiny (6–8%, transform-only) for depth without motion sickness.
- Spend GSAP + pinning on exactly ONE cinematic moment (headline dissolving into the orchid featured venue) and lazy-load the library only there so the rest of the site stays light.
- Treat Lenis as opt-in luxury, not default: gate behind non-touch + no-reduced-motion, keep lerp ~0.1, because forced smooth-scroll is the fastest way to make a premium site feel broken on cheap Androids.
- Watch Chrome 145's animation-trigger / timeline-trigger — declarative scroll-TRIGGERED (play-once) reveals that will replace even the view() reveal pattern for entrance animations.

**Sources**

- [Scroll-Driven Animations — Josh W. Comeau](https://www.joshwcomeau.com/animation/scroll-driven-animations/) — Deep, accurate walkthrough of animation-timeline, view()/scroll(), animation-range (entry/exit/contain/cover), timeline-scope for linked timelines, and the prefers-reduced-motion gating pattern with exact CSS.
- [CSS scroll-triggered animations are coming — Chrome for Developers](https://developer.chrome.com/blog/scroll-triggered-animations) — Documents the new animation-trigger / timeline-trigger longhands landing in Chrome 145 (Dec 2025) — declarative scroll-triggered (not just scroll-driven) reveals that replace IntersectionObserver.
- [ScrollTrigger — GSAP Docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) — Authoritative reference for pinning, scrub, toggleActions, ScrollTrigger.batch() for staggered reveals, and parallax; confirms all GSAP plugins are now free.
- [Lenis — darkroom.engineering (GitHub)](https://github.com/darkroomengineering/lenis) — Install/init, the exact GSAP ScrollTrigger sync snippet, lerp/duration options, and mobile syncTouch caveats for smooth scroll.
- [CSS scroll-driven animations — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Canonical spec reference for scroll() vs view() timelines and animation-range values to verify syntax and support.

## Cutting-edge CSS features

The strongest 2025 wins for Boba Night are native, JS-free, and progressively enhanced: cross-document View Transitions turn the boba-card shop-profile jump into a shared-element hero animation, scroll-driven animations reveal cards on scroll without an IntersectionObserver library, and :has()/container queries/color-mix() let cards restyle by their own content and context. All degrade gracefully and gate behind prefers-reduced-motion, so they stay fast, tasteful, and accessible on mobile. Everything below is buildable with plain CSS plus one @view-transition line — no Framer Motion, no GSAP.

**Techniques**

- **Cross-document View Transitions (shared-element card shop profile)** — Native browser API that animates between two DOM states — including across full page navigations in an MPA — by matching elements that share a view-transition-name and morphing one into the other. Level 2 (cross-document) ships in Chrome/Edge 126+ and Safari 18.2+; unsupported browsers just hard-cut, so it's safe progressive enhancement.
  - How: Add @view-transition { navigation: auto; } once. On each boba card's thumbnail set view-transition-name: shop-<id> (unique per shop), and on the shop profile's hero image set the SAME name — the browser morphs the card image into the hero. Customize timing with ::view-transition-old(root)/::view-transition-new(root) keyframes. Wrap all of it in @media (prefers-reduced-motion: no-preference). Clear the name after transition so only one element ever holds a given name. No JS library needed; for in-page filtering use document.startViewTransition(() => updateDOM()).
  - Fit: This is the single biggest 'luxury magazine, not Yelp' upgrade: tapping a boba card on the SoCal discovery grid makes its photo glide and expand into the shop's profile hero, like Airbnb/Spotify detail transitions. It gives spatial continuity between the finder feed and profile pages you already generate, at zero JS weight, staying smooth on mobile.
- **Scroll-driven reveal + progress (animation-timeline: view() / scroll())** — Declarative animations tied to scroll position (scroll()) or an element's visibility within the viewport (view()) — the browser runs them off the main thread, so no IntersectionObserver or scroll-listener JS. Chrome/Edge full support; Safari via polyfill/newer builds; guard with @supports.
  - How: For cards fading/rising in as they enter: .card { animation: rise linear both; animation-timeline: view(); animation-range: entry 0% entry 40%; } with @keyframes rise { from { opacity:0; transform: translateY(24px) } to { opacity:1; transform:none } }. For an 'after dark' reading progress hairline on long profile pages: a fixed 2px champagne bar with animation-timeline: scroll(root block) scaling scaleX 01. Gate both behind @media (prefers-reduced-motion: no-preference) and @supports (animation-timeline: view()).
  - Fit: Replaces any AOS/GSAP scroll library with pure CSS, keeping the mobile bundle tiny and fast. A restrained champagne-gold rise-in on the discovery cards and a thin gold scroll bar on profiles reinforce the editorial, dark-luxury feel without the janky, gimmicky scroll effects that would cheapen the brand.
- **:has() content- and state-aware cards** — The parent/relational selector: style an element based on what it contains or the state of a descendant. Baseline across all modern browsers in 2025. Eliminates the JS that used to add wrapper classes.
  - How: .card:has(.badge--featured) { outline:1px solid var(--orchid); } to light up only featured shops in orchid #b46bd6. .card:has(.badge--open-late) { --accent: var(--jade); }. Section-level: .grid:has(.card:hover) .card:not(:hover){ opacity:.6 } to dim siblings on hover (spotlight effect). Nav: body:has(.filter-drawer[open]) { overflow:hidden } to lock scroll when a filter opens — no JS. Wrap experimental bits in @supports (selector(:has(*))).
  - Fit: Lets the finder grid react to its own data: a shop flagged featured in Supabase renders its orchid treatment purely from markup, open-late shops pick up jade accents, and hovering one card gently dims the rest for that curated, spotlighted gallery feel — all without shipping state-management JS to the phone.
- **Container queries (@container) for one card that fits everywhere** — Style a component based on the width of its container rather than the viewport, so the same boba-card markup adapts whether it's in a 4-up desktop grid, a 2-up tablet grid, a full-width 'featured' slot, or a horizontal scroll rail. Baseline 2023+, fully safe in 2025.
  - How: On the card wrapper: .card { container-type: inline-size; container-name: card; }. Then @container card (min-width: 320px) { .card__meta { display:flex; } .card__title { font-size: clamp(1.1rem, 4cqi, 1.6rem); } } — note cqi units scale type to the container. Optionally style-query the featured token: @container style(--featured: true) { ... }.
  - Fit: You render cards in several layouts (city grids, 'Open Late' rails, Date Night hub, featured hero). One container-query-driven card component means a single source of truth that looks intentional in every slot — critical for a magazine-grade layout system and far less brittle than viewport media queries as you add SoCal city pages.
- **color-mix() in OKLCH for a live palette** — Blend two colors at author time in a perceptually-uniform space (oklch), generating tints, shades, hover states, and translucent overlays from your five brand tokens without hand-picking hex values. Baseline across modern browsers in 2025.
  - How: Define --gold: #C5A46D etc., then derive: --gold-soft: color-mix(in oklch, var(--gold), var(--obsidian) 70%); for hover on dark; --scrim: color-mix(in srgb, var(--obsidian) 60%, transparent) for image overlays; button hover: background: color-mix(in oklch, var(--gold), white 12%). Great for state layers: :hover { background: color-mix(in oklch, currentColor 8%, transparent); }.
  - Fit: Keeps the obsidian/pearl/champagne/jade/orchid system tight and consistent: every hover, focus ring, and photo scrim is mathematically derived from the five brand tokens, so the whole site reads as one deliberate palette instead of a pile of one-off hex codes — exactly the discipline a luxury brand needs, and it makes dark-mode overlays over boba photography effortless.
- **Editorial polish: text-wrap balance/pretty, @property gradients, tasteful backdrop-filter** — Three small, high-taste primitives. text-wrap: balance evens out heading line lengths; text-wrap: pretty prevents orphans in body copy. @property registers a custom property with a type so gradients/values can actually animate. backdrop-filter: blur() creates frosted glass over imagery. All baseline or near-baseline in 2025.
  - How: h1,h2,.hero-title,.card__title { text-wrap: balance; } and .prose p,.card__desc { text-wrap: pretty; }. For an animatable gold sheen on a featured badge: @property --angle { syntax:'<angle>'; inherits:false; initial-value:0deg; } then animate --angle in a conic-gradient border. Frosted sticky nav / filter bar over hero photos: position:sticky; background: color-mix(in srgb, var(--obsidian) 55%, transparent); backdrop-filter: blur(12px) saturate(1.2); (always keep a solid @supports-not fallback for contrast).
  - Fit: These are the details that separate 'editorial' from 'template': balanced Fraunces headlines that never leave one lonely word, clean descriptions under each shop, a frosted obsidian nav floating over full-bleed boba photography, and a subtle animated gold edge on featured (orchid) shops. High polish, near-zero performance cost, and each one degrades to plain text/solid color.

**Steal this**

- Give every boba card thumbnail a unique view-transition-name (shop-<id>) and reuse the exact same name on the profile hero image, so tapping a card morphs the photo into the profile hero across the page load — the flagship Airbnb/Spotify-grade moment, from one @view-transition line.
- Replace any scroll-animation library with animation-timeline: view() on cards (entry 0%40% rise+fade) and a fixed scaleX champagne bar on animation-timeline: scroll() for profile reading progress — all behind prefers-reduced-motion + @supports.
- Drive featured/open-late styling from data with :has(): .card:has(.badge--featured) gets the orchid #b46bd6 treatment and .card:has(.badge--open-late) picks up jade — no JS class toggling.
- Make the boba card a single container-query component (container-type: inline-size, type sized in cqi) so it looks intentional in city grids, Open-Late rails, and featured hero slots alike.
- Derive every hover, focus ring, and photo scrim from the 5 brand tokens with color-mix(in oklch, …) instead of hand-coding hex — one coherent obsidian/champagne/jade/orchid system.
- Ship the editorial finish: text-wrap: balance on Fraunces headings, text-wrap: pretty on descriptions, and a backdrop-filter: blur() frosted obsidian nav/filter bar floating over full-bleed boba photography (with a solid-color @supports fallback).

**Sources**

- [A beginner-friendly guide to view transitions in CSS — MDN Blog](https://developer.mozilla.org/en-US/blog/view-transitions-beginner-guide/) — Shows the one-line @view-transition { navigation: auto } opt-in for multi-page apps plus ::view-transition-old/new customization and browser-support baseline (Chrome/Edge 126+, Safari 18.2+).
- [Some practical examples of view transitions to elevate your UI — Piccalilli](https://piccalil.li/blog/some-practical-examples-of-view-transitions-to-elevate-your-ui/) — Concrete gallery-to-detail shared-element pattern using matching view-transition-name on the same image across pages, plus view-transition-name: match-element for lists and the guidance to scope names tightly.
- [An Introduction To CSS Scroll-Driven Animations — Smashing Magazine](https://www.smashingmagazine.com/2024/12/introduction-css-scroll-driven-animations/) — Exact CSS for animation-timeline: view() reveal-on-scroll and scroll() progress bars, entry/exit keyframe ranges, and the @supports + prefers-reduced-motion guard pattern.
- [CSS scroll-driven animations — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Reference for scroll-timeline vs view-timeline and animation-range, confirming these are pure-CSS declarative animations tied to scroll position/visibility.
- [2026 CSS Features You Must Know (Shipped Late 2025–Now) — Riad Kilani](https://blog.riadkilani.com/2026-css-features-you-must-know/) — Real syntax for color-mix(in oklch, var(--brand), white 65%) token blending, text-wrap: balance/pretty, and :has() behind @supports feature queries.
- [View Transition API — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) — Authoritative reference for same-document document.startViewTransition() and the ::view-transition-group/old/new pseudo-element tree used to scope shared-element animations.

## Interactive card patterns

The strongest, most on-brand interactive card patterns for Boba Night are pointer-tracking spotlight/glow (a single radial-gradient masked layer whose center is driven by CSS custom properties), a grid-wide "one glow follows the pointer across all cards" variant, subtle 3D tilt with a champagne glare sweep, and magnetic CTAs. All are GPU-cheap (transform/opacity only), sub-9KB or fully vanilla, and easy to gate behind prefers-reduced-motion and pointer:fine so mobile stays flat and fast. Skip heavy flip cards on the main grid; the glow-and-tilt combo reads far more "luxury magazine" than "Yelp directory."

**Techniques**

- **Pointer-tracking spotlight glow (CSS mask + custom props)** — A soft champagne/gold light pool follows the cursor across a card. A duplicate/overlay layer is revealed only inside a radial-gradient mask whose center is the live pointer position; nothing animates on the main layer so it's essentially free.
  - How: Vanilla CSS+JS. On the card set -webkit-mask/mask: radial-gradient(20rem 20rem at var(--x) var(--y), #000 1%, transparent 50%) on an inset:0 pointer-events:none overlay; a pointermove handler computes x=e.clientX-rect.left and sets el.style.setProperty('--x'/'--y') plus --opacity:1. Gate behind @media (hover:hover) and (pointer:fine). No library.
  - Fit: Turns each shop card into an 'after dark' spotlight against obsidian #0B0C0E — the gold pool grazing a drink photo feels like a magazine light rig, not a directory row. Use champagne #C5A46D at low opacity for standard cards, orchid #b46bd6 only on the Featured card.
- **Grid-wide glow that flows between cards** — A single luminous edge/border light tracks the pointer as it moves across the whole card grid, lighting each card's border as you pass — the marquee 'premium SaaS' effect (Linear/Vercel style).
  - How: One mousemove listener on the parent grid; for each card compute cardX = -(cardRect.left-parentRect.left)+x and set --mouse-x/--mouse-y. Cards use a blurred radial pseudo-element translated by those vars, behind a 1px padded 'fake border' that reveals a gradient. Pure CSS+JS (Cruip pattern), works without Tailwind.
  - Fit: Makes the SoCal boba grid feel like one cohesive editorial spread that responds as a whole. A thin gold hairline that ignites along card edges as you scan reinforces the luxury-magazine feel and visually ties the obsidian layout together.
- **Subtle 3D tilt with a gold glare sweep** — Cards tilt a few degrees toward the cursor with a light glare sheen crossing the surface — depth and tactility without cartoonish rotation.
  - How: vanilla-tilt.js (8.5KB, zero deps): add data-tilt or VanillaTilt.init(el,{max:6, speed:400, glare:true, 'max-glare':0.15, scale:1.02, gyroscope:false}). Keep max low (~6°) for taste; disable on touch and under prefers-reduced-motion.
  - Fit: A restrained ~6° tilt plus a faint champagne glare on the drink photo gives shop cards a glossy, physical, premium feel (think a lacquered menu). Tie the glare tint to #C5A46D so the sheen reads as gold, not a generic white shine.
- **Magnetic primary CTA** — The main action button (e.g. 'Find boba near me') gently pulls toward the cursor as you approach and springs back on exit — a signature high-end micro-interaction reserved for one hero element.
  - How: GSAP quickTo (or ~15 lines vanilla): on mousemove within the button compute x=clientX-(left+width/2), y=clientY-(top+height/2), apply translate at ~0.3 strength; on mouseleave gsap.to(...,{x:0,y:0, ease:'elastic.out(1,0.3)'}). Restrict to pointer:fine.
  - Fit: Gives the location/finder CTA a bespoke, expensive feel that guides the eye to the site's core action (find the closest SoCal boba). Use once, on the gold pill button, so it stays special rather than gimmicky.
- **Expandable / detail-reveal card (progressive disclosure)** — Card grows or slides open in place to reveal hours, distance, and a 'get directions' action instead of jumping to a new page — keeps browsing flow intact.
  - How: CSS grid-template-rows: 0fr 1fr transition (or a height clip) toggled by a real <button aria-expanded>; animate transform/opacity of the inner content. Pure CSS+JS, no library; respect prefers-reduced-motion by cross-fading instead of sliding.
  - Fit: Lets a user peek a shop's open-late hours and proximity without leaving the editorial grid — fast, mobile-friendly, and keeps the 'browse the night' narrative unbroken. Pairs naturally with the Supabase city/distance data already in the project.
- **Accessible flip card (detail views only)** — A card flips to a back face (e.g. quick stats or a signature-drink note). Powerful but heavier and easy to get wrong for a11y — reserve for one-off detail cards, not the scanning grid.
  - How: transform: rotateY(180deg) on a preserve-3d inner wrapper toggled by a real <button> (not hover), with focus management and aria-live/aria-expanded per the Vispero pattern; disable the rotate under prefers-reduced-motion and cross-fade instead.
  - Fit: Optional flourish for a 'Featured tonight' hero card where the back reveals a tasting note in Fraunces — but keep it off the main grid to preserve speed and the calm, scannable layout.

**Steal this**

- Drive a radial-gradient mask center with --x/--y custom props set on pointermove — a whole spotlight with zero animated layout and no library.
- Attach ONE mousemove listener to the grid and compute per-card offsets so a single gold glow flows across every card (Linear/Vercel look) instead of independent per-card glows.
- Use the 1px-padding 'fake border' trick: a padded wrapper whose gradient reveals only a hairline, so the glow lights card EDGES in champagne gold.
- Keep vanilla-tilt max at ~6° with max-glare 0.15 and tint the glare gold — restraint is what separates 'luxury' from 'gimmick'.
- Reserve the magnetic pull for exactly one element (the finder CTA) using GSAP quickTo + elastic.out reset, so it feels bespoke, not busy.
- Gate every motion effect behind @media (hover:hover) and (pointer:fine) plus prefers-reduced-motion — mobile stays flat, fast, and battery-friendly while desktop gets the theatrics.

**Sources**

- [Build a Glowing Hover Effect that Follows the Pointer — Frontend Masters Blog](https://frontendmasters.com/blog/glowing-hover-effect/) — Exact CSS mask + --x/--y custom-property technique for a pointer-tracking spotlight, using a masked overlay layer and pointermove.
- [How to Create a Spotlight Card Hover Effect with Tailwind CSS — Cruip](https://cruip.com/how-to-create-a-spotlight-card-hover-effect-with-tailwind-css/) — Full pattern for ONE glow that tracks the pointer across a whole grid of cards by setting per-card --mouse-x/--mouse-y from a single parent listener, plus a 1px fake-border reveal.
- [Vanilla-tilt.js (official demo/docs)](https://micku7zu.github.io/vanilla-tilt.js/) — Dependency-free 8.5KB tilt library with data-tilt init and built-in glare (max-glare, glare-prerender) — the exact source for the tilt + champagne-glare technique.
- [2 Ways to Make Magnetic Buttons (GSAP / Framer Motion) — Olivier Larose](https://blog.olivierlarose.com/tutorials/magnetic-button) — Concrete magnetic-CTA math (displacement from element center, quickTo, elastic ease, reset to 0,0 on leave) for the primary 'Find boba near me' button.
- [prefers-reduced-motion — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) — Canonical reference for gating tilt/flip/magnetic motion so the site stays accessible and calm for reduced-motion users.
- [Creating a truly accessible Flip Card — Vispero](https://vispero.com/resources/creating-a-truly-accessible-flip-card/) — How to build a keyboard- and screen-reader-safe flip card (real button, focus, aria) if flip is used on detail cards rather than the main grid.

## WebGL / canvas hero effects

The tasteful, fast path for a dark luxury hero is a slow-drifting WebGL mesh/noise gradient rendered on a single fullscreen quad — not a heavy 3D scene. A ~10kb Stripe-style "whatamesh" shader or a layered-simplex-noise fragment shader on OGL (29kb, tree-shakes smaller) gives Boba Night a living obsidian-to-jade-to-champagne haze at 60fps on mobile, as long as you cap DPR, lazy-load on view, and ship a static poster under prefers-reduced-motion. Reserve heavier r3f-based ShaderGradient only if you want a sphere/orb centerpiece.

**Techniques**

- **Whatamesh single-file mesh gradient** — A ~10kb WebGL fragment-shader that renders a slow, silky animated mesh gradient on one canvas, colors set via CSS custom properties (--gradient-color-1..4). This is the exact tech behind Stripe's and Luma's hero backgrounds.
  - How: Drop jordienr's Gradient.js gist into the project, add <canvas id="gradient-canvas">, then new Gradient().initGradient('#gradient-canvas') in a useEffect/onMount. Set the four --gradient-color CSS vars.
  - Fit: Feed it obsidian #0B0C0E as the base with jade #123F35 and champagne #C5A46D as the two accent stops (skip a 4th, or use a whisper of orchid #b46bd6 only on featured pages). Keep it behind the Fraunces headline at very low speed so it reads like light moving through dark glass — 'after dark' luxury, near-zero build cost.
- **Layered-simplex-noise flowing gradient on OGL** — A custom fullscreen fragment shader that sums 3-4 simplex-noise octaves (1.0x/1.3x/1.86x/3.25x wavelengths) and maps the resulting lightness into a JS-rendered gradient texture, with time flowing on the noise z-axis and a tiny horizontal drift (~0.04) so it never looks like a scroll loop.
  - How: OGL (29kb, tree-shakes smaller) driving one Triangle/Plane + Program; pull the noise fn from stegu/webgl-noise; pass colors as a sampler2D gradient texture. Branchless SDF blur via smoothstep, no neighbor sampling = single-pass and cheap.
  - Fit: Gives full art-direction control the whatamesh preset can't: you can bias the palette so 80% of the frame stays near-obsidian and only a slow champagne/jade bloom drifts through — the restrained, editorial-magazine feel the brand wants, while staying lighter than any three.js option.
- **ShaderGradient r3f component (orb/plane centerpiece)** — A configurable React component rendering a 3D moving gradient as a plane, sphere, or water surface with 40+ props (colors, camera, lighting, speed).
  - How: npm i @shadergradient/react @react-three/fiber three three-stdlib camera-controls; <ShaderGradientCanvas pixelDensity={1} lazyLoad rootMargin> wrapping <ShaderGradient type='sphere' .../>. Match React 19 + R3F v9 on Next 15 App Router.
  - Fit: Only if you want a hero *object* — e.g. a slowly rotating champagne-and-jade gradient sphere echoing a boba pearl, as the focal element beside the wordmark. Heavier (drags in three + r3f), so gate it behind lazyLoad and reserve for desktop; use technique 1 or 2 as the mobile fallback.
- **2D-canvas rising 'pearl' particles** — A lightweight plain-Canvas2D loop (no WebGL) drifting a few dozen soft, blurred dark circles slowly upward with gentle parallax — evoking boba pearls settling/rising in tea.
  - How: ~60 lines of requestAnimationFrame Canvas2D; cap particle count to ~30-40, use radial-gradient fills in champagne/pearl at 4-8% opacity over the obsidian. No library needed.
  - Fit: A quieter, thematically literal alternative or overlay on top of the gradient — adds brand-specific storytelling (boba, not generic SaaS gradient) while staying trivially cheap on low-end phones. Layer it above technique 1 at very low opacity for depth.
- **DPR cap + IntersectionObserver lazy start** — Performance discipline that makes any of the above safe on mobile: clamp devicePixelRatio to ~1.5-2, only start the render loop when the hero is in view, and pause it when scrolled offscreen.
  - How: renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); wrap init in an IntersectionObserver (or ShaderGradient's lazyLoad/threshold/rootMargin props) and cancelAnimationFrame when out of view.
  - Fit: Keeps the luxury effect from tanking Lighthouse/LCP on the phones most SoCal users browse on — the difference between 'premium' and 'janky and hot battery.' Non-negotiable given the mobile-first, performant brief.
- **prefers-reduced-motion static-poster fallback** — Render one high-quality still frame of the gradient (or a baked PNG/WebP) and show it instead of the live shader when the user requests reduced motion or on very weak hardware.
  - How: @media (prefers-reduced-motion: reduce) { hide canvas, show the poster img }; in JS, check window.matchMedia('(prefers-reduced-motion: reduce)').matches before booting the loop. Export the poster from a single paused render.
  - Fit: Satisfies the accessibility requirement and doubles as the instant LCP image so the hero looks finished before WebGL initializes — the effect becomes a progressive enhancement, never a blocker, which is how a luxury brand should treat motion.

**Steal this**

- Use whatamesh/Gradient.js with obsidian as base and only jade + champagne as accent stops — restraint is what separates luxury from a rainbow SaaS gradient.
- Bias the noise so ~80% of the frame stays near-obsidian; let only a slow champagne/jade bloom drift through, plus a ~0.04 horizontal time drift so it never looks like a repeating scroll loop.
- Always cap devicePixelRatio to ~2 and pause the render loop via IntersectionObserver when the hero scrolls offscreen.
- Ship a baked poster frame as the LCP image and gate the live shader behind prefers-reduced-motion + in-view — motion as progressive enhancement.
- Reserve orchid #b46bd6 in the gradient exclusively for featured/date-night hero variants, keeping the default palette obsidian-jade-champagne.
- Consider a Canvas2D rising-pearl particle layer at 4-8% opacity over the gradient for brand-specific storytelling instead of a generic mesh.

**Sources**

- [A flowing WebGL gradient, deconstructed — Alex Harri](https://alexharri.com/blog/webgl-gradients) — Full teardown of a subtle flowing gradient: stacked 2D/3D simplex noise, gradient-texture color mapping, branchless SDF blur, and slow time offsets so motion reads organic not mechanical — exactly the 'tasteful, not gimmicky' bar.
- [whatamesh / Gradient.js (Stripe mesh gradient) — jordienr gist](https://gist.github.com/jordienr/64bcf75f8b08641f205bd6a1a0d4ce1d) — The ~10kb single-file WebGL mesh gradient Stripe/Luma use; init on a canvas id and drive colors with CSS custom properties. Lowest-effort, lowest-weight way to get a premium moving gradient.
- [oframe/ogl — Minimal WebGL library](https://github.com/oframe/ogl) — 29kb minzipped (8kb core), zero deps, tree-shakeable — the right engine for a custom fullscreen fragment-shader hero when you want control without three.js weight.
- [ruucm/shadergradient — 3D moving gradients for React](https://github.com/ruucm/shadergradient) — Drop-in @shadergradient/react component (plane/sphere/water) with pixelDensity + lazyLoad/threshold props; documents the r3f+three dependency cost so you can decide when a heavier orb is worth it.
- [React Gradient Mesh Shaders — shadcn.io](https://www.shadcn.io/shaders/gradient-mesh) — Copy-paste React mesh-gradient shader block useful as a reference implementation and for comparing config surface (colors, speed, geometry).
- [prefers-reduced-motion — MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) — Canonical reference for gating the animation and swapping in a static poster frame — required for the 'accessible' constraint.

## Micro-interactions & spring physics

Spring physics (stiffness/damping/mass) beats fixed-duration easing because it feels physical and is interruption-safe — a re-tap mid-animation redirects instead of restarting, which matters for save/favorite and toggle on a mobile discovery feed. The tasteful move for Boba Night is a small, consistent motion vocabulary: snappy scale-pop on press (Motion One or a shared cubic-bezier), a spring-driven heart save, and a @property count-up for stats — all gated behind prefers-reduced-motion. No confetti, no bounce-heavy gimmicks; just weighted, sub-250ms feedback that reads luxe.

**Techniques**

- **Spring press-feedback on buttons & cards (the house motion)** — On pointer/tap-down, scale to ~0.97 and lift a hair; on release, a spring settles it back with slight overshoot. Physical, weighted, sub-200ms. Interruption-safe: a fast double-tap redirects instead of stuttering.
  - How: Motion One (2.5kb): animate(el,{scale:0.97},{type:'spring',stiffness:400,damping:28,mass:0.8}). Non-JS fallback: transition:transform 180ms cubic-bezier(.34,1.56,.64,1) with :active{scale:.97}. In React use whileTap={{scale:0.97}} transition={{type:'spring',stiffness:400,damping:28}}.
  - Fit: Apply one shared spring token to every tappable surface — spot cards in the feed, the city/area pills, the 'Open Late' toggle. Consistent weight across the whole front page is what separates luxury from Yelp. Keep champagne #C5A46D as the pressed-state ring so feedback stays on-brand, not blue.
- **Spring save / favorite (heart) toggle** — Tapping save pops the icon: quick scale up past 1 then springs to rest as it fills, with the outline morphing to a solid champagne/gold fill. No confetti — the overshoot alone reads as delight.
  - How: Motion One keyframe: animate(icon,{scale:[1,1.3,1]},{type:'spring',stiffness:500,damping:15}) and swap fill to #C5A46D. Or Framer whileTap + an AnimatePresence swap of outline/solid SVG paths. CSS-only fallback: @keyframes pop with cubic-bezier(.34,1.56,.64,1).
  - Fit: 'Save a spot for boba night' is the core repeat action. A gold heart that springs to fill turns a utilitarian bookmark into the site's signature moment — restrained enough for the obsidian/pearl palette, memorable enough to reinforce the after-dark, curated feel.
- **@property count-up for stats** — Animate an integer CSS variable from 0 to its value; the DOM text interpolates with no per-frame JS. Use for a hero/section stat like number of open-late spots or cities covered.
  - How: @property --n{syntax:'<integer>';initial-value:0;inherits:false} then transition:--n 1.2s cubic-bezier(.16,1,.3,1); element uses counter-reset:n var(--n) and ::after{content:counter(n)}. Trigger the value change when the section enters view via a one-line IntersectionObserver adding a class. JS fallback (requestAnimationFrame tween) for Safari, which lacks @property number animation.
  - Fit: A single tasteful count-up ('247 spots open past midnight') in Fraunces gives the front page an editorial-magazine data moment without a chart. Near-zero JS keeps it fast on mobile, matching the performance bar.
- **Magnetic / cursor-follow primary CTA (desktop only)** — The main CTA subtly leans toward the cursor within a small radius and springs back on exit — a premium, physical hover cue. Disabled on touch so it never misfires on mobile.
  - How: Track pointer delta within the button's bounds, translate by delta*0.2 via a spring. Motion One: use a springValue/animate on translateX/Y; Kinetics ships a copy-paste 'Magnetic button'. Wrap in @media(hover:hover) and pointer:fine so touch devices get a plain press.
  - Fit: Reserve this for the single hero CTA (e.g. 'Find boba near me'). One magnetic element per page reads as quiet luxury (Airbnb/Linear-tier); more would be gimmicky. Keeps the orchid #b46bd6 strictly for featured, so the CTA stays champagne.
- **Spring segmented toggle for 'Open Late' / mode switch** — A pill-shaped segmented control whose active-state thumb slides between options on a spring instead of snapping, with the selected label crossfading. Interruption-safe when tapped rapidly.
  - How: Animate the thumb's translateX with a spring (Motion One animate or FLIP via getBoundingClientRect). Kinetics 'Toggle pills' / 'choice chips' give ready CSS. CSS-only: transition:transform 220ms cubic-bezier(.34,1.4,.64,1) on an absolutely-positioned thumb.
  - Fit: The core 'only doing SoCal / open late now' filtering wants a switch that feels deliberate. A gliding champagne thumb on obsidian is the kind of controlled motion that signals a curated product, not a database filter row.
- **prefers-reduced-motion gating layer** — A single motion guard so every spring, pop, count-up and magnet degrades to an instant, non-animated state change for users who opt out or are on low-power devices.
  - How: const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches — branch to duration:0 / no spring. In CSS wrap decorative motion in @media(prefers-reduced-motion:no-preference){...}. Motion respects it if you check the query before animate().
  - Fit: Non-negotiable for the 'tasteful, accessible' bar. It lets Boba Night ship all the spring delight above while guaranteeing the front page stays fully usable and calm for anyone who needs stillness — the difference between polished and reckless.

**Steal this**

- Define ONE spring token (stiffness:400, damping:28, mass:0.8) and reuse it on every tappable surface — cards, pills, toggle, save. Cross-page consistency is the luxury signal.
- Make the save/favorite heart the signature moment: scale [1,1.3,1] spring pop + outline-to-solid champagne #C5A46D fill. No confetti.
- Ship one @property count-up stat in Fraunces ('X spots open past midnight') triggered by IntersectionObserver — editorial data moment, near-zero JS.
- Limit the magnetic cursor-follow effect to the single hero CTA and wrap it in @media(hover:hover) so touch never misfires.
- Give the 'Open Late'/SoCal filter a spring-sliding segmented thumb in champagne on obsidian instead of a snapping radio row.
- Wrap all decorative motion in prefers-reduced-motion and keep every interaction sub-250ms, transform/opacity-only, so it stays fast and accessible on mobile.

**Sources**

- [Spring step-by-step tutorial — Motion.dev](https://motion.dev/tutorials/js-spring) — Official Motion One (2.5kb) spring API: animate() with type:'spring' and stiffness/damping/mass, or the duration+bounce shorthand. Exact params for tuning snappy vs settled motion.
- [Kinetics — Spring-physics motion for web interfaces](https://kinetics.colorion.co/) — 117 copy-paste spring micro-interactions (magnetic button, toggle pills, star rating, choice chips, ripple, count-up) shipped as pure CSS cubic-bezier approximations AND React. Directly maps to Boba Night's chip/save/toggle needs and explains interruption-safety.
- [Animating Number Counters — CSS-Tricks](https://css-tricks.com/animating-number-counters/) — The modern @property + counter-reset technique to animate an integer with zero JS. Exact syntax for a count-up on stats like number of open-late spots.
- [Save Button Micro-Interaction in Framer — Framer University](https://framer.university/resources/save-button-micro-interaction-in-framer) — Concrete pattern for a spring-based save/favorite toggle with fill + scale-pop, the exact interaction Boba Night's save-a-spot action needs.
- [React gesture animations | hover, drag, press — Motion for React](https://www.framer.com/motion/gestures/) — whileTap/whileHover with a spring transition — the canonical accessible press-feedback pattern for buttons and cards if the stack uses React.
- [Detecting prefers-reduced-motion in JavaScript — css-animation.com](https://www.css-animation.com/accessible-motion-architecture/prefers-reduced-motion-architecture/detecting-prefers-reduced-motion-in-javascript/) — matchMedia('(prefers-reduced-motion: reduce)') gate so every spring/count-up degrades to an instant state change — required for the accessible, tasteful bar.

## Cursor effects & magnetic buttons

A small dose of cursor/magnetic interaction is exactly the kind of "editorial luxury" texture that separates Boba Night from a Yelp directory, but only on fine-pointer devices — every credible source gates these behind !isTouchDevice && !prefersReducedMotion. The highest-ROI moves for a dark champagne-on-obsidian site are a single mix-blend-mode: difference cursor ring (which auto-inverts to gold/pearl over any photo) and magnetic pull on the hero CTA and featured cards, both cheap to build with GSAP quickTo() or a few lines of vanilla JS.

**Techniques**

- **Mix-blend-mode difference cursor ring** — A single ~40-50px fixed-position circle (border only or filled) that follows the pointer with mix-blend-mode: difference, so it auto-inverts against whatever it's over — reads gold over dark, dark over pearl, and pops beautifully over boba photography without ever clashing.
  - How: One div, position:fixed, pointer-events:none, mix-blend-mode:difference, background/border in a near-white so it inverts. Update with transform: translate3d(x,y,0) on mousemove (use transform, NOT top/left, to stay on the compositor and avoid the double-buffering lag CSS-Tricks flags). Optional GSAP quickTo for a slight lag/smoothing. Idle scale(.3), scale(1) over links/cards.
  - Fit: This is the single most on-brand effect: a difference-blend ring turns the whole dark page into a live surface and makes the champagne #C5A46D and pearl feel expensive. It signals 'magazine, not directory' with ~30 lines and no image assets.
- **Magnetic hero CTA + featured cards** — The primary 'Find boba near me' button and the orchid-accented featured shop cards subtly lean toward the cursor as it approaches, then spring back on exit — a physical, tactile pull that rewards intent.
  - How: On mousemove within the element compute x=clientX-(left+w/2), y=clientY-(top+h/2), then gsap.quickTo(el,'x',{ease:'elastic.out(1,0.3)'}) (and y); on mouseleave gsap.to(el,{x:0,y:0,duration:1}). Vanilla alt: translate a fraction (~0.2-0.35) of the offset in a rAF loop. Keep strength low (0.25) for tasteful, not cartoonish.
  - Fit: Draws the eye and thumb to the one action that matters (proximity search) and to featured shops — reinforcing the orchid 'featured only' hierarchy. Feels like Airbnb/Spotify polish, adds zero clutter.
- **Cursor label / word-swap on hover targets** — The cursor ring expands and reveals a tiny word ('Open now', 'View', 'Map') when over a shop card or CTA, replacing a generic tooltip with editorial microcopy inside the cursor itself.
  - How: Add a text span inside the cursor div; toggle a --active class on mouseenter of [data-cursor] elements that scales the ring to ~72-90px and fades the label in. Pull the label from a data-cursor-label attribute. Fraunces for the word to stay on-brand.
  - Fit: Communicates 'open late / near you' status with brand voice at the exact moment of intent, keeping the UI clean — no persistent badges needed. Very Spotify-hover-card energy.
- **SVG url() cursor as the tasteful fallback** — Instead of a JS follower everywhere, ship a lightweight custom cursor via CSS cursor: url() using a small gold-dot or boba-pearl SVG with a correct hotspot — near-zero cost, no reduced-motion concerns.
  - How: cursor: url("data:image/svg+xml;base64,...") 16 16, auto; where 16 16 centers the hotspot on a 32px glyph. Use as the baseline, and layer the JS blend cursor only on capable devices.
  - Fit: Gives a branded pointer even on lower-powered devices or when motion is reduced, so the luxury detail degrades gracefully instead of vanishing to the OS arrow.
- **Accessibility + mobile gate (mandatory wrapper)** — All follower/magnetic effects must be feature-gated: never render on touch/coarse pointers (they have no hover and it just lags), and honor prefers-reduced-motion.
  - How: const ok = window.matchMedia('(hover:hover) and (pointer:fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches; only then init cursor/magnetic JS. Keep cursor:none scoped to the same condition so mobile keeps the native cursor. Set the follower aria-hidden and pointer-events:none.
  - Fit: Boba Night is mobile-first — most traffic is phones where these effects are pure jank. Gating keeps mobile fast and clean while desktop gets the flourish, which is exactly the 'tasteful, performant' bar the brand sets.

**Steal this**

- Use mix-blend-mode: difference on ONE cursor circle so it auto-inverts to gold/pearl over dark UI and over boba photos — no per-state color logic needed.
- Drive position with transform: translate3d, not top/left — CSS-Tricks and the CodePen both confirm top/left causes visible double-buffering lag.
- Magnetic math is universal: offset = cursor - element-center, animate a fraction of it, reset to 0,0 on leave. Keep strength ~0.25 and use elastic.out(1,0.3) for the luxe spring.
- Gate everything behind matchMedia('(hover:hover) and (pointer:fine)') AND prefers-reduced-motion — this is the consensus across CSS-Tricks, dbushell, and Motion docs.
- GSAP quickTo() is the performant modern way to smooth a follower (vs recreating tweens each mousemove); Motion+ Cursor is the turnkey paid alternative if we don't want to hand-roll.
- Put editorial microcopy ('Open now', 'View map') INSIDE the expanding cursor instead of tooltips to keep the dark layout uncluttered.

**Sources**

- [Magnetic Button — 2 Ways (GSAP + Framer Motion), Olivier Larose](https://blog.olivierlarose.com/tutorials/magnetic-button) — Cleanest reference for the magnetic math: offset = cursor - element center, animate with GSAP quickTo elastic.out or a Framer spring (stiffness 150/damping 15), reset to 0 on mouse leave.
- [Custom cursor with mix-blend-mode (CodePen, Lomzo)](https://codepen.io/Lomzo/pen/qBBROLm) — Working blend-mode difference cursor: fixed white circle, pointer-events none, scale(.3) idle -> scale(1) over links, positioned via GSAP. Exact pattern to invert against dark obsidian + photos.
- [Next Level CSS Styling for Cursors — CSS-Tricks](https://css-tricks.com/next-level-css-styling-for-cursors/) — Covers url() SVG cursors with hotspot coords, the cursor:none + pointer-events:none div technique, and the explicit accessibility gate (skip if touch or reduced-motion). Notes JS followers cause double-buffering lag.
- [Motion (Framer) Cursor component docs](https://motion.dev/docs/cursor) — Prebuilt state-aware cursor that snaps magnetically to interactive elements and can be disabled for reduced-motion — a paid motion-plus option if we want it turnkey rather than hand-rolled.
- [Magnetic Button Effect with GSAP (CodePen, Course-Max-One)](https://codepen.io/Course-Max-One/pen/QwyjPOg) — Minimal standalone GSAP magnetic button demo to copy directly for the hero CTA.

## Kinetic & variable typography

Fraunces is a variable serif with weight, optical-size (opsz), SOFT and WONK axes, which makes it ideal for the tasteful kinetic-type moves trending now: scroll-linked weight/optical-size shifts, masked split-text reveals, gradient-clipped headlines, and a slow single-line marquee. The current best practice is CSS-native where possible (scroll-driven animations, background-clip:text) and GSAP SplitText only where a JS reveal earns its weight, always gated behind prefers-reduced-motion and kept off the critical render path for mobile. Every technique below is a small, GPU-cheap or native-optimized effect that reads as luxury/editorial rather than gimmick.

**Techniques**

- **Scroll-linked optical-size / weight on the hero headline** — As the visitor scrolls the hero, the Fraunces display headline continuously interpolates its variable axes (e.g. wght 340680 and opsz toward 144) so the type visibly 'thickens and sharpens' — a slow, native, JS-free move.
  - How: CSS scroll-driven animations: view-timeline-name on the hero section, animation-timeline on the h1, @keyframes animating font-variation-settings: 'opsz' and 'wght'. Critical: use overflow:clip (not hidden) on any clipping ancestor or the timeline breaks. Gate with @media(prefers-reduced-motion:reduce){animation:none}. Note per Val Head that font-variation-settings isn't GPU-accelerated, so keep it to ONE headline and short axis ranges.
  - Fit: Turns the 'after dark' hero into a living masthead — Fraunces at high opsz gets the thin, high-contrast serifs of a luxury magazine cover, reinforcing the editorial-not-Yelp feel without any image weight.
- **Masked split-text reveal on section headers** — Headlines wipe up line-by-line from behind an invisible mask on entry — the single most 'editorial magazine' motion, used for section titles like the finder and date-night hub.
  - How: GSAP SplitText (free since 3.13) with type:'lines', mask:'lines', then gsap.from(split.lines,{yPercent:110,stagger:0.08,duration:0.9,ease:'power4.out'}) triggered by ScrollTrigger once. SplitText auto-adds aria-label on the parent and aria-hidden on the fragments, so screen readers still read the intact headline. Wrap the tween in a matchMedia that disables it under reduced motion and just shows the text.
  - Fit: Gives each section a considered 'reveal' cadence like a print title sequence, elevating perceived quality; the built-in aria handling keeps it accessible, matching the tasteful/accessible brand bar.
- **Champagne/gold gradient-clipped headline** — A static but rich treatment: the hero or featured-shop headline is painted with a subtle gold gradient (champagne #C5A46D into pearl), optionally with a slow sheen sweep — luxury without motion cost.
  - How: background: linear-gradient(#C5A46D, #E4D3A8); background-clip:text; -webkit-background-clip:text; color:transparent. For the optional sheen, animate background-position of a wider gradient (GPU-cheap, transform/opacity-class), still disabled under reduced motion. Reference CodyHouse text-gradients.
  - Fit: Directly renders the champagne/gold brand accent as the headline's own material against obsidian #0B0C0E — instantly reads 'luxury after dark' and differentiates from flat-white directory type.
- **Single-line editorial marquee ribbon (neighborhood names)** — One slow horizontal ribbon of SoCal locations — 'Rowland Heights · Cypress · Sawtelle · Irvine · Koreatown' — drifting under the hero, done as a tasteful kinetic detail, not a spammy ticker.
  - How: Ryan Mulligan's technique: two identical .marquee__content tracks in a flex container, the second aria-hidden='true'; @keyframes translateX(0) calc(-100% - var(--gap)); animation-play-state:paused on hover. Wrap in @media(prefers-reduced-motion:reduce) to drop the animation and show a static row. Set the loop to ~40s for a calm luxury pace.
  - Fit: Reinforces the SoCal-proximity core of the project (Rowland Heights/Cypress) as ambient motion, and the slow champagne-on-obsidian ribbon feels like a magazine strapline rather than a Yelp category bar.
- **Variable-weight hover on shop/finder cards** — On card hover/focus the shop name animates its Fraunces weight up (and slightly tightens tracking), a micro-interaction that signals interactivity with type instead of borders or shadows.
  - How: CSS transition on font-variation-settings ('wght' 380 620) plus letter-spacing, triggered on :hover and :focus-visible. Keep the range small since the property repaints; only the hovered card animates so cost is negligible. Provide a non-motion fallback (color/underline) under reduced motion.
  - Fit: Lets the finder cards feel premium and tactile using only the typeface — no Yelp-style chrome — keeping the dark editorial surface clean while still giving clear affordance on the 'find nearest boba' cards.
- **WONK/SOFT accent for the orchid 'Featured' label only** — Reserve Fraunces' playful WONK (wonky serifs) and SOFT axes for the orchid-highlighted Featured items — a subtle static or one-shot axis flourish that marks 'special' without a different font.
  - How: Set font-variation-settings 'WONK' 1,'SOFT' 40 on .featured headings (orchid #b46bd6), or animate SOFT once on reveal via a short transition. Purely opt-in per element, so no global perf hit.
  - Fit: Uses the variable font itself to encode the featured tier in the brand's orchid color, giving the 'featured only' accent a distinct personality while staying within one type system — cohesive and unmistakably intentional.

**Steal this**

- Use overflow:clip instead of overflow:hidden anywhere near a scroll-driven headline — hidden silently creates a scroll container and kills the animation-timeline (Carmen Ansió's documented gotcha).
- GSAP SplitText is now free in 3.13+ and auto-manages aria-label/aria-hidden, so you get magazine-grade line reveals without breaking screen readers — no custom accessibility plumbing needed.
- font-variation-settings is NOT hardware-accelerated and causes repaints (Val Head), so limit animated variable type to one hero headline and per-card hover, never a whole page of moving weights.
- For the marquee, translate by calc(-100% - var(--gap)) not just -100% so the gap doesn't cause a visible jump at loop restart, and mark the duplicated track aria-hidden='true'.
- Wrap every kinetic effect in @media(prefers-reduced-motion:reduce) that reduces to the static end-state — for Boba Night that means the gradient headline and ribbon still look finished, just still.
- Exploit Fraunces' four axes as a design system: opsz for the scroll hero, wght for hover, WONK/SOFT reserved strictly for orchid featured items — one font doing the work of a whole type family.

**Sources**

- [Scroll-Driven Variable Fonts — Carmen Ansió](https://www.carmenansio.com/articles/variable-font-scroll) — Exact CSS for driving font-variation-settings from scroll position with view-timeline; documents the overflow:clip gotcha and browser support.
- [SplitText | GSAP Docs](https://gsap.com/docs/v3/Plugins/SplitText/) — Official docs for the now-free SplitText: char/word/line splitting, built-in mask option for reveals, and automatic aria-label/aria-hidden so screen readers still read the whole headline.
- [The Infinite Marquee — Ryan Mulligan](https://ryanmulligan.dev/blog/css-marquee/) — Modern accessible marquee: duplicate the track, aria-hidden the copy, translateX by calc(-100% - gap) for seamless loop, disable under reduced motion.
- [Animating variable fonts with CSS — Val Head](https://valhead.com/2020/11/15/animating-variable-fonts/) — Confirms font-variation-settings is animatable per-axis and warns it isn't hardware-accelerated (repaints) — the key performance caveat for using it sparingly.
- [Text Gradients in CSS — CodyHouse](https://codyhouse.co/nuggets/text-gradients) — Reference for background-clip:text + transparent text gradient technique used for the champagne/gold headline treatment.
- [Kinetic Typography 2026: Examples + GSAP Code — Studio Meyer](https://studiomeyer.io/en/blog/kinetische-typografie) — Current-year survey of tasteful kinetic type patterns and GSAP recipes, confirming split-reveal and scroll-linked type as the 2025-26 editorial direction.

## Quiet-luxury / editorial web design

The quiet-luxury look is mostly restraint plus two or three tactile details done well: a barely-there film grain over the obsidian, type that scales fluidly so the Fraunces hero reads like a magazine cover on a phone, and disciplined whitespace with gold used only as a hairline accent. Modern CSS now does the heavy lifting natively — SVG feTurbulence grain, clamp() fluid type, and animation-timeline: view() scroll reveals need zero JS libraries, which keeps it fast and mobile-friendly. The biggest upgrade for Boba Night is treating imagery editorially (duotone/monochrome that blooms to color on interaction) so the front page feels curated, never like a Yelp grid.

**Techniques**

- **Barely-there film grain over obsidian** — A fixed, full-viewport noise layer generated from an SVG feTurbulence (fractalNoise) filter — the analog-film/paper texture that separates luxury dark sites from flat #000 SaaS backgrounds.
  - How: Inline the SVG as a data-URI background-image on a body::after pseudo-element (see ibelick), set position:fixed; inset:0; pointer-events:none; z-index:9999. Use baseFrequency ~0.75, numOctaves 3, opacity 0.04–0.07, mix-blend-mode:soft-light so grain rides on top of #0B0C0E without muddying it. No extra HTTP request; ~1KB. CSS-Tricks' contrast(170%) brightness() trick lets you dial grain intensity.
  - Fit: Gives the obsidian background a tactile, low-light 'after dark' film quality instead of dead black, reinforcing the luxury-magazine mood on every page for essentially zero performance cost.
- **Fluid clamp() type scale for Fraunces** — Display headings and body that scale continuously with viewport width instead of jumping at breakpoints, so the Fraunces hero reads as a proper editorial cover on a 390px phone and doesn't blow out on desktop.
  - How: Use Utopia's calculator to generate CSS custom properties, e.g. --step-6: clamp(2.75rem, 2rem + 3.75vw, 5.5rem) for the hero, --step-0: clamp(1rem,0.95rem+0.25vw,1.125rem) for Inter body. Pair with Fraunces as a variable font and set font-optical-sizing:auto (Fraunces has an opsz axis) plus tight letter-spacing:-0.02em on display, generous line-height:1.6 on body.
  - Fit: Mobile-first is the whole point of Boba Night — this makes the front-page headline feel intentionally typeset at any size, the single biggest 'magazine not directory' signal, with no JS.
- **JS-free scroll-driven reveals** — Sections and boba cards fade-and-rise as they enter the viewport, using native CSS scroll timelines instead of an IntersectionObserver library like AOS or GSAP ScrollTrigger.
  - How: @keyframes rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}} then on the element: animation:rise linear both; animation-timeline:view(); animation-range: entry 0% cover 40%. Wrap in @media (prefers-reduced-motion: no-preference). Provide a no-timeline fallback (elements simply visible) for older browsers.
  - Fit: Adds the calm, choreographed reveal of a hospitality site to Boba Night's card grid while shipping zero animation JS — keeps the mobile bundle tiny and honors reduced-motion, staying tasteful not gimmicky.
- **Editorial duotone imagery with color-on-interaction** — Boba/venue photos rendered in a restrained obsidian-and-champagne monochrome by default, blooming to full color on hover/tap — the trick fashion and gallery sites use to make a photo grid feel curated rather than Yelp-crowded.
  - How: Layer background-blend-mode or a ::after with mix-blend-mode:color over the image, or filter: grayscale(1) contrast(1.05) sepia(0.15) for a warm gold cast; transition filter 400ms ease; on :hover/:focus-within remove to filter:none. Keep real alt text and don't hide info behind the effect.
  - Fit: Unifies mismatched venue photography under the brand palette so the front page looks art-directed; the reveal-to-color moment rewards interaction and makes browsing feel like flipping a magazine.
- **Restraint grid: wide margins + hairline gold rules** — An asymmetric editorial layout with large negative space and 1px champagne dividers at low opacity instead of boxes/borders/cards-with-shadows — the structural discipline that reads as 'quiet luxury'.
  - How: CSS Grid with a max content measure (~66ch for text), fluid gutters via Utopia space tokens, and section separators as border-top:1px solid color-mix(in srgb, #C5A46D 22%, transparent). Avoid drop shadows; use spacing and a single hairline to imply hierarchy. Reserve orchid #b46bd6 strictly for a 'Featured' tag.
  - Fit: Directly counters the Yelp-directory feel: generous whitespace and thin gold rules make the SoCal-boba listings feel like a considered editorial spread, and the palette discipline keeps gold/orchid as rare accents.
- **Variable-font micro-typography for headlines** — Exploiting Fraunces' variable axes (opsz optical size, SOFT, WONK) so large display type gets high-contrast, slightly quirky editorial character while small UI text stays legible.
  - How: Load Fraunces variable from Google Fonts with the axes you need; set font-variation-settings:'opsz' 144,'SOFT' 0,'WONK' 1 on the hero and 'opsz' 20 on labels. Combine with text-wrap:balance on headings for even ragged lines and font-feature-settings:'liga','dlig' for tasteful ligatures.
  - Fit: Gives the Boba Night wordmark and hero a distinctive luxury-magazine masthead feel from one font file, keeping payload low while looking bespoke rather than default-Google-Fonts.

**Steal this**

- Ship one 1KB inline-SVG feTurbulence grain layer as body::after at opacity ~0.05, mix-blend soft-light — instant analog-film mood over #0B0C0E on every page.
- Set the hero headline to clamp(2.75rem,2rem+3.75vw,5.5rem) with Fraunces opsz auto and -0.02em tracking so it reads like a cover on a 390px phone.
- Replace any scroll-animation library with native animation-timeline:view() + animation-range: entry 0% cover 40%, wrapped in prefers-reduced-motion — zero JS reveals.
- Render venue photos filter:grayscale(1) sepia(0.15) by default and transition to full color on :hover/:focus-within so the grid looks art-directed, not Yelp.
- Use dividers of border-top:1px color-mix(in srgb,#C5A46D 22%,transparent) instead of card boxes/shadows, and lock orchid #b46bd6 to a single 'Featured' pill.
- Cap body measure at ~66ch with Inter at line-height 1.6 and text-wrap:balance on all Fraunces headings for clean ragged-right editorial lines.

**Sources**

- [Grainy Gradients — CSS-Tricks](https://css-tricks.com/grainy-gradients/) — Canonical breakdown of the SVG feTurbulence noise technique with the contrast/brightness filter trick and mix-blend overlay for dark surfaces.
- [Creating grainy backgrounds with CSS — ibelick](https://ibelick.com/blog/create-grainy-backgrounds-with-css) — Gives the exact inline data-URI SVG so grain ships with zero extra network requests — key for a performant mobile hero.
- [Fluid Responsive Design — Utopia](https://utopia.fyi/) — The fluid type/space methodology and clamp() calculator behind smoothly scaling Fraunces display type across phone-to-desktop.
- [A guide to Scroll-driven Animations with just CSS — WebKit](https://webkit.org/blog/17101/a-guide-to-scroll-driven-animations-with-just-css/) — Exact animation-timeline: view() + animation-range code and the prefers-reduced-motion guard for JS-free, accessible reveals.
- [Designing And Building With Fluid Type And Space Scales — Smashing Magazine](https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/) — Deep implementation of the Utopia custom-property pattern for a consistent editorial type-and-spacing system.
- [Hotel & Restaurant Design websites — Awwwards](https://www.awwwards.com/websites/hotel-restaurant/) — Live reference gallery for hospitality/editorial layout, spacing restraint, and serif-led type direction to benchmark against.

## Bento grids & modern section layouts

The modern bento grid is a 12-column CSS Grid with grid-auto-flow: dense, tiles that span different column/row counts to encode editorial hierarchy, and a single consistent gap + corner radius that holds it together. The difference between "curated" and "cluttered" is restraint (6-12 tiles, one clear hero tile, generous negative space) plus responsiveness that collapses cleanly to 1-2 columns on mobile. For Boba Night this means one obsidian canvas where a champagne-framed featured venue anchors a rhythm of smaller cards, so a dense homepage reads like a magazine spread instead of a Yelp list.

**Techniques**

- **12-column grid with grid-auto-flow: dense** — A single grid (repeat(12, minmax(0,1fr))) where each tile declares grid-column: span N / grid-row: span N. The 'dense' keyword backfills gaps with smaller tiles so odd spans never leave holes, without reordering the DOM.
  - How: Pure CSS: display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); grid-auto-flow:dense; gap:clamp(12px,1.5vw,20px). Hero venue = span 6/span 4; secondary = span 3; chips = span 2. No JS, no library.
  - Fit: Lets one featured (orchid-framed) venue tile physically dominate the fold while cities, 'open late', and date-night tiles fill in around it — a curated composition, not a uniform card grid. dense keeps the obsidian canvas gap-free even with mixed tile sizes.
- **Content-height mobile, equal-height desktop** — On mobile the grid rows size to content (natural stacking); only at wide viewports do you switch on grid-auto-rows:1fr to force the tidy equal-height mosaic. This is why Apple/Linear bentos look crisp on desktop but never crush text on phones.
  - How: CSS: default grid-template-columns:repeat(2,1fr) with rows auto; at @media(min-width:1024px) go to 12 columns + grid-auto-rows:1fr. Reset each tile's span to 1/1 at the mobile breakpoint so everything linearizes.
  - Fit: Mobile-first requirement met without hacks: on a phone Boba Night becomes a clean single/two-column feed; on desktop it snaps into the editorial mosaic. Prevents the #1 bento failure mode of squished tiles on small screens.
- **Container queries for per-tile layout** — Each tile is a query container so its INTERNAL layout (image-left vs image-top, title size) responds to the tile's own width, not the viewport. A wide hero tile shows a horizontal split; the same component in a narrow slot stacks — one component, many sizes.
  - How: CSS: .tile{container-type:inline-size} then @container (min-width:17.5rem){.tile__body{flex-direction:row}}. Zero JS. Supported in all evergreen browsers.
  - Fit: Reuse ONE venue-card component across every tile size (hero, half, quarter) instead of authoring variants. A wide featured tile gets a photo-beside-text editorial layout; the same card in a small slot goes photo-on-top — keeps the system DRY and consistent.
- **Intrinsic responsive tiles (auto-fit + minmax)** — For secondary rails (e.g. 'more neighborhoods'), repeat(auto-fit, minmax(min(100%,220px),1fr)) reflows the number of columns automatically as width changes — no breakpoints at all.
  - How: CSS one-liner: grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr)). The min(100%,…) guard prevents overflow on very narrow phones.
  - Fit: City/neighborhood chip rails auto-pack to the viewport so a SoCal-only, city-dense homepage stays tidy from iPhone SE to desktop with almost no media-query maintenance — fast and low-CSS.
- **Restraint system: hero + rhythm + one accent** — The curated look is a rule set, not decoration: cap the visible grid at ~6-12 tiles, give exactly ONE tile clear dominance, keep a single gap value and a single corner radius (12-20px) across every tile, and let negative space breathe. Extra items go behind a 'view all'.
  - How: Design tokens: --gap, --radius, --tile-pad as CSS custom properties applied to every .tile; enforce a max tile count in the template loop. Reserve the orchid (#b46bd6) accent border/glow for a single featured tile only.
  - Fit: This is what separates Boba Night from a Yelp directory: obsidian background + pearl text + champagne hairline borders on all tiles, orchid reserved for the one featured venue. Uniform radius/gap makes density read as an intentional magazine layout, not a dump of results.
- **Tasteful tile hover / lift interactions** — Subtle, GPU-cheap hover states — a slight scale/translate, a champagne border brighten, or a photo zoom under overflow:hidden — signal interactivity without gimmicks and respect reduced-motion.
  - How: CSS: transition:transform .3s ease, box-shadow .3s; :hover{transform:translateY(-2px)}; wrap with @media(prefers-reduced-motion:reduce){transition:none}. Image zoom via .tile img{transition:transform .4s} + .tile:hover img{transform:scale(1.04)} inside overflow:hidden.
  - Fit: Adds the Spotify/Airbnb tactile polish on venue tiles — photo gently zooms, champagne border warms — while staying fast (transform/opacity only) and accessible via reduced-motion, matching the tasteful 'after dark' luxury tone.

**Steal this**

- Make ONE tile the hero — the current featured/nearest boba venue — at grid-column:span 6/grid-row:span 4 with the orchid #b46bd6 accent reserved exclusively for it; everything else stays champagne-hairlined so the eye lands where you want.
- Use grid-auto-flow:dense on a 12-col grid so mixed tile sizes (venue photo, 'open late' pill, city list, map teaser) pack with no gaps on the obsidian canvas — no manual placement.
- Ship content-height rows on mobile and switch grid-auto-rows:1fr on only above 1024px, resetting spans to 1 at the mobile breakpoint, so the phone view is a clean vertical feed and desktop is the tight mosaic.
- Wrap each venue card in container-type:inline-size and write ONE component that flips photo-beside-text (wide tiles) to photo-on-top (small tiles) via @container — reuse everywhere instead of building variants.
- Enforce a design-token discipline: one --gap (clamp 12-20px), one --radius (16px), applied to every tile, and cap the homepage at ~8-10 visible tiles with a 'view all' for overflow — density stays editorial, not cluttered.
- Add a photo-zoom-on-hover inside overflow:hidden plus a translateY(-2px) lift using only transform/box-shadow transitions, gated behind prefers-reduced-motion, for Airbnb-grade polish that stays performant and accessible.

**Sources**

- [Bento grid layout with CSS grid and container queries — iamsteve](https://iamsteve.me/blog/bento-layout-css-grid) — Best real code: 12-col grid + grid-auto-flow: dense, rows sized to content on mobile and grid-auto-rows: 1fr only above 1280px, plus @container queries for per-tile internal layout — the exact responsive-reflow pattern Boba Night needs.
- [Building a Bento Grid Layout with Modern CSS Grid — WeAreDevelopers](https://www.wearedevelopers.com/en/magazine/682/building-a-bento-grid-layout-with-modern-css-grid-682) — Compares two spanning strategies (auto-placement with dense vs explicit grid-line positioning via nth-child) so you can lock the hero tile's position while letting the rest flow.
- [Bento Grid CSS Tutorial: Apple-Style Layout — Senorit](https://senorit.de/en/blog/bento-grid-design-trend-2025) — Concrete Apple-style principles: hierarchy through tile size, consistent 12-24px gaps and radii, and a hard 6-12 block limit to avoid clutter — directly maps to the luxury-magazine feel.
- [Look Ma, No Media Queries! Responsive Layouts Using CSS Grid — CSS-Tricks](https://css-tricks.com/look-ma-no-media-queries-responsive-layouts-using-css-grid/) — Canonical reference for auto-fit/minmax intrinsic responsiveness so the grid reflows fluidly without a stack of breakpoints — fewer media queries, faster mobile.

## Boba / bubble tea brand sites

The strongest boba brands don't win on drink icons or Yelp-style lists — they win on art-directed real photography (Gong Cha), tactile "bubble" texture and curved organic geometry (Machi Machi), and Hermès-of-boba heritage storytelling with restrained type (Xing Fu Tang, Nayuki). Boba Night should steal the editorial/luxury craft cues, not the bright commercial candy palettes. The single biggest upgrade: treat drinks as photographed subjects on obsidian, add grain/plaster texture so the dark background reads as luxury not emptiness, and lean on a bilingual serif wordmark for cultural authority.

**Techniques**

- **Photograph the drink, don't icon it** — Gong Cha's system deliberately replaced graphic drink icons with real, art-directed product photography for authenticity across kiosks and web. The drink is the hero subject, shot with intent.
  - How: Serve art-directed cutout/on-obsidian drink shots as the primary hero and card imagery. Use responsive <img srcset> (or next/image) with fixed aspect-ratio boxes (aspect-ratio: 4/5), object-fit: cover, and LQIP blur-up (a tiny base64 placeholder that fades to sharp) so cards never reflow. Lazy-load below-the-fold with loading="lazy" and decoding="async".
  - Fit: On #0B0C0E, a single well-lit boba glass with condensation and a champagne rim-light reads instantly as luxury magazine, not directory. Makes each SoCal shop's featured drink the emotional hook of the front page.
- **Bubble-effervescence texture + Venetian-plaster grain** — Machi Machi's premium feel comes from Venetian plaster wall finishes that 'mimic the effervescence of bubbles' — tactile texture instead of flat color. Flat dark backgrounds read cheap; textured dark reads expensive.
  - How: Overlay a subtle SVG grain using feTurbulence (type='fractalNoise', baseFrequency ~0.8) at 3-5% opacity fixed over the obsidian bg, plus a couple of very-low-opacity radial-gradient 'bubble' glows in champagne/jade. Keep it a single inline SVG or one 2KB PNG tiled via background-image; no JS. It's static so it's motion-safe.
  - Fit: Kills the dead-flat black that makes dark sites feel like an unstyled template. Gives Boba Night the tactile, after-dark depth of a printed cover without hurting performance.
- **Editorial heritage-craft narrative blocks** — Xing Fu Tang ('the Hermès of bubble tea') and Nayuki build luxury through story: ancestral craft, founder values, a 'mental shelter' lifestyle mood — restrained type, generous whitespace, content in distinct blocks rather than a grid of listings.
  - How: Build a scroll of full-bleed editorial sections (one idea per viewport) using CSS scroll-driven animation (animation-timeline: view()) or a tiny IntersectionObserver to fade/rise elements in at 12% opacity->1. Set Fraunces at a large optical size for display headers, Inter for body, and a max line-length of ~66ch for any prose.
  - Fit: Turns the front page into a curated 'tonight in SoCal' magazine spread — a featured neighborhood, a signature drink, a shop story — instead of a scrollable list. This is the exact Spotify/Airbnb/luxury-magazine feel the brand wants.
- **Bilingual serif wordmark lockup** — HeyTea's 2026 rebrand and most premium CJK tea brands run a dual-language logo — a CJK mark paired with a Latin logotype — signaling cultural authority and global polish.
  - How: Pair Fraunces (Latin 'Boba Night') with a quality CJK serif such as Noto Serif SC or Source Han Serif for a 波霸/夜 character set beside or above it. Lock them on a shared baseline/optical grid, ship the CJK glyphs subset via unicode-range in @font-face so you only load the handful of characters used (keeps payload tiny).
  - Fit: Gives the masthead instant heritage credibility and a distinctive editorial signature no Yelp clone has — while the subsetting keeps it mobile-fast.
- **Restrained palette with light-bold contrast blocks** — Xing Fu Tang's site uses a disciplined black/white 'light-bold' system with minimal decoration, distinct content blocks, and a 16px base — restraint reads as premium; only accent colors carry weight.
  - How: Enforce the token palette (obsidian/pearl/champagne) as the whole page, reserving orchid #b46bd6 strictly for a single 'Featured' badge/state via a CSS custom property (--accent-featured) so it never leaks. Use type scale and whitespace — not extra colors — for hierarchy; base font 16-17px, clamp() for fluid display sizes.
  - Fit: Protects the luxury feel: orchid stays rare and meaningful (a truly featured spot 'glows'), and the front page never devolves into the multicolor candy look of CoCo/Chatime directories.
- **Curved organic geometry for cards and CTAs** — Machi Machi uses curved surfaces and 'floating' organic forms to feel exploratory and high-end rather than the boxy, linear grid of a functional menu.
  - How: Give discovery cards a large asymmetric border-radius (e.g. border-radius: 24px 24px 24px 4px) or a soft blob mask, elevate on hover with a subtle transform: translateY(-4px) and a champagne 1px inner border (box-shadow inset). Keep transitions ~180ms ease-out and gate hover effects behind @media (hover:hover) so mobile taps stay instant.
  - Fit: Softens the 'nearest boba to me' result cards into something that feels curated and tactile — matching the after-dark, sensual mood — while staying a lightweight CSS-only interaction that performs on phones.

**Steal this**

- Shoot/commission one signature drink photo per featured SoCal shop on the obsidian bg with champagne rim-light; make it the front-page hero rotation.
- Add a 3-5% feTurbulence SVG grain layer over #0B0C0E site-wide so the dark never looks flat/unstyled.
- Reserve orchid #b46bd6 for a single 'Featured tonight' badge state via one CSS variable — never anywhere else.
- Build a bilingual masthead: Fraunces 'Boba Night' + a subset CJK serif character, locked on a shared baseline.
- Replace the results grid with scroll-revealed editorial blocks (view()-timeline fade-up) framing 'closest boba near you' as a curated pick.
- Give a short heritage/story block per neighborhood (Rowland Heights, Cypress) in Fraunces at ~66ch — proximity results wrapped in magazine narrative, not a list.

**Sources**

- [UI/UX Web Design Case Study: Gong Cha — Verz Design](https://verzdesign.com/case-studies/gong-cha) — Documents Gong Cha's deliberate choice of real product photography over graphic icons, Libre Baskerville serif + Arial pairing, and instructional visual hierarchy — directly relevant to a photo-led discovery site.
- [Machi Machi — LOOP Design Awards](https://loopdesignawards.com/project/machi-machi/) — Details Machi Machi's luxury cues: Venetian plaster texture that 'mimics the effervescence of bubbles,' curved organic geometry, and Instagrammable brand moments — texture and form ideas that translate to a dark web surface.
- [Brand Story | XING FU TANG (the 'Hermès of bubble tea')](https://www.xingfutang.com.tw/article_d.php?lang=en&tb=2&id=327) — Shows how a boba brand builds luxury through heritage craft ('ancestral stir-frying of brown sugar'), restrained typography, and founder-values storytelling — the editorial-magazine positioning Boba Night wants.
- [Design in China: Nayuki Tea and Bakery — Animaze](https://www.animaze-group.com/2023/08/16/design-in-china-e53-nayuki-tea-and-bakery-%E5%A5%88%E9%9B%AA%E7%9A%84%E8%8C%B6-where-imagination-meets-tea-perfection/) — Explains Nayuki's 'mental shelter' lifestyle-café mood, natural/woody-greenery palette, and curated art collaborations — a model for editorial curation and a jade-accented calm mood.
- [The Subtly Younger HeyTea Rebrand — Design Compass](https://designcompass.org/en/2026/01/14/heytea-subtly-younger-rebrand/) — Covers HeyTea's 2026 bilingual (CJK + Latin) logo system built for global markets, splitting symbol and logotype — a template for a dual-language serif wordmark.
- [Machi Machi — rebranding by Irène Chazalviel (Behance)](https://www.behance.net/gallery/194124113/machi-machi-rebranding) — Visual reference for how Machi Machi's premium pink/neutral identity is executed across typographic lockups and packaging, showing restrained luxury layout.

## Luxury tea house brands

The best luxury tea houses win on restraint, not ornament: Mariage Frères and TWG prove a dark-or-cream editorial canvas plus a single gold accent, poetic serif headlines, and multi-axis "discovery" navigation (by mood, origin, moment — not by SKU) reads as luxury rather than directory. For Boba Night the highest-leverage steal is reframing browse-by-city into browse-by-moment/mood/neighborhood the way these houses browse tea by "Tea Moments," plus founder/heritage storytelling and quiet honesty chips that make a listing feel curated and human.

**Techniques**

- **Obsidian-and-gold editorial canvas with a single accent** — Mariage Frères runs a near-black theme (#090909) with white type and ONE gold accent reserved for the logo and key CTAs — luxury comes from the restraint, not from many colors. TWG does the inverted cream (#fffef1) version with the same single-gold discipline.
  - How: Lock a CSS custom-property token set: --obsidian:#0B0C0E, --pearl:#F4EFE7, --gold:#C5A46D and gate gold to only CTAs, active nav, and the featured badge via a single utility class (.is-accent). Reserve --orchid:#b46bd6 strictly for a 'Featured tonight' state so it never competes with gold. Enforce with a limited token palette.
  - Fit: Boba Night already has this exact palette — the discipline these houses show (gold ONLY on CTAs/featured, never decoratively) keeps the front page from sliding into a colorful Yelp look. Use jade #123F35 as the near-black card surface over obsidian for depth.
- **Poetic serif hero over a full-bleed atmospheric image** — TWG opens with 'A Voyage of Discovery' / 'Steeped for Departure' in understated serif with generous letter-spacing over aspirational lifestyle photography — mood first, product second. Mariage Frères uses a rotating full-width atmospheric carousel, not clinical product shots.
  - How: Full-viewport hero: a single dark, grainy night photo (boba shop at night, neon reflections) with a Fraunces display headline at clamp(2.5rem,6vw,5rem), letter-spacing:-0.02em, and a short Inter subhead. Add a CSS mask-image linear-gradient bottom fade so the image melts into --obsidian; lazy-load with a low-res blur-up placeholder for mobile. Avoid JS carousels — one strong still is faster and more luxe.
  - Fit: Sets the 'after dark' editorial tone instantly and differentiates from every boba directory that opens with a search bar and map. The Fraunces headline over an obsidian-fading night photo is the single biggest 'luxury magazine, not Yelp' signal for the front page.
- **Multi-axis discovery: browse by mood/moment, not by SKU** — Palais des Thés lets you enter by origin, by benefit (sleep, energy, digestion), and by mood/season; Mariage Frères groups tea by 'Tea Family', 'Fragrance', 'Origins', and 'Tea Moments' — curated lenses, not an alphabetical list. This is the core mechanic that makes a large catalog feel editorial.
  - How: Build 3-4 editorial entry tiles as a CSS grid of anchor cards ('Open Late', 'Date Night', 'Near You', 'Neighborhood Gems'), each a large image card with a Fraunces label and gold hover underline (background-position transition, no layout shift). Back them with your existing Supabase city field plus tags; each tile is a filtered query.
  - Fit: Directly answers the project brief — 'find boba closest to me at Rowland Heights / Cypress'. Reframe the Supabase city data as a 'By Neighborhood' lens alongside 'Open Late' and 'Date Night' moments, so proximity discovery feels curated rather than like a database filter.
- **Taste-descriptor cards + a low-friction 'where to start' quiz** — Ippodo's product cards carry two-word taste tags ('Rich & Smooth', 'Light & Calm') and a 'Not Sure Where to Start?' quiz entry, giving personality and a guided path without clutter. Palais uses one-line evocative descriptors under each item.
  - How: Design boba cards: image top, Fraunces shop name, then 1-2 pill tags ('Brown Sugar · Cozy', 'Cheese Foam · Loud') as small-caps Inter chips with a hairline gold border, price/distance line, no star ratings. Keep cards as one reusable component. The quiz can be a 3-question client-side flow writing to a query string — no backend.
  - Fit: Replaces Yelp-style star ratings (which cheapen the look) with editorial flavor/vibe tags matching Boba Night's voice, and the mini-quiz gives an indecisive 'boba night' visitor a guided, branded path to a nearby spot.
- **Heritage/founder editorial voice + a Journal** — Rare Tea Company centers founder Henrietta and 'terroir/direct-trade' pillars and runs a substantive 'Rare Tea Journal'; Mariage Frères foregrounds 'à Paris depuis 1854' and a 'History & Savoir-faire' section. The point of view is the luxury signal.
  - How: Add a short 'A note from the maker' band on the front page (Fraunces pull-quote, gold em-dash, small mark) and a lightweight editorial/journal index (static MD-driven pages) for neighborhood guides. Use a large blockquote with a hanging gold quotation glyph via ::before.
  - Fit: Turns Boba Night from an aggregator into a curated SoCal point of view — 'our favorite after-dark spots' framing — which justifies the luxury treatment and builds trust a directory can't. Neighborhood guides double as SEO/GEO surfaces for each SoCal city.
- **Restrained trust signals + honest per-visit framing** — Palais des Thés places 'Featured in' press logos (Vogue, WSJ) and quiet sample/shipping badges; Rare Tea shows a price-per-cup calc to make premium feel fair. Trust is conveyed with a light touch, tucked below the fold, never shouty.
  - How: A single muted row of monochrome trust marks (inline SVG, desaturated to --pearl at ~40% opacity) below the hero, and per-listing honesty chips like '$ · 12 min away · open till 1am' in Inter small caps. Keep these grayscale so gold stays the only color that pops.
  - Fit: Gives credibility for a new SoCal brand without loud badge-spam that reads cheap, and the 'open till 1am / X min away' chips reinforce the 'after dark, near me' promise at the heart of the project — luxe, useful, fast.

**Steal this**

- Gate gold (#C5A46D) to CTAs, active nav, and the featured badge ONLY — copy Mariage Frères' one-accent discipline; let jade #123F35 do card-surface work over obsidian for depth.
- Open with a single full-bleed obsidian-fading night photo + a Fraunces poetic headline (TWG's 'Steeped for Departure' energy), not a search bar or map — one still image, no JS carousel, blur-up on mobile.
- Rebuild navigation as curated 'moment' lenses — Open Late / Date Night / Near You / By Neighborhood — mirroring Mariage Frères' 'Tea Moments'; back each with the existing Supabase city + tags.
- Replace star ratings with two-word taste/vibe pill tags on each boba card (Ippodo's 'Rich & Smooth' pattern): e.g. 'Brown Sugar · Cozy', 'Cheese Foam · Loud'.
- Add a 3-question client-side 'where should we go tonight?' quiz (Ippodo's 'Not Sure Where to Start?') that writes to a query string and lands on a nearby filtered result — no backend.
- Add a founder/curator 'A note from the maker' pull-quote + lightweight neighborhood Journal (Rare Tea's model), and keep trust signals quiet: grayscale press marks + '$ · 12 min · open till 1am' honesty chips so gold stays the only pop of color.

**Sources**

- [Mariage Frères — French tea since 1854](https://www.mariagefreres.com/en/) — Dark (#090909) editorial theme with a single gold accent and heritage-forward storytelling — the closest direct analog to Boba Night's obsidian + champagne 'after dark' palette.
- [TWG Tea — Luxury Teas & Accessories Online](https://twgtea.com/) — Poetic serif hero copy ('A Voyage of Discovery', 'Steeped for Departure') and restrained cream/gold grid — model for aspirational voice + minimalism over a Yelp grid.
- [Ippodo Tea (Kyoto since 1717)](https://ippodotea.com/) — Taste-descriptor product cards ('Rich & Smooth', 'Light & Calm') and a 'Not Sure Where to Start?' quiz — a clean discovery pattern that translates directly to boba flavor/vibe tags.
- [Palais des Thés — Premium Teas](https://us.palaisdesthes.com/en_us/) — Multi-axis discovery (by origin, by benefit, by mood/season) via visual mega-menus plus press logos and sample badges — the exact 'browse by mood not SKU' navigation to mirror for SoCal cities/vibes.
- [Rare Tea Company](https://rareteacompany.com/) — Founder-led narrative (Henrietta), terroir/direct-trade pillars, and a 'Rare Tea Journal' — editorial authority model for turning boba listings into a curated point of view.

## Premium beverage DTC sites

The premium beverage DTC playbook is: lead with one oversized editorial display headline over rich product/lifestyle photography, keep the base palette calm and let the product's color be the only loud thing, and layer in exactly one signature motion or texture gimmick (a branded cursor, a grain/star filter, a slow scroll reveal) rather than many. The "premium not Yelp" feeling comes from restraint, generous whitespace, foil/metallic accents, and human storytelling blocks — all cheap to implement and mobile-safe if you gate motion behind prefers-reduced-motion. Boba Night can steal the editorial-headline-over-photo hero, a gold-foil text treatment, an after-dark grain/star overlay, and a single tasteful scroll-reveal rhythm.

**Techniques**

- **Signature branded cursor (desktop only)** — Waterdrop replaces the default pointer with a persistent brand mark (a '¼' glyph) that follows the cursor across the whole site — a single, cheap, memorable motion signature instead of scattered animations.
  - How: pointermove listener translating a fixed-position element with transform: translate3d() (GPU-cheap), or CSS cursor: url(pearl.svg). Add a lerp/easing trail with requestAnimationFrame for a slight lag. Gate behind a (hover: hover) and (pointer: fine) media query so it never loads on touch, and behind prefers-reduced-motion.
  - Fit: A small champagne-gold boba pearl (or soft gold glow) trailing the cursor on desktop gives Boba Night one ownable motion signature against the obsidian background without touching mobile performance or the 'luxury magazine' calm.
- **Oversized editorial display headline crossing the product image** — Ghia's identity is built on a fat-stress Italian script wordmark that dramatically crosses the label; DTC hero sections mirror this by letting one huge serif headline overlap the product/lifestyle photo instead of sitting in a tidy box.
  - How: CSS grid with overlapping grid-area (headline and image share the same cell, different z-index), Fraunces at a fluid clamp() size (e.g. clamp(2.75rem, 9vw, 7rem)) with tight letter-spacing and optical sizing 'opsz'. Use mix-blend-mode: difference or a subtle text-shadow so type stays legible where it crosses the image.
  - Fit: Boba Night's Fraunces display headline overlapping a moody nighttime drink shot instantly reads editorial/magazine, not directory — the single strongest lever to escape the Yelp look, and it's pure CSS.
- **Gold-foil / metallic text treatment for accents** — Ghia leans on gold-foil label details to signal luxury; premium beverage sites echo this with metallic gradient type on select words (brand name, 'Featured', section eyebrows) rather than flat color everywhere.
  - How: background: linear-gradient across champagne tones (#C5A46D #E8D5A8 #C5A46D) with background-clip: text; -webkit-text-fill-color: transparent. Optional very slow background-position shimmer via @keyframes (disable under prefers-reduced-motion). Keep it to 1–2 words per screen.
  - Fit: Applied to the Boba Night wordmark and 'Featured' eyebrows, the champagne #C5A46D reads as real foil against obsidian — premium restraint that keeps gold as an accent, not a fill.
- **After-dark grain + subtle star/particle overlay** — Ghia uses an 'iconic starry filter' over its art direction to create mood; grain/noise overlays are a common DTC trick to make flat dark backgrounds feel filmic and expensive rather than empty.
  - How: An SVG <filter> with feTurbulence + feColorMatrix as a fixed, pointer-events:none, low-opacity (3–6%) overlay layer, OR a small tiling PNG noise texture. For stars, a single <canvas> drawing a handful of slow-twinkling points, capped to a low count and paused via IntersectionObserver + prefers-reduced-motion.
  - Fit: A faint grain plus a few slow gold/pearl 'stars' over the #0B0C0E obsidian sells the 'after dark' concept and hides banding on dark gradients — atmospheric, tiny payload, and invisible to performance if you use SVG grain over canvas.
- **Alternating photo/text storytelling blocks with human faces** — Olipop's story page alternates founder/advisor portraits with mission copy and 'Feed Life / Adapt & Improve' value blocks, building emotional, credible narrative instead of a product grid — positioning by feeling (nostalgia, status, warmth).
  - How: A repeating two-column grid section that flips order:reverse on alternate rows, collapsing to a single column on mobile. Pair each with a short editorial caption in Inter and a Fraunces sub-head. Add scroll-reveal (below) for entrance.
  - Fit: Instead of a flat list of shops, Boba Night can run alternating 'shop spotlight' blocks — a nighttime photo of the spot beside a one-line editorial note — making discovery feel like reading a city magazine, reinforcing the anti-directory brand.
- **Single calm scroll-reveal rhythm (not scrollytelling overload)** — The strongest DTC sites use one restrained scroll behavior — content fades/rises slightly as it enters — rather than heavy pinned scrollytelling, keeping things fast and elegant.
  - How: Native CSS scroll-driven animations (animation-timeline: view(); opacity + translateY) where supported — zero JS; fall back to IntersectionObserver toggling a class. Reserve GSAP ScrollTrigger / Lenis smooth-scroll only if you later want one hero moment. Keep offsets small (12–20px), durations ~500ms, and wrap all of it in @media (prefers-reduced-motion: no-preference).
  - Fit: A uniform 500ms fade-up as each shop card and section enters gives Boba Night's front page a composed, premium cadence (Spotify/Airbnb-like) on mobile without janky libraries or a heavy JS bundle.

**Steal this**

- Hero: one giant Fraunces headline overlapping a single moody nighttime boba photo (CSS grid overlap + clamp() type) — kill any boxed hero card.
- Add a desktop-only trailing gold boba-pearl cursor as the one ownable motion signature; never load it on touch.
- Use background-clip:text champagne gradient on just the wordmark and 'Featured' eyebrows so gold reads as foil, not fill.
- Lay a 4–6% SVG feTurbulence grain + a few slow-twinkling gold 'stars' over the obsidian to make 'after dark' filmic and hide dark-gradient banding.
- Replace any shop list-grid with alternating photo/text 'spotlight' blocks (flip order per row, one-line editorial caption) so discovery feels magazine, not Yelp.
- Ship one uniform ~500ms fade-up-on-enter (native animation-timeline: view() with IntersectionObserver fallback), all gated behind prefers-reduced-motion.

**Sources**

- [Olipop — Our Story (live page)](https://drinkolipop.com/pages/our-story) — Direct example of alternating founder/advisor photo+text storytelling blocks, value-theme sections, and 'New/Limited' badges on a calm neutral base.
- [The Olipop Playbook — 9 Birds](https://www.9-birds.com/insights/the-olipop-playbook-how-to-build-and-brand-a-billion-dollar-beverage-in-2025) — Documents Olipop's emotion-first positioning (nostalgia, status, warmth) and outsized branding investment — the strategic 'why' behind the storytelling patterns.
- [Ghia packaging & identity — BP&O](https://bpando.org/2022/06/23/packaging-design-ghia/) — Details Ghia's fat-stress Italian display type crossing the label, gold-foil accents, and the 'starry filter' art direction — sources for the editorial-headline, foil-text, and grain/star techniques.
- [Ghia bottle redesign — Fast Company](https://www.fastcompany.com/90879705/ghia-nonalcoholic-apertif-redesign-bottle-melanie-masarin) — Confirms Ghia's deliberate balance of Mediterranean warmth/joie de vivre with premium restraint — the fun-vs-luxury tension Boba Night wants.
- [Beverage website examples (Waterdrop analysis) — It's Fun Doing Marketing](https://www.itsfundoingmarketing.com/inspiration/drinks-beverages-website-examples) — Documents Waterdrop's persistent branded '¼' cursor as a single signature interaction instead of heavy animation — basis for the branded-cursor technique.
- [Liquid Death official website design — Serge Vasil (Behance)](https://www.behance.net/gallery/190145333/Liquid-Death-Official-Website-Design) — Verifies a premium beverage DTC build on Shopify with custom illustration collaborators — evidence that 'edgy but premium' is executed through art direction, not gimmick overload.

## Matcha & Japanese/Taiwanese cafe aesthetics

Premium matcha and Japanese-tea sites (Ippodo, Kettl, Cuzen, % Arabica) win through restraint, not effects: video heroes of craft/ritual, huge negative space (Ma), heritage micro-copy, and letting one saturated natural color (jade green) pop against neutral fields. Boba Night can borrow this calm-luxury discipline — a single restrained hero video, generous whitespace, slow easing, and jade used as a rare accent — to read as an editorial tea brand rather than a listings directory, without adding weight.

**Techniques**

- **Single-accent discipline (jade-on-obsidian)** — Premium tea sites let ONE saturated natural color carry all the visual energy against a large neutral field — Cuzen's vivid jade on wood/white, Kettl's lone accent on white. The neutral does 90% of the work; the color is a rare event.
  - How: CSS custom properties with a strict rule: --obsidian and --pearl own all large surfaces; --jade #123F35 and --champagne #C5A46D appear only on 2-3 elements per viewport (one CTA, active nav underline, a single stat). Orchid reserved strictly for the 'featured' badge. Audit each section: if more than ~10% of pixels are accent, pull back.
  - Fit: Boba Night already has the exact palette matcha brands earn their calm from. The upgrade is enforcement — using jade as a scarce jewel on obsidian rather than tinting cards/dividers/icons. This separates 'luxury magazine' from 'Yelp with a dark theme,' and costs zero performance.
- **Full-bleed craft/ritual video hero (poster-first, lazy)** — Ippodo, % Arabica, and Kettl all open on a silent, looping full-width video of the craft act (whisking, pouring, steam) instead of a headline block. It communicates 'experience' before a single word and sets an unhurried pace.
  - How: <video autoplay muted loop playsinline preload='none' poster='hero.avif'> with a compressed ~6-10s clip (H.265/AV1, <2MB, ~1200px wide) and a poster that renders instantly. Gate the video behind matchMedia('(prefers-reduced-motion: no-preference)') and IntersectionObserver so it never blocks LCP or plays on data-saver/reduced-motion. Fall back to the poster.
  - Fit: A slow-motion boba pour / pearls dropping through milk over obsidian, jade-lit, instantly reframes the front page from 'directory' to 'after-dark experience.' The poster-first + lazy pattern keeps it mobile-fast and accessible — the LCP is the poster, not the video.
- **Ma — engineered negative space** — The defining move of Ippodo/% Arabica is aggressive whitespace: double the breathing room around headlines and imagery, sparse nav (% Arabica ships only 5 links), sections separated so the eye rests. Emptiness reads as confidence.
  - How: Adopt a spacing scale where section vertical padding is generous (clamp(4rem, 10vw, 9rem)) and headings carry large margin-block. Cap hero/nav to 4-6 items. Use a max-width prose measure (~62ch) so text never sprawls. Fluid clamp() values keep the airiness on mobile instead of collapsing to cramped.
  - Fit: Boba Night's Fraunces display headings need room to feel editorial. Widening the rhythm and trimming nav to essentials (Near Me / Open Late / Date Night / Featured) makes it feel like a magazine spread, and less content-per-screen paints faster.
- **Slow gravity easing on all motion** — Wabi-sabi/luxury cafe sites deliberately slow every transition — buttons fade over ~0.5s, nothing pops instantly, easing mimics gravity (slow start, fast middle, soft settle). Calm pace = premium.
  - How: Define tokens: --ease-settle: cubic-bezier(0.16, 1, 0.3, 1); --dur: 480ms. Apply to hover states, reveal-on-scroll, and nav. Use IntersectionObserver + an .in-view class for one-time fade/translate-up reveals (opacity + transform only, GPU-cheap). Wrap all of it in @media (prefers-reduced-motion: no-preference).
  - Fit: Cheap, tasteful polish that makes card hovers and scroll reveals on the finder feel intentional rather than snappy/webby. Transform+opacity-only keeps it 60fps on phones; the reduced-motion guard keeps it accessible.
- **Editorial IA: verb-led sections, not a filter wall** — Kettl organizes as Shop / Experience / Learn and Ippodo leads with education and pairings — experience-first framing, not a database dump. The nav tells a story instead of exposing a filter panel.
  - How: Structure the front page as named editorial modules ('Closest to you', 'Open past midnight', 'Date-night worthy', 'This week's featured') each as a horizontally-scrollable rail (CSS scroll-snap-type: x mandatory) rather than a paginated grid. Anchor nav links jump to these modules.
  - Fit: Directly serves the project's core goal (find the nearest boba fast) while keeping the luxury-magazine feel. A 'Closest to you' snap-rail at top uses the Supabase city data to surface proximity as a curated shelf, not a Yelp result list.
- **Heritage/ritual micro-copy as texture** — Ippodo anchors prestige with 'Since 1717'; Cuzen leans on 'rituals,' 'journeys,' 'centuries of tea preparation.' Small ceremony-toned lines do heavy lifting for perceived quality with zero design cost.
  - How: Plain HTML — small caps or letter-spaced eyebrow labels (font-variant-caps: all-small-caps; letter-spacing: 0.12em) in champagne above headings, and short evocative kickers per rail ('for the 11pm craving'). No JS.
  - Fit: Boba Night's 'after dark' angle is a story matcha brands would kill for. A few letter-spaced champagne eyebrows in Fraunces/Inter turn utilitarian section titles into editorial captions and reinforce the luxury-magazine voice instantly.

**Steal this**

- Storyboard one 6-8s slow-motion boba pour (pearls falling through milk, steam, jade rim-light on obsidian) as a poster-first, lazy-loaded full-bleed hero video — the single biggest 'experience not directory' upgrade.
- Enforce a hard single-accent rule: jade and champagne on <3 elements per viewport, orchid only on featured badges; everything else obsidian/pearl.
- Rebuild the front page as verb-led editorial rails ('Closest to you', 'Open past midnight', 'Date-night worthy') using CSS scroll-snap instead of a filtered results grid.
- Add motion tokens (--ease-settle: cubic-bezier(0.16,1,0.3,1), 480ms) for slow gravity easing on hovers plus one-time IntersectionObserver scroll reveals, all behind prefers-reduced-motion.
- Widen vertical rhythm with clamp(4rem,10vw,9rem) section padding, cap text to ~62ch, and trim nav to ~4 essentials so Fraunces headings breathe like a magazine spread.
- Add letter-spaced champagne small-caps eyebrows ('for the 11pm craving') above each rail to inject ritual/heritage tone at zero cost.

**Sources**

- [Ippodo Tea Global (Kyoto, since 1717)](https://global.ippodo-tea.co.jp/) — Reference for calm premium tea e-commerce: neutral palette, generous grid, restrained animation, heritage micro-copy, product-as-hero photography.
- [% Arabica (en)](https://arabica.com/en/) — Master class in extreme minimalism: sparse nav (5 items), white-space-first layout, symbolic '%' branding, full-bleed video-first hero with no text clutter.
- [Cuzen Matcha](https://cuzenmatcha.com/) — Shows how to make jade/vivid green the hero against neutral wood/ceramic backdrops, plus ritual/ceremony language that elevates product to experience.
- [Kettl Tea](https://kettl.co/) — Full-width craft video hero, editorial Shop/Experience/Learn IA, single accent color (#574CD5) on white — proof an accent-on-neutral system reads luxury.
- [Wabi-Sabi in Web Design: Implementing Imperfection (Silphium Design)](https://silphiumdesign.com/wabi-sabi-web-design-implement-imperfection/) — Concrete CSS techniques for organic shapes, grain texture, asymmetry, slow gravity easing, and Ma/Kanso spacing principles.

## Best-in-class discovery / directory UX

The best food-discovery products beat the "Yelp directory" feeling by leading with editorial curation and occasion-based framing (The Infatuation's "Perfect For" tags and expert-not-rubric ratings), thematic hand-picked rails instead of one flat sorted list (Resy's Discover shelves), and light, tasteful progression/social signals (Beli's lists, milestones, taste-matched leaderboards). For Boba Night the highest-leverage move is to reframe the front page from a proximity list into a small set of curated, occasion-tagged collections wrapped in editorial voice and full-bleed photography — luxe magazine, not database.

**Techniques**

- **Occasion tags ('Perfect For') instead of cuisine filters** — The Infatuation labels every listing with behavioral tags like 'Date Night,' 'Casual,' 'Impressing Out-of-Towners' rather than only category/cuisine, so people match a spot to a moment, not a keyword.
  - How: Add a short tag taxonomy to your Supabase rows (e.g. perfect_for: ['Date Night','Study Session','Open Late','Group Hang']). Render as small pill chips under each card in champagne #C5A46D outline on obsidian; make them clickable to filter. Pure CSS fl‑wrap chip row (display:flex; gap; flex-wrap) — no library needed.
  - Fit: Directly serves the Project brief ('date night hub', 'open late' docs already exist). Turns Boba Night from 'boba near Rowland Heights' into 'a late-night date spot near you' — the after-dark, editorial angle the brand wants.
- **Curated thematic rails, not one flat sorted list** — Resy's Discover page segments content into hand-picked horizontal shelves (Date Night Destinations, Top Rated, New, 'climbing the ladder') so browsing feels curated and endless without an algorithmic feed.
  - How: Build 3-5 horizontal scroll rails with CSS scroll-snap (overflow-x:auto; scroll-snap-type:x mandatory; each card scroll-snap-align:start). Each rail is a Supabase query (nearest, open-now, new, staff-pick). No carousel JS library — native scroll-snap is fast and mobile-perfect.
  - Fit: Replaces a Yelp-style ranked list with magazine 'shelves.' A 'Closest to You Tonight' rail satisfies the proximity requirement while 'Open Past Midnight' and 'Featured' (orchid #b46bd6) rails add the luxury-mag texture.
- **Editorial ratings, not 5-star averages** — The Infatuation deliberately rejects a rigid star rubric; ratings come from 'expertise, context, and instinct,' every one 'verified by a visit in the past year,' presented as an opinion with voice.
  - How: Store a single editorial score + a one-line verdict field + last_verified date. Render the score in Fraunces display type, not a row of star glyphs; show a 'Verified [month]' micro-label. Avoid importing Yelp star widgets entirely.
  - Fit: A distinctive, non-Yelp rating treatment is the single clearest signal of 'luxury editorial, not directory.' Fraunces numerals + a terse verdict reads like a magazine pick and reinforces the obsidian/champagne palette.
- **Personality-driven card copy (short verdict line)** — Infatuation listings read like tiny magazine articles — vivid, specific one-liners ('hipster Hillstone,' 'puffy life preservers') instead of neutral database descriptions.
  - How: Add a 60-90 char 'verdict' text field per venue rendered as the card subtitle in Inter italic or Fraunces. Keep name in Fraunces display, metadata (price, neighborhood, distance) in small Inter caps with letter-spacing.
  - Fit: Copy voice is what most separates editorial from directory and it's cheap to add. One sharp line per boba shop ('The taro that ruins all other taro') gives Boba Night its after-dark personality.
- **Full-bleed photography as the card, text overlaid** — Editorial guides let photography carry each listing — large imagery the layout is built around, not a thumbnail beside text.
  - How: Card = a single full-bleed image with a bottom obsidian gradient scrim (linear-gradient to transparent) and name/tags overlaid. Use loading='lazy', width/height attrs to prevent CLS, and modern formats (AVIF/WebP via <picture>). aspect-ratio CSS to hold layout.
  - Fit: Boba is intensely photogenic and this is the core Spotify/Airbnb feel. Dark scrim over imagery is literally the 'after dark' aesthetic and keeps pearl #F4EFE7 text legible over any photo.
- **Lightweight lists + taste signals (Beli), used sparingly** — Beli drives repeat visits with save-to-list, a map view of saved spots, milestone celebrations, and a taste-matched leaderboard (green = similar palate) — engagement without clutter.
  - How: Start with a single 'Save' (bookmark) action persisting to Supabase + a 'Your Spots' map (use Maplibre GL JS with a dark style, or a static styled map to stay light). Skip points/badges; add only a subtle 'Saved by locals' count if data exists.
  - Fit: Gives a reason to return without turning the luxe brand into a gamified app. A dark-themed saved-spots map matches the obsidian palette and answers the 'find one closest to me' brief with a personal, ownable layer.

**Steal this**

- Add a 'perfect_for' tag array in Supabase and render champagne pill chips under every card — filter by moment (Date Night / Open Late / Study) instead of cuisine.
- Rebuild the front page as 3-5 CSS scroll-snap rails: 'Closest to You Tonight,' 'Open Past Midnight,' 'Featured' (orchid), 'New This Month' — each a separate Supabase query.
- Kill the 5-star widget; show one Fraunces editorial score + a 'Verified [month]' freshness label per venue.
- Give every venue a 60-90 char verdict line in the card as its subtitle — vivid and specific, magazine voice.
- Make each card a full-bleed AVIF/WebP image with an obsidian bottom gradient scrim and pearl text overlaid; set aspect-ratio + width/height to kill layout shift.
- Add a single 'Save' bookmark and a dark-styled 'Your Spots' map (Maplibre GL dark theme); skip points and badges to protect the luxury feel.

**Sources**

- [Design Critique: Beli App — IXD@Pratt](https://ixd.prattsi.org/2024/09/design-critique-beli-app/) — Concrete breakdown of Beli's category icons, list-keeping, map view, milestone celebrations, and taste-matched leaderboards — the engagement/gamification patterns.
- [Design Critique: Resy (iOS app) — IXD@Pratt](https://ixd.prattsi.org/2025/02/design-critique-resy-ios-app-2/) — Documents Resy's Discover page structure: thematic curated shelves (Date Night, Top Rated, climbing/new) and restrained low-info cards.
- [The Hit List: New LA Restaurants To Try Right Now — The Infatuation](https://www.theinfatuation.com/los-angeles/guides/best-new-los-angeles-restaurants-hit-list) — Real LA guide showing the 'Perfect For' occasion tags, editorial card layout, price tier, and personality-driven copy voice.
- [Welcome To The New Infatuation — Ratings Relaunch](https://www.theinfatuation.com/all/features/new-infatuation-ratings-relaunch) — Explains their expertise/context/instinct rating philosophy and freshness ('verified within the past year') — how to make ratings feel editorial and trustworthy, not a 5-star average.
- [Beli App — Restaurant List Keeping (official)](https://beliapp.com/) — Primary source for Beli's list-first, ranked-comparison model of saving and organizing places.

## Map-based near-me UI patterns

The dominant modern near-me pattern is a persistent map with a draggable bottom sheet of ranked results and synced pins — and on the web this can now be built with CSS scroll-snap instead of heavy JS gesture libraries, which suits Boba Night's "fast, tasteful, mobile-first" mandate. The delight lives in the details: a contextual location prompt, a "blue dot" that animates in, distance-sorted cards, and a "search this area" affordance when the user pans. For Boba Night, style a dark MapLibre basemap in the obsidian/champagne palette so the map itself reads as editorial luxury rather than a stock Google Maps directory.

**Techniques**

- **CSS scroll-snap bottom sheet (map + ranked list)** — A persistent map behind a draggable sheet of boba spots with 3 snap detents (peek ~15vh showing the nearest place, half ~50vh, full-screen list). Dragging the sheet is native browser scrolling, not JS gesture math, so it runs on the compositor thread and never jank-drops frames.
  - How: Use the pure-web-bottom-sheet web component, or hand-roll it: a scroll container with overflow-y:scroll; scroll-snap-type:y mandatory; invisible snap targets (scroll-snap-align:start) positioned at top:var(--snap); and CSS scroll-driven animations (animation-timeline) for the peek. Wrap in <dialog> for focus-trap or the Popover API for light-dismiss accessibility.
  - Fit: Delivers the Airbnb/Apple-Maps feel with almost no JS, honoring Boba Night's 'fast, performant, mobile-first' bar. The sheet's grabber handle and card edges become brand surfaces: pearl cards on obsidian, a thin champagne hairline handle — an editorial magazine index that slides over a map, not a Yelp list.
- **Branded dark basemap (kill the stock-Google look)** — Replace the default road-heavy, primary-colored basemap with a custom-styled dark map: obsidian land, muted jade water/parks, hidden minor roads and POI labels, so the only bright things are your own boba pins.
  - How: MapLibre GL JS (open-source, free, no Mapbox token) with a custom style JSON — set land to #0B0C0E, water to a desaturated #123F35, labels to pearl at low opacity, and strip commercial POIs. Vector tiles keep it crisp and fast on mobile.
  - Fit: This single move is what separates 'luxury after-dark discovery' from 'a directory with a map widget.' A dark champagne-accented map reads as Spotify/luxury-magazine and makes each featured spot's orchid pin genuinely pop against the obsidian field.
- **Contextual 'near me' permission + animated blue dot** — Never fire the raw browser geolocation prompt cold. Show a branded pre-prompt ('Find boba closest to you tonight — we'll use your location just for this') then, on grant, fly-to and drop an animated location marker. On denial, fall back to the city you already have from Supabase.
  - How: Custom in-page prompt navigator.geolocation.getCurrentPosition() only after the user taps 'Use my location.' Animate map.flyTo() and a pulsing marker (CSS @keyframes ring pulse). Cache the fix; degrade to the Supabase city centroid if permission is denied or times out.
  - Fit: Directly serves the project brief ('if I'm at Rowland Heights or Cypress, make it easy to find the closest boba'). The champagne pulsing dot flying to your neighborhood is the 'near-me delight' moment; the Supabase-city fallback means the page is never dead if location is blocked.
- **Distance-sorted cards synced to pins (List + details)** — Every result card shows a computed distance ('0.4 mi · 7 min') and the list is sorted nearest-first; tapping a card highlights its pin and recenters, tapping a pin scrolls the sheet to that card. Two-way selection binding is the pattern that makes map+list feel like one object.
  - How: Compute haversine distance client-side from the user fix to each spot's lat/lng (or PostGIS ST_Distance / an RPC in Supabase for server sorting). Give each card data-id matching its marker; on marker click, scrollIntoView({behavior:'smooth'}) the card and toggle a selected class (champagne border, subtle lift).
  - Fit: Turns raw proximity into an editorial ranking — 'The 6 closest to you, in order' — which matches the magazine tone better than a plain radius list. Distance + walk-time is the concrete utility the user asked for, presented as curation, not a spreadsheet.
- **Marker clustering for SoCal density** — When zoomed out over a dense corridor (e.g., the SGV / 626), collapse overlapping pins into a single champagne cluster bubble with a count; it splits apart as the user zooms in.
  - How: MapLibre's built-in cluster:true on a GeoJSON source (Supercluster under the hood) with cluster-count symbol layers, or the Leaflet.markercluster plugin if on Leaflet. Style cluster bubbles in champagne with Fraunces numerals.
  - Fit: SoCal boba is extremely dense; without clustering the map is a blob of overlapping pins that looks cheap. Clean, counted clusters keep the map calm and premium at every zoom, and the numerals in Fraunces reinforce the type system.
- **'Search this area' on pan + peek preview** — When the user drags the map away from their location, surface a floating 'Search this area' pill; and in the sheet's peek state show just the single nearest spot as a hero card so the answer to 'where's the closest boba' is visible before any interaction.
  - How: Listen to map 'moveend'; if the center moved beyond a threshold from the last query center, fade in a centered pill button (transform+opacity transition) that re-queries by the new viewport bounds. The peek detent renders one card via the sheet's smallest snap point.
  - Fit: Supports exploration beyond the current neighborhood (checking boba near a date-night destination) without abandoning the near-me default. The champagne pill and single peek card keep first paint minimal and luxurious — one confident recommendation, not a wall of options.

**Steal this**

- 3-detent bottom sheet: peek shows the single nearest spot, half shows ~4 cards + map, full is the whole list — built on CSS scroll-snap so it's JS-light and 60fps on mobile
- Custom obsidian/jade/champagne MapLibre basemap with minor roads and 3rd-party POIs hidden, so only your boba pins carry color — the fastest way to stop looking like Google Maps
- Contextual pre-permission card before the geolocation prompt, with graceful fallback to the Supabase city centroid on denial (page never dies)
- Champagne pulsing 'blue dot' + map.flyTo animation as the near-me delight moment when location is granted
- Two-way pin↔card binding: tap pin scrolls to card, tap card highlights pin and recenters — makes map + list feel like one object
- 'Search this area' pill on map pan, plus Fraunces-numeral champagne cluster bubbles to tame dense SoCal (626/SGV) pin overlap

**Sources**

- [Native-like bottom sheets on the web: the power of modern CSS](https://viliket.github.io/posts/native-like-bottom-sheets-on-the-web/) — Deep, verified technical walkthrough of building an Airbnb/Apple-Maps-style draggable bottom sheet with CSS scroll-snap + scroll-driven animations and near-zero JS — the exact mechanism Boba Night should use for a performant map+list sheet.
- [pure-web-bottom-sheet (GitHub)](https://github.com/viliket/pure-web-bottom-sheet) — Framework-agnostic, SSR-friendly web component implementing that CSS approach with multiple snap points, nested scrolling, and dialog/popover accessibility — a droppable library for the results sheet.
- [Locate Me – Map UI Patterns](https://mapuipatterns.com/locate-me/) — Verified pattern guidance on locate button placement (thumb-reachable bottom corner), blue-dot centering, contextual permission copy, and dynamic button state.
- [Map UI Patterns (catalog)](https://mapuipatterns.com/) — Names the reusable near-me patterns to borrow: Nearby, Blue dot, Cluster marker, Location list, List and details, Search this area, Spatial/Attribute filter.
- [Map UI Design: Best Practices, Tools & Real-World Examples — Eleken](https://www.eleken.co/blog-posts/map-ui-design) — Concrete guidance on custom map styling to match a brand palette, marker clustering for city-scale performance, and collapsible panels to keep the map the hero.
- [Bottom Sheet UI Design: best practices & variants — Mobbin](https://mobbin.com/glossary/bottom-sheet) — Catalog of real app bottom-sheet variants (snap heights, grabber handle, peek state) to calibrate Boba Night's sheet detents against shipping apps.

## Dark after-dark palettes & texture

The strongest "after dark" luxury looks come from three cheap, fast, accessible layers: an almost-black obsidian base lit by soft layered radial "spotlight" gradients (not flat color), a tileable SVG feTurbulence grain overlaid at very low opacity to kill the flat-vector cheapness, and neon used as restraint — a single tight text-shadow/box-shadow glow reserved for featured items, never body copy. All of this is pure CSS/inline-SVG with zero JS payload and degrades cleanly under prefers-reduced-motion.

**Techniques**

- **Champagne-tinted SVG grain overlay** — A single tileable feTurbulence noise texture laid over the whole page at very low opacity so the obsidian base reads like printed magazine stock instead of flat #0B0C0E vector fill.
  - How: Inline data-URI SVG on a ::before with `type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'`, `background-size:180px`, `opacity:0.08–0.12`, `pointer-events:none`, `position:fixed;inset:0`. Tint it champagne by generating via fffuel nnnoise instead of pure gray, or blend with `mix-blend-mode:overlay`. Content sits at z-index:1. Zero JS, ~1KB.
  - Fit: Kills the biggest tell of a cheap dark site (flat black slabs) and gives Boba Night the tactile, editorial-print feel across the whole front page for basically no perf cost.
- **Layered radial spotlight base (not flat black)** — Instead of a solid obsidian background, stack 2–3 large soft radial gradients so light seems to pool behind the hero and featured cards — the 'after dark, lit from within' look.
  - How: `background: radial-gradient(1200px 600px at 20% 0%, rgba(197,164,109,0.10), transparent 60%), radial-gradient(900px 500px at 90% 20%, rgba(18,63,53,0.18), transparent 55%), #0B0C0E;` Layer champagne + jade glows over obsidian. All GPU-cheap, single paint, no images.
  - Fit: Turns the hero from a black rectangle into a moody, dimensional stage; champagne pool warms the Fraunces headline, jade pool adds the 'night lounge' depth without any neon.
- **Reserved neon glow for featured only** — A tight, low-blur orchid glow used exclusively on Featured cards/badges so 'featured' reads instantly as premium, while everything else stays quiet gold/jade.
  - How: `box-shadow: 0 0 0 1px rgba(180,107,214,0.5), 0 0 24px -6px rgba(180,107,214,0.55);` and for a featured label `text-shadow: 0 0 8px rgba(180,107,214,0.6)`. Keep blur small and STATIC — per CSS-Tricks, animating shadows tanks mobile FPS. Two shadow layers max.
  - Fit: Gives Boba Night a Spotify-playlist-highlight moment that separates featured spots from the directory, using the orchid the brand already reserves for featured — restraint is what keeps it luxury not Yelp.
- **Gradient-text gold headline** — The Fraunces display headline filled with a subtle champagne gradient + faint glow so it reads like foil-stamped magazine type.
  - How: `background:linear-gradient(180deg,#F4EFE7,#C5A46D); -webkit-background-clip:text; background-clip:text; color:transparent;` optional `filter:drop-shadow(0 1px 12px rgba(197,164,109,0.25))`. Static, one element.
  - Fit: Elevates the hero wordmark/headline to editorial-luxury without a webfont-heavy logo image; the gold-to-pearl fade matches the palette exactly and stays crisp on mobile.
- **Grain-textured card edges + hairline gold borders** — Cards get a 1px translucent champagne hairline and a faint inner glow instead of heavy shadows, so the UI feels like thin gold-leaf framing rather than Material elevation.
  - How: `border:1px solid rgba(197,164,109,0.18); box-shadow: inset 0 1px 0 rgba(244,239,231,0.04), 0 20px 40px -24px rgba(0,0,0,0.7);` plus the shared grain ::before. Reserve a jade-tinted border for open-late/night states.
  - Fit: Replaces generic dark-card drop shadows with the quiet-luxury hairline detail; keeps boba spot cards feeling like magazine plates, and lets jade signal 'open late' without adding new UI chrome.
- **prefers-reduced-motion + reduced-transparency guards** — All glow/flicker/parallax motion disabled and grain opacity dialed down for users who opt out, so the after-dark aesthetic stays accessible.
  - How: `@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}` and optionally lower grain opacity / raise text contrast under `@media (prefers-contrast:more)`. Ensure pearl-on-obsidian body text hits WCAG AA (#F4EFE7 on #0B0C0E passes ~16:1).
  - Fit: Lets Boba Night keep the mood on capable devices while staying tasteful and accessible — the difference between a luxury brand and a gimmick site.

**Steal this**

- Overlay one champagne-tinted fractalNoise SVG at opacity ~0.10 over the entire obsidian page — single biggest upgrade, ~1KB, kills the flat-black cheapness instantly.
- Replace the flat background with 2–3 stacked radial gradients (champagne pool top-left, jade pool right) so the hero looks lit from within.
- Reserve orchid neon glow strictly for Featured cards/badges using a STATIC two-layer box-shadow — never animate shadows (mobile FPS) and never on body text.
- Fill the Fraunces hero headline with a pearlchampagne background-clip:text gradient plus a faint gold drop-shadow for a foil-stamped look.
- Use 1px rgba champagne hairline borders + inset glow instead of heavy drop shadows on spot cards; switch the hairline to jade to signal open-late.
- Ship a prefers-reduced-motion block that kills all glow/flicker and verify pearl #F4EFE7 on obsidian #0B0C0E stays WCAG AA.

**Sources**

- [Grainy Gradients — CSS-Tricks](https://css-tricks.com/grainy-gradients/) — Canonical feTurbulence-over-gradient technique with baseFrequency guidance and the contrast/brightness trick to sharpen grain.
- [Creating grainy backgrounds with CSS — ibelick](https://ibelick.com/blog/create-grainy-backgrounds-with-css) — Copy-paste inline data-URI SVG noise pseudo-element with exact opacity 0.12 / background-size 182px values, no external asset.
- [How to Create Neon Text With CSS — CSS-Tricks](https://css-tricks.com/how-to-create-neon-text-with-css/) — Exact layered text-shadow neon recipe plus real performance warnings (shadow animation tanks FPS on mobile) and prefers-reduced-motion guard.
- [After Dark: Night Color Palettes — Design Your Way](https://www.designyourway.net/blog/night-color-palettes/) — Real night palettes with hex codes showing deep base + warm gold metallic + jewel accent pairings that back Boba Night's obsidian/champagne/jade scheme.
- [nnnoise: Online SVG Noise Texture Generator — fffuel](https://www.fffuel.co/nnnoise/) — Free generator that outputs the exact optimized inline-SVG grain (tune frequency/opacity/color) so grain can be tinted champagne instead of gray.
- [SVG Filter Effects: Creating Texture with feTurbulence — Codrops](https://tympanus.net/codrops/2019/02/19/svg-filter-effects-creating-texture-with-feturbulence/) — Deep reference on fractalNoise vs turbulence, numOctaves, and stitchTiles for seamless tiling on large hero backgrounds.

## Page transitions & reveal galleries

The strongest, most tasteful wins for Boba Night are native and near-zero-JS: cross-document View Transitions to morph a shop's hero photo from the grid into its detail page, and CSS scroll-driven animations (animation-timeline: view()) for clip-path image reveals and staggered card entrances. Both are performant, mobile-friendly, degrade gracefully in unsupported browsers, and can be fully gated behind prefers-reduced-motion. Reserve heavier JS (GSAP/barba) only for a signature moment, not the whole site.

**Techniques**

- **Cross-document View Transitions (MPA)** — Native browser API that animates between two full page loads on the same origin with zero JS — you opt in with a single CSS rule and the browser crossfades the roots automatically.
  - How: Add `@view-transition { navigation: auto; }` to CSS on every page (Chrome/Edge 126+, Safari 18.2+; silently no-ops elsewhere). Customize the root crossfade via `::view-transition-old(root)` / `::view-transition-new(root)` keyframes. No build step, no library.
  - Fit: Turns navigation from the SoCal city grid into an individual boba-shop page into one continuous editorial gesture instead of a hard reload — reinforces the 'luxury magazine, not Yelp directory' feel the moment you tap through to a shop near Rowland Heights or Cypress.
- **Shared-element hero morph (view-transition-name)** — Give the same element on two pages an identical `view-transition-name` and the browser tweens its position, size and shape between them, so a shop's hero photo appears to fly from a grid card into the detail page's hero.
  - How: On the grid card image: `.card img { view-transition-name: shop-hero; }` and the detail hero: `.detail img { view-transition-name: shop-hero; }` — names must be unique per page. Works with cross-document transitions above, or with `document.startViewTransition(() => updateDOM())` for same-page filtering. Use `match-element` to auto-name repeated items.
  - Fit: The signature 'after dark' move: a champagne-framed boba photo physically travels from the listing into the shop page, keeping spatial context so you never lose your place — exactly the 'convey movement + maintain context' use case, and it reads as Airbnb/Spotify-grade polish.
- **Scroll-driven clip-path image reveal** — Images un-mask as they scroll into view — a rectangle wipes open (inset clip-path) tied to scroll position, not a timer, so it feels physical and never fires off-screen.
  - How: Pure CSS: `@keyframes reveal { from { opacity:0; clip-path: inset(45% 20% 45% 20%);} to { opacity:1; clip-path: inset(0 0 0 0);} }` then `.hero-img { animation: reveal linear both; animation-timeline: view(); animation-range: cover 0% cover 50%; }`. No JS, no IntersectionObserver.
  - Fit: Boba drink photography is the product — a slow inset wipe revealing a drink against obsidian #0B0C0E feels like a magazine plate turning, far more luxe than a plain fade, and the mask can echo the gold #C5A46D frame.
- **Staggered scroll-driven grid entrance** — Grid/list cards fade and rise in sequence as the grid enters the viewport, using entry/exit keyframe keywords so items animate both in and (optionally) out on scroll.
  - How: CSS only: `@keyframes animate-in { entry 0% { opacity:0; transform:translateY(100%);} entry 100% { opacity:1; transform:translateY(0);} }` and `.grid li { animation: animate-in linear both; animation-timeline: view(); }`. Add a small per-item `animation-range` offset (or nth-child delay) for the stagger.
  - Fit: The city/near-me results grid enters like a curated editorial spread rather than dumping a directory list — makes 'closest boba to me' results feel hand-picked, and it's GPU-cheap so it stays smooth on mid-range phones.
- **Custom root transition + reduced-motion gate** — Directional or radial page transitions (slide, or a circular clip-path wipe from the tap point) for a bespoke feel, always wrapped so motion-sensitive users get an instant cut.
  - How: For same-page: `document.startViewTransition()` then in `transition.ready` animate `::view-transition-new(root)` clipPath from `circle(0 at Xpx Ypx)` to full radius via the Web Animations API. Gate everything: `@media (prefers-reduced-motion: reduce){ ::view-transition-group(*),::view-transition-old(*),::view-transition-new(*){ animation-duration:.01ms !important; } }`.
  - Fit: A subtle upward slide between hub sections (Open Late, Date Night) gives a cohesive 'app-like' spine without a heavy SPA framework, and the reduced-motion gate keeps it accessible — non-negotiable for a tasteful brand.
- **GSAP ScrollTrigger reserved for one signature moment** — JS-driven scroll animation (SVG mask reveals, pinned scenes) — powerful but heavier; best used sparingly, not sitewide, given the native CSS options now cover most needs.
  - How: barba.js for SPA-style page transitions or GSAP+ScrollTrigger for an SVG-mask reveal; load only on the landing hero, lazy-import so it never blocks first paint. Prefer native View Transitions/scroll-timeline everywhere else.
  - Fit: Fine for a single hero flourish on the front page (e.g. a masked reveal of the 'after dark' skyline), but resist making it the whole site — the native techniques above deliver 90% of the effect at a fraction of the JS weight and mobile battery cost.

**Steal this**

- Add `@view-transition { navigation: auto; }` sitewide today — it's one line and instantly upgrades every SoCal cityshop navigation with a crossfade, doing nothing in browsers that don't support it.
- Tag each shop's hero photo with `view-transition-name: shop-hero` on both the results card and the detail page so the image morphs between them — the single most premium, low-effort win in this lane.
- Replace plain fade-ins on drink photography with a scroll-driven `clip-path: inset()` wipe via `animation-timeline: view()` — no JS, feels like a magazine reveal against the obsidian background.
- Give the near-me results grid a staggered `entry`-keyword scroll animation so results arrive like a curated spread, reinforcing 'not a Yelp directory'.
- Wrap ALL of it in `@media (prefers-reduced-motion: reduce)` collapsing animation-duration to ~0.01ms — required for the accessible, tasteful positioning.
- Keep GSAP/barba out of the critical path: use native View Transitions + CSS scroll-timeline for the site, and reserve any heavy JS scroll effect for a single lazy-loaded hero moment.

**Sources**

- [Smooth transitions with the View Transition API — Chrome for Developers](https://developer.chrome.com/docs/web-platform/view-transitions) — Confirms the one-line `@view-transition { navigation: auto; }` opt-in for cross-document MPA transitions and browser support (Chrome/Edge 126+, Safari 18.2+).
- [Using the View Transition API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using) — Exact syntax for view-transition-name shared-element morphs, ::view-transition-old/new keyframe customization, startViewTransition() JS, and prefers-reduced-motion gating.
- [Unleash the Power of Scroll-Driven Animations — CSS-Tricks](https://css-tricks.com/unleash-the-power-of-scroll-driven-animations/) — Concrete CSS for animation-timeline: view(), clip-path reveal keyframes, entry/exit staggered grid entrances, and @supports + reduced-motion fallback.
- [Some practical examples of view transitions to elevate your UI — Piccalilli](https://piccalil.li/blog/some-practical-examples-of-view-transitions-to-elevate-your-ui/) — Frames the tasteful, restrained use cases (draw attention, convey movement, maintain context) and the gallery-to-detail photo morph pattern; warns against overuse.

## Open-source snippet sources

The best tasteful upgrades for Boba Night come from three real sources: Aceternity UI for a handful of restrained dark-mode React/Framer Motion effects (Spotlight, Focus Cards, Bento Grid, Apple Cards Carousel), Codrops for scroll-driven grid choreography (HoverGrid, Sticky Grid Scroll), and native CSS scroll-driven animations plus Animista keyframes for zero-JS, mobile-safe reveals. Lean on native CSS and pure-CSS snippets for performance and accessibility; reserve one or two Framer Motion pieces for the hero and featured rail so the site reads editorial-luxury, not gimmicky.

**Techniques**

- **Spotlight / Lamp hero glow** — A soft radial spotlight (Aceternity 'Spotlight' and 'Lamp Effect') that sweeps a single beam of light across a dark hero, drawing the eye to the headline. Built to sit on near-black backgrounds.
  - How: Aceternity UI Spotlight component (Tailwind + Framer Motion) at ui.aceternity.com/components/spotlight. If you want zero JS, replicate with a single absolutely-positioned div using a CSS radial-gradient in champagne at ~8% opacity plus a slow @keyframes translate — no library needed.
  - Fit: Gives the obsidian #0B0C0E hero an 'after dark' pool of champagne #C5A46D light behind the Fraunces headline — the luxury-magazine cover feel, not a Yelp banner. Use gold for the beam; swap to orchid only on the featured/hero variant.
- **Focus Cards (blur siblings on hover)** — Aceternity 'Focus Cards': hovering one card brings it into sharp focus while the sibling cards dim and blur, isolating the choice. Also their 'Card Hover Effect' slides a highlight to the hovered card.
  - How: Aceternity Focus Cards component (Tailwind + Framer Motion). Pure-CSS fallback: on the grid's :has(:hover) state, apply filter: blur(2px) brightness(.6) to all cards, and reset the hovered one — one CSS rule, no JS.
  - Fit: Perfect for the boba-shop card grid: pointing to one spot at a time feels curated and editorial. On mobile (no hover) fall back to a scroll-snap rail so nothing breaks.
- **Bento Grid + Apple Cards Carousel** — Bento Grid is an asymmetric magazine-style tile layout (varied cell sizes); Apple Cards Carousel is the minimal, snap-scrolling horizontal card rail seen on apple.com.
  - How: Aceternity 'Bento Grid' and 'Apple Cards Carousel' components (Tailwind + Framer Motion). The carousel maps cleanly to native CSS scroll-snap (scroll-snap-type: x mandatory) for a lightweight mobile version.
  - Fit: Bento layout gives the front page the Airbnb/Spotify 'featured collections' rhythm instead of a uniform directory grid. The Apple carousel is ideal for a 'Featured tonight' or 'Open late near you' rail — thumb-swipeable, snappy, premium.
- **Native CSS scroll-driven reveals (animation-timeline: view())** — Elements fade/slide/scale in as they enter the viewport using the browser's own scroll timeline — no IntersectionObserver, no JS library. Now baseline in Chrome/Edge/Safari with graceful fallback.
  - How: Pure CSS: @keyframes reveal { from { opacity:0; transform: translateY(24px) } } then animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% cover 40%. Docs: MDN Scroll-driven_animations and developer.chrome.com/docs/css-ui/scroll-driven-animations. Wrap in @supports and @media (prefers-reduced-motion: no-preference).
  - Fit: Zero-JS section reveals as you scroll the boba listings keep the site fast on phones and fully accessible (honors reduced-motion). Cheapest possible way to add the 'considered, unfolding editorial' feel.
- **Codrops HoverGrid / Sticky Grid Scroll** — HoverGrid: grid tiles reveal underlying media/title on hover (Metalab-inspired), vanilla HTML/CSS/JS, no GSAP. Sticky Grid Scroll: a position:sticky grid that animates cells as you scroll through a pinned section.
  - How: Open-source repos: github.com/codrops/HoverGrid (vanilla JS) and the Sticky Grid Scroll tutorial at tympanus.net/codrops. MIT-style Codrops license, copy the css/ and js/ folders directly.
  - Fit: HoverGrid on the shop tiles reveals a photo + neighborhood label on hover for the desktop 'discovery wall'. Sticky Grid Scroll can pin a 'Tonight in Rowland Heights / Cypress' section while cards animate — a signature editorial moment without a heavy framework.
- **Animista text reveals + Uiverse glass chips** — Animista generates pure-CSS keyframe animations (tracking-in-expand, focus-in, text-shadow-drop, slide-in) you tune and copy. Uiverse is a huge open-source library of CSS/Tailwind buttons, glassmorphism cards and hover effects.
  - How: animista.net — tweak duration/easing, copy the generated keyframes (FreeBSD licensed, no runtime). uiverse.io — filter by glassmorphism/dark, copy CSS or Tailwind for buttons and city/filter chips.
  - Fit: tracking-in-expand on the Fraunces hero headline gives a slow, letter-spacing 'develop-in' that feels like a title card. Uiverse frosted-glass chips suit the SoCal city filters (Rowland Heights, Cypress) — subtle pearl-on-obsidian glass, gold on active. Keep animations under ~600ms and gate behind prefers-reduced-motion.

**Steal this**

- Hero: obsidian background + single champagne radial-gradient spotlight (Aceternity Spotlight, or a CSS-only radial-gradient div) behind a Fraunces headline that plays Animista tracking-in-expand once on load.
- Shop grid: :has(:hover) focus-blur so hovering one card dims and blurs the rest (Aceternity Focus Cards behavior, achievable in ~5 lines of pure CSS).
- 'Open late near you' / city rail: Apple Cards Carousel look via native CSS scroll-snap (scroll-snap-type: x mandatory) — thumb-swipeable on mobile, no JS.
- Section entrances: native CSS animation-timeline: view() reveals (fade + 24px rise) wrapped in @supports and prefers-reduced-motion — zero JS, fast on phones.
- Featured collections: Aceternity Bento Grid asymmetric tiles to break the uniform-directory look; reserve orchid #b46bd6 only for the one 'featured' tile.
- City filter chips (Rowland Heights, Cypress): Uiverse frosted-glass chips, pearl text on obsidian, gold border/fill on the active city.

**Sources**

- [Aceternity UI — Effects components](https://ui.aceternity.com/categories/effects) — Verified list of dark-friendly Framer Motion effects (Spotlight/Lamp, Aurora, Background Beams, Sparkles, Parallax Scroll, Tracing Beam) — copy-paste React + Tailwind.
- [Aceternity UI — Components (Focus Cards, Bento Grid, Apple Cards Carousel, Card Hover, Glare Card)](https://ui.aceternity.com/components) — Source of the Focus Cards blur-siblings effect, Bento Grid, and the apple.com-style carousel — the core tasteful card interactions for the boba grid.
- [Codrops — HoverGrid (GitHub repo)](https://github.com/codrops/HoverGrid) — Open-source vanilla HTML/CSS/JS grid-item reveal-on-hover (Metalab-inspired) — no framework, drop-in css/ and js/ for the desktop discovery wall.
- [Codrops — Sticky Grid Scroll tutorial](https://tympanus.net/codrops/2026/03/02/sticky-grid-scroll-building-a-scroll-driven-animated-grid/) — Technique for a position:sticky, scroll-driven animated grid — a signature pinned 'Tonight in [city]' editorial section.
- [MDN — CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Authoritative reference for native animation-timeline: view() reveals — zero-JS, accessible, the performant way to animate sections on scroll.
- [Animista — on-demand pure-CSS animation generator](https://animista.net/play/text/focus-in) — Generates copy-paste, runtime-free CSS keyframes (tracking-in-expand, focus-in) under a FreeBSD license — ideal for the Fraunces headline reveal.

## Gamified / addictive discovery loops

The strongest, non-dark-pattern loops for a boba explorer are collection/passport mechanics (a "Boba Passport" of shops you've tried) and card-by-card reveal (a Wrapped-style progressive disclosure that turns your visits into a shareable story). Pair these with a gentle weekly-not-daily cadence and positive, never-shaming framing so returning feels like self-expression, not a chore. All of it can be built with lightweight CSS scroll-snap, IntersectionObserver, and Framer Motion / Web Animations — no heavy game engine, fully mobile-first.

**Techniques**

- **Boba Passport (collection / stamp book)** — A visual grid of shops you've visited, each 'stamped' when checked in. Uncollected slots show as elegant embossed silhouettes; collected ones fill with the shop's color/logo. Progress reads like a luxury travel passport, not a Yelp check-in list.
  - How: CSS grid of cards with a filled/unfilled state; store visited IDs in Supabase (you already have city data — add a user_visits table). Animate the stamp on collect with Framer Motion (scale + rotate 'thunk') or the Web Animations API. Empty slots use a subtle inset box-shadow in champagne over obsidian.
  - Fit: Turns Boba Night from a lookup tool into a personal SoCal boba map you fill in. A pearl-on-obsidian passport with gold foil stamps matches the luxury-magazine brand exactly, and gives a concrete reason to return after each shop.
- **Wrapped-style reveal (progressive disclosure)** — A monthly or seasonal 'Your Boba, Wrapped' — full-screen cards revealed one swipe at a time: shops visited, most-ordered drink, a new neighborhood you unlocked, ending on a screenshot-ready summary card.
  - How: CSS scroll-snap (scroll-snap-type: y mandatory) or a swipe carousel; IntersectionObserver to trigger each card's entrance animation once. Generate the final share card client-side with html-to-image / the Canvas API sized to 1080x1920 for Instagram Stories.
  - Fit: Reframes raw data as narrative ('You found yourself in 7 SoCal boba shops this summer') in Fraunces display type over obsidian. The share card is free viral distribution and reads as identity, not a directory export.
- **Nearby reveal / 'shake for a pick'** — A single tasteful surprise mechanic: given the user's city (Rowland Heights, Cypress), reveal one nearby recommendation with a flip or curtain animation instead of a list dump. Optional re-roll.
  - How: CSS 3D flip (transform: rotateY, backface-visibility: hidden) or a mask-reveal wipe; pull nearest shop by city/geo from your Supabase finder endpoint. Cap re-rolls to keep it feeling curated, not slot-machine.
  - Fit: Directly serves the project's core goal (find boba closest to me) but delivers it as a delightful reveal rather than a Yelp results page — a single orchid-accented 'featured pick' card fits the after-dark editorial mood.
- **Gentle weekly cadence + streak freeze** — A soft 'boba weeks' streak counting weeks you visited any shop, not days — with a built-in freeze so a missed week never resets to zero. Framing is always celebratory ('4 of your last 5 weeks — a true connoisseur').
  - How: Compute streak from visit timestamps server-side in Supabase; render a small week-dot row. Never use loss-aversion guilt copy; use positive-progress strings. Weekly (Peloton-style) cadence avoids the daily-pressure dark pattern.
  - Fit: Boba is a weekly-treat behavior, so a daily streak would feel coercive and off-brand. A quiet, non-shaming weekly ribbon keeps people coming back to the site without cheapening the luxury tone.
- **Neighborhood unlock map** — SoCal regions (San Gabriel Valley, OC, Rowland Heights, Cypress) start dimmed and 'light up' in champagne/jade as you log a shop there — a personal map of territory explored.
  - How: Inline SVG map of SoCal sub-regions with per-path fill transitions on unlock; drive state from visited-city aggregates in Supabase. Animate the fill with a CSS transition on the path's fill/opacity.
  - Fit: Gives exploration a spatial reward and visual payoff on the front page that no competitor directory offers, while leaning on the city data you already have. Reads as an editorial cartographic centerpiece, not a pin-cluttered Google Map.
- **Taste passport onboarding (endowed progress)** — A quick swipe-to-rate intro (Stitch Fix Style Shuffle style): a few 'this or that' boba cards that seed personalization and instantly show the profile as ~30% complete.
  - How: Swipeable card stack (Framer Motion drag, or a lightweight Tinder-card lib) writing preference tags to Supabase; show a pre-filled progress ring to trigger the endowed-progress effect so users finish.
  - Fit: Collects taste data to power 'closest + best match for you' picks while feeling like a game, not a form. Keeping it to 4-5 cards keeps it fast and mobile-friendly, and the drag interaction feels premium rather than survey-like.

**Steal this**

- Reveal, don't dump: replace any results list with card-by-card progressive disclosure (scroll-snap + IntersectionObserver) so finding boba feels like unwrapping, not searching.
- Build the share card at 1080x1920 from the start — every Wrapped/passport summary should export a Fraunces-on-obsidian image ready for Instagram Stories in one tap.
- Frame stats as identity, not numbers: 'You found yourself in 7 SoCal shops' beats '7 visits'; write the milestone copy in the brand's editorial voice.
- Cadence is weekly with a freeze, never daily — boba is a treat, so avoid streak guilt and use only celebratory, never-shaming copy (positive progress, no confirmshaming).
- Empty states are the hook: render unvisited passport slots as elegant embossed gold silhouettes so the incomplete collection itself pulls the user back.
- Cap the re-roll on any 'surprise pick' so it reads as curation, not a slot machine — one tasteful reveal with a limited re-roll, not infinite spins.

**Sources**

- [What UX Designers Can Learn From Spotify Wrapped](https://uxplaybook.org/articles/spotify-wrapped-ux-design-lessons) — Concrete Wrapped mechanics: card-by-card progressive disclosure, narrative framing over raw numbers, screenshot-optimized share cards, gamification that amplifies existing behavior.
- [How to design an effective streak (Make It Tools)](https://www.makeit.tools/blogs/how-to-design-an-effective-streak-2) — Streak freeze, weekly-not-daily cadence (Peloton), decoupling rewards from streak continuity, milestone animations that lifted 7-day retention +1.7%.
- [The Psychology of Hot Streak Game Design Without Shame (UX Magazine)](https://uxmag.com/articles/the-psychology-of-hot-streak-game-design-how-to-keep-players-coming-back-every-day-without-shame) — Anti-dark-pattern rules: positive framing over confirmshaming, grace periods, earn-back over pay-to-recover, transparent rules and user autonomy.
- [Letterboxd and the Gamification of Movie-Watching (Flasz On Film)](https://flaszonfilm.com/2023/01/11/letterboxd-and-the-gamification-of-movie-watching/) — Shows how visible collection counts, best-of lists, and Year-in-Review drive social status and completionism — and warns where competitive consumption goes too far.
- [10 App Gamification Ideas (StriveCloud)](https://www.strivecloud.io/blog/app-gamification-ideas-dc300) — Implementation patterns for collections/stamps, passport/progress systems, surprise reveals, and Style-Shuffle-style preference gathering via the endowed-progress effect.
