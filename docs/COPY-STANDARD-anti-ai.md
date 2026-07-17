# Boba Night — Copy Standard (anti-AI-tells)

Binding writing standard for every visible string on the site: pages, CTAs,
links, cards, modals, tooltips, empty states, FAQ answers, meta descriptions,
schema descriptions, aria-labels. Adapted from the CoverCapy anti-AI rules
(the dental specifics don't apply; the tell-killing mechanics do). This SITS
ON TOP OF the existing Boba Night voice (psychic-free, editorial, honest) and
the CLAUDE.md banned list. Where a generic copywriting habit conflicts, this
file wins.

Goal: sound like a person who actually knows SoCal boba explaining it plainly.
Not a brochure, not a pitch deck, not an AI landing page.

## Nonnegotiable mechanics

1. **No decorative arrows in visible copy.** Not `->`, `→`, `➜`, `⟶`, or a
   chevron glued to link text. A functional chevron inside a real control
   (dropdown, carousel, accordion marker) is fine. CTAs and links carry none.
   Wrong: "Enter the directory →". Right: "Enter the directory".

2. **No em dash as a sentence separator.** Rewrite as two sentences or a
   comma. (The `—` char shows up constantly in AI copy; it's a top tell.)
   Wrong: "334 shops, menus checked — nothing invented." Right: "334 shops.
   Menus checked against official sources. Nothing invented."

3. **No unnecessary hyphens** when open wording is natural. Keep only the real
   ones (open-late as an established phrase, in-network-style compounds, URLs,
   proper names). Prefer "open late" as two words in prose where it reads clean.

4. **No synthetic three-part rhythm.** Don't force every line into a triplet
   ("clear, honest, and fresh"). Triplets are fine when the three things are
   genuinely a set (annual list: name, city, area).

5. **No empty contrast formulas.** Ban these shapes: "It's not X, it's Y",
   "Not just X but Y", "More than X", "From X to Y", "Whether you're X or Y",
   "In a world where", "When it comes to", "At the end of the day", "Now more
   than ever", "The future of", "This is where X comes in".

6. **No fragment-stacking for drama.** "Your night. Your shop. Your pour."
   is out. One fragment in a headline is fine; don't make it the page rhythm.

7. **No filler intros.** Delete "It's worth noting", "It's important to",
   "At Boba Night we believe", "Our mission is", "We're proud to", "We
   understand that". Start with the useful fact.

8. **No invented facts.** No made-up ratings, review counts, hours, prices,
   crowd numbers, or "voted best". This is already the brand's core. Estimates
   are labeled; unverified is "Verifying".

## Banned words (public copy)

The CLAUDE.md list stays: hidden gem, nestled, vibrant, indulge, premium,
curated, discover, transform, seamless, elevate, empower, navigate,
innovative, look no further, burst of flavor.

Add the AI-corporate tells: unlock, leverage, revolutionary, cutting edge,
state of the art, comprehensive, frictionless, hassle free, stress free,
peace of mind, one stop shop, we've got you covered, game changer, world
class, best in class, robust, dynamic solution, tailored solution, embark,
journey (as in "boba journey"), ecosystem, "take your X to the next level",
"experience the difference".

Watchlist (use only when specific and true): concierge (part of the site's
voice — don't repeat it every section), exquisite, curator, effortless,
elevate, simple, easy, smarter, expert, trusted, best, top. "Best" lists are
allowed because they're labeled opinions with a shown method — that's the
existing honesty rule, keep it.

## CTAs and links

- Verb + object, 2 to 5 words, sentence case, no ending punctuation, no arrow,
  no all caps, no false urgency.
- Good: "Find a shop", "Browse the 626", "See open-late spots", "Spin the
  roulette", "Save to your list", "Claim this listing".
- Bad: "Get started", "Explore more", "Learn more", "Discover shops",
  "Begin your journey", "Take control".
- Link text names the destination. Not "click here" / "read more".

## Voice reference

Write like someone who has actually driven SGV at 11pm looking for a shop
that's still pouring. Specific over grand. "Still open past 10 in Rowland
Heights" beats "your late-night boba destination". Name cities, streets,
what to order, what's verified and what isn't. Honesty is the differentiator,
so say plainly what you don't know ("Hours verifying") instead of dressing it up.

## Self-check before shipping copy

Arrow scan · em-dash scan · banned-word scan · CTA-specificity scan · invented-
fact scan. If a sentence could sit unchanged on any generic startup site,
rewrite it. Run `python3 build/copy_audit.py` to catch the mechanical tells.
