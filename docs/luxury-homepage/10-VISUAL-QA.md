# 10 - Visual QA

## Screenshot status (honest)
This environment has no browser-rendering or headless-screenshot tool available, so live screenshots of the built page could not be captured here; docs/luxury-homepage/screenshots/ is intentionally empty rather than filled with fabricated images. The screenshot-and-critique loop is therefore completed as a structured reasoning review of the built markup and CSS at each target breakpoint, plus the Ruthless Luxury Critic pass below. The one gate that requires a real browser (a human-eye screenshot review at 320/375/390/430/768/1024/1440/1728) is flagged for the person to run; the build was written to satisfy it, and every code-verifiable check passed (doc 11).

## Per-breakpoint reasoning
- **320 to 430 (mobile):** single column. Arrival stacks: headline, sub, CTAs, then the Pour plate with the Tonight's Selection note floating over its lower edge (note--float uses negative margin, not absolute, so it never overlaps text). Concierge option cards drop to a 1 to 2 column auto-fit grid at minmax(150px). Sheet rows collapse side/actions beneath the title. City splits and flight columns stack. All buttons >=44px. No horizontal scroll (overflow-x hidden; no fixed-width rows).
- **768 to 860 (tablet):** city rows and sheet rows go two-up; flight becomes three columns; mega-nav is still the drawer until 1040.
- **1000:** arrival becomes two columns (copy | media) with the note absolutely placed on the media's lower-left.
- **1040+:** desktop mega-nav appears; hover and focus open panels.
- **1240 max:** content is capped; generous side padding.

## Critique checklist (self-review of the built page)
- Feels expensive: yes - obsidian/porcelain rhythm, one signature, restrained type.
- Creates appetite: partially - the render and copy do work; real macro photography (doc 09) will raise this further. Honest limitation.
- Hospitality over software: yes - concierge note, menu sheet, no dashboards or chip walls.
- Too much UI chrome: no - controls are minimal and mostly text/hairline.
- Photography strong enough: not yet - placeholders are art-directed but are not photography; see doc 09.
- Typography disciplined: yes - Fraunces sparingly, Inter for text, tracked labels.
- Too many cards: no - varied content forms.
- Composition varied: yes - split, sheet, columns, full-bleed, magazine, notebook.
- Recommendation clear: yes - Tonight's Selection is immediate and real.
- Mobile genuinely polished: yes by construction; pending the human screenshot pass.
- Fast: yes - two fonts, one CSS, small JS, no images, no framework.
- Every section necessary: yes - each maps to a step in the hosted-evening journey.

## Revision made after this review
The first construction left scroll-reveal sections at opacity 0 with reveal driven by JS, which would blank the page without JS. Revised so reveal is gated behind a `js` class: content is fully visible without JS and only animates when JS runs (and never under reduced motion). Small tap targets were raised to 44px. The one en-dash UI glyph was replaced with a math minus.
