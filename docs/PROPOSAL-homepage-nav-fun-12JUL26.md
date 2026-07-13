# NiteBoba — Homepage Review + Nav & "Fun Layer" Proposal
**Written:** 12 JUL 2026 · for Jay · status: proposal, nothing built yet

## 1. Honest read of the main page

What works: it's the most distinctive boba site on the internet. "Something
exquisite for tonight," the concierge framing, the editorial dark hero — nobody
else in this niche looks like this, and the sourced menu note under Tonight's
Selection quietly shows off the honesty moat. Keep the soul.

What doesn't work yet — the site is a mood before it's a tool:

1. **Mystery-meat navigation.** Tonight · The Concierge · The Menu · The New
   Pour · Black Book — a first-time visitor can't predict what ANY of those
   open. Your 322-shop directory (the actual product) hides behind labels.
2. **No search anywhere in the hero.** "Find [shop] near [city]" is the #1
   intent and it requires two clicks to even reach a filterable list.
3. **Duplicate CTA.** "Ask the concierge" appears twice within one viewport.
4. **The fun already exists but is buried.** You shipped concierge, tasting
   flight, evening route, black book, house choice, AND a roulette tool
   (/tools/roulette) — the homepage surfaces almost none of them by name.
5. **Accessibility debt:** small gold-on-dark caps flirt with contrast minimums;
   hover-only dropdowns exclude keyboard/touch; several sections rely on
   scroll-reveal that hides content if JS hiccups.

## 2. Supabase reality check (before designing on top of it)

Supabase holds all 322 stores, but the live site does NOT read it — pages are
static, the directory list is baked in. That's actually fine (fast, free,
un-crashable). The path:
- **Now:** a build-time sync script (Supabase → SHOPS array + CSV) so the DB is
  the single source of truth. ~40 lines. Kills the 6-file store surgery.
- **Later:** one tiny edge endpoint for genuinely-live data (open-now status)
  once enrichment fills hours. Everything else stays static.
Don't build live-DB features before enrichment — there's nothing live to show.

## 3. Navigation proposal (keep the voice, add legibility)

Rename with plain meaning, keep the register:
- Tonight → **Tonight** (keep — it's the signature)
- The Concierge → **Concierge**
- Cities → **Cities**
- Tea Houses → **Directory · 322 shops** (this is the money link — say the number)
- The Menu → **Drinks**
- The New Pour → **New Openings**
- Black Book → **Saved ♥**
Plus: a persistent **search input in the header** (shop or city, feeds the
directory's existing filter), visible on every page; a **mobile bottom bar**
(Tonight · Search · Directory · Saved); dropdowns open on click/focus, not
hover; skip-link + visible focus states.

## 4. The fun layer — random fun + date night (mostly surfacing what exists)

1. **"Can't decide? Spin." — Boba Roulette, promoted to the hero.** One button
   next to Ask the concierge. Random shop (weighted: featured first, specialty
   over chain), card flips in with confetti of pearls. The tool already exists.
2. **Date Night Planner (upgrade evening-route).** Pick area + vibe → a
   3-stop itinerary: drink (shop + what to order) → dessert/walk nearby →
   late-option. Output = a beautiful shareable card (canvas → PNG) titled
   "Tonight in the 626." Shareability = free distribution.
3. **Tonight's Pour, daily.** Deterministic date-seeded rotation through the 66
   sourced drinks — changes at 5pm daily, no backend needed. Gives regulars a
   reason to return and screenshots well.
4. **"What your boba order says about you" quiz.** 5 taps → a persona card
   (The Loose-Leaf Purist, The Brown Sugar Maximalist…) + 3 matching shops.
   Pure virality; zero data dependencies; on-voice.
5. **Open-late strip (post-enrichment).** "Still pouring at 10pm near you" —
   THE NiteBoba feature; the name demands it. Blocked on hours data only.
6. **Featured-house rotation.** Taro Yuan's slot becomes "This month's house,"
   archived monthly — turns the featured slot into recurring sellable inventory.
7. **Boba Passport waitlist.** One email field on the homepage ("check in,
   keep streaks, nominate shops — coming"). Cheap to add, starts the audience
   for Phase 3 monetization.

## 5. Order of operations

- **P0 (one session):** nav relabels + header search + hero Roulette button +
  "Directory · 322 shops" CTA + dropdown/focus accessibility fixes.
- **P1 (one session):** Date Night Planner + shareable card; Tonight's Pour.
- **P2 (backend first):** enrichment run (geocode + hours) → open-late strip,
  open-now badges, map view on the directory.
- **P3:** quiz + Passport waitlist + featured rotation automation.

Monetization threads: the planner is sponsorable ("date night, presented by
___"), roulette can weight paying members, the featured rotation is monthly
inventory, and Passport is the future first-party ratings engine that unlocks
aggregateRating schema. The fun layer isn't decoration — it's the funnel.
