# 00 - Current Luxury Gap Audit

Honest read of the "Craving Arcade" homepage this rebuild replaces. It was better than the original but not a luxury product.

## 1. Current visual direction
Night-ink background with neon accents (pool blue, acid lime, tangerine, ultraviolet, cherry pink), Space Grotesk display, pill controls, bordered cards, an illustrated SVG cup as the hero. Reads as arcade / sportswear / tech product, not tea salon.

## 2. Why it still feels inexpensive
Saturated neon signals play, not restraint. Space Grotesk + pill buttons read as a SaaS component kit. Zero photography, so appetite is never triggered. Everything sits in a rounded rectangle. Copy explains mechanics ("Move the pearl, choose the mood") instead of selling the outcome.

## 3. Where it looks like a startup UI kit
Segmented toggles, chip rows, "Surprise me" buttons, bordered result cards, and a stat-y directory grid.

## 4. Too many containers / pills / borders / buttons
The hero alone stacked a select, a pad, a segmented control, a preset dropdown, a neon button, and a result card; then chip rows for vibe/landmark/city and a 48-card grid.

## 5. Lacking photography / sensory imagery
The standalone homepage had zero `<img>`. The only "image" was a cartoon cup. No liquid, condensation, steam, pearls, rooms, or hands.

## 6. Interactions worth preserving
Taste-matching logic (creamy / tea-forward axes + adventurousness); save + share; server-rendered crawlable content and the static generator; the two-drink comparison.

## 7. Interactions to rename and redesign
Craving Cup -> Tea Concierge. Spin the Straw -> House Choice (envelope reveal, no wheel). Boba Battle -> Tasting Flight (no winner counts). Menu Drop Radar -> The New Pour (magazine, dated). Taste Passport -> The Black Book (no badges). Crawl builder -> An Evening in...

## 8. Modules to delete
The neon arcade hero, the tools strip as presented, the on-page 48-of-321 grid, and all pill/chip walls.

## 9. Belongs on a separate directory page
The full 321-shop searchable grid. Already moved to /directory/; the homepage keeps a restrained entry point.

## 10. CSS / JS to refactor
Was one monolithic file with inline CSS, a giant inline shop array, and inline scripts. Now css/luxury-homepage.css plus js/homepage/*.js modules; the shop array is off the homepage; drink data is a small society-data.js.

## 11. Which claims and menu data are properly sourced
Sourced first-party: 7 Leaves, Sharetea, Kung Fu Tea, Tastea, plus Chatime and CoCo (added this pass). Caffeine/dairy only where the menu states it. No ratings, prices, hours, or wait times anywhere. See data/research/source-ledger.csv.

## 12. Prior-build tasks still incomplete
The prior summary admitted research, screenshot review, asset plan, full menu research (target 15/75), mega-nav, and several modules were unfinished. This pass completes the homepage rebuild, docs, mega-nav, and modules; menu breadth reaches 6 chains / 66 drinks (short of 15/75; see docs 05 and 12).

## 13. SEO routes that must stay stable
/, /directory/, /boba/ca/{city}/{shop}/, /area/{region}/, /best/{slug}/, /near/{slug}/, /cities/, /tools/{slug}/, sitemap.xml, robots.txt. All preserved; the homepage links into them with normal anchors.

## 14. What mobile gets wrong today
Scrolling chip rows, miniature cards, a hero that pushes the first real recommendation down, hover affordances, no image-crop discipline.

## 15. Decisions that create a genuine luxury result
Obsidian lacquer alternating with porcelain relief; jade / garnet / aubergine as controlled color; champagne as a thin accent only; Fraunces used sparingly with Inter; one signature art-directed "Pour" instead of a cartoon cup; content forms beyond the card; a hosted-evening section order; a concierge-index mega-nav.
