# Community & Recurring-Event Virality — Turning a Directory into a Hub

Research for Boba Night. The directory today answers *"where is good boba?"* This doc is about the next layer: making 334 shops feel like **334 potential meeting places** — recurring boba meetups, "third place" venue badges, a submit-your-event flow, and shareable cards that let a member's own social feed do our marketing. The lesson from run-club and Strava culture: a directory becomes a community hub when it (a) makes *showing up* frictionless and *recurring*, (b) gives people an **identity object to share**, and (c) treats every share as free distribution.

Palette contract this doc assumes: obsidian `#0B0C0E`, pearl `#F4EFE7` text, champagne `#C5A46D` hairlines/eyebrows, ONE neon hot-pink `#ff3f6f` glow per viewport, Fraunces (serif display) + Inter (UI), letterspaced eyebrows, 1px hairline borders, film grain, 2px radii. Static vanilla-JS multi-page site; CSS-first, transform/opacity only, `prefers-reduced-motion` honored. Honesty brand: no fake ratings, no fake attendance numbers.

---

## Sources studied

- **November Project — city pages (Boston, NYC, Richmond)** — november-project.com. The canonical grassroots run-club model. Every city page is built on a *fixed weekly rhythm* ("Mondays / Wednesdays / Fridays, 6:30am") with consistent locations, and hard practical detail (GPS coords, parking, a noise-ordinance note) that removes every excuse not to show up. Belonging is manufactured with **inside language** ("Show Up!", "the tribe", founders on a first-name basis, the "black ace = 14 pushups" ritual) and an origin myth ("this is where the movement was born"). Free, recurring, imperative-voice CTAs. This is the blueprint for a boba-meetup layer.
- **Strava — clubs, segments, shareable activity cards** — strava.com + NoGood teardown (nogood.io/blog/strava-marketing-strategy). The definitive "product mechanics = distribution" case. Strava shipped transparent route-map overlays *because users were already screenshotting them for Instagram* — they made the share asset native. "If it's not on Strava, it didn't happen." Group activities get **95–121% more kudos** than solo ones; leaderboards / Local Legend create recurring reasons to return. Takeaway: build the shareable artifact *and* the club infrastructure before any campaign.
- **Strava Group Events / Club Posts docs** — support.strava.com. Concrete IA for how a club schedules a recurring meetup: title, day/time, location pin, "I'm in" RSVP, and a post feed. A minimal, copyable schema for a boba-meetup object.
- **UIUX Trend — "Submit Your Event" pattern** — uiuxtrend.com/submit-your-event. Community-submission UX: **consent stated up front** ("by submitting you consent to store & display if approved"), explicit editorial discretion ("we reserve the right to approve/reject"), moderation-gated publishing. The honest-directory way to accept user events without letting spam onto the site.
- **AddEvent — recurring-rule generator + Add-to-Calendar** — addevent.com/blog/whats-the-recurring-rule-generator. Recurrence expressed as the **iCal RRULE** standard (`FREQ=WEEKLY;INTERVAL=1;BYDAY=TU`), rendered to humans as "every Tuesday." Add-to-Calendar links that hit Google/Apple/Outlook/Yahoo. The correct data spine for "every Tuesday, 7pm" boba nights.
- **Ben Kaiser — "Sharing Images using the Web Share API"** — benkaiser.dev. The exact client-side recipe: draw a card to `<canvas>`, `toDataURL()` → `fetch()` → `blob()` → `new File()`, feature-detect with `navigator.canShare({files})`, then `navigator.share()`. Native share sheet on mobile with zero backend — perfect for a static site.
- **MDN — Web Share API / `navigator.share` / `canShare`** — developer.mozilla.org. Spec confirmation: `share()` must be triggered by a user gesture, resolves a Promise, and file sharing is gated behind `canShare({files})`. Graceful degradation to copy-link.
- **Vercel — OG Image Generation (Satori)** — vercel.com/docs/og-image-generation + knaap.dev "Dynamic OG images with any static site generator." How dynamic social-preview images are generated from HTML/CSS. For a *static* site the reusable idea is **pre-render one OG image per shop/event at build time** (or a shared branded template) so every link unfurls as a designed card, not a bare URL.

---

## Hot moves

### 1. The recurring-meetup object ("every Tuesday, 7pm")
**Where seen:** November Project's fixed weekly grid; Strava Group Events; AddEvent RRULE.
**Why it works:** Recurrence is the engine of community. A one-off event is an errand; "every Tuesday" is a *habit and an identity*. A stable cadence means a member can plan their week around it and bring a friend next time — the compounding loop that built November Project from two guys to a global tribe. Store the truth as an RRULE, render it in human words.
**Snippet:**
```html
<article class="meetup" itemscope itemtype="https://schema.org/Event">
  <p class="meetup__cadence" data-rrule="FREQ=WEEKLY;BYDAY=TU">
    <span class="eyebrow">Recurring</span> Every Tuesday · 7:00pm
  </p>
  <h3 itemprop="name">Taro Tuesdays @ Boba Guys DTLA</h3>
  <p class="meetup__where" itemprop="location">Boba Guys, 333 S Alameda</p>
  <a class="meetup__ics" href="/events/taro-tuesdays.ics">Add to calendar</a>
</article>
```
```js
// RRULE → human string (tiny, no lib)
const DAYS={SU:'Sunday',MO:'Monday',TU:'Tuesday',WE:'Wednesday',
  TH:'Thursday',FR:'Friday',SA:'Saturday'};
function rruleToText(r){
  const m=Object.fromEntries(r.split(';').map(p=>p.split('=')));
  if(m.FREQ==='WEEKLY'&&m.BYDAY) return 'Every '+
    m.BYDAY.split(',').map(d=>DAYS[d]).join(' & ');
  return 'Recurring';
}
```
**Impact:** H · **Effort:** Med (needs an events data file + a static `.ics` per event; schema markup is free SEO).

### 2. Client-side shareable card via canvas + Web Share API
**Where seen:** Strava's native route-map share asset; Ben Kaiser's canvas recipe; MDN `canShare`.
**Why it works:** This is the single highest-leverage virality move for a static site. A member taps "Share this shop / I'm going" → we draw a branded obsidian card (shop name in Fraunces, champagne hairline, the one pink glow) to `<canvas>` and hand it to the OS share sheet as a real PNG file. No backend, no login. Their Instagram story *is* our billboard — exactly Strava's "make the thing people already screenshot native."
**Snippet:**
```js
async function shareShopCard(canvas, shopName){
  const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
  const file = new File([blob], 'bobanight.png', {type:'image/png'});
  const data = {files:[file], title:shopName,
    text:`${shopName} · found on Boba Night`, url:location.href};
  if (navigator.canShare && navigator.canShare({files:[file]})) {
    try { await navigator.share(data); } catch(e){ /* user cancelled */ }
  } else {
    await navigator.clipboard.writeText(location.href); // desktop fallback
    toast('Link copied');
  }
}
// must be called from a click handler (user-gesture requirement)
```
**Impact:** H · **Effort:** Med (canvas drawing routine + a share button). Draw with `fillText`/`roundRect`; load Fraunces via `document.fonts.ready` before drawing.

### 3. Per-shop "third place" badge (earned language, not a rank)
**Where seen:** November Project "the tribe" identity markers; third-place theory (Oldenburg); Strava Local Legend as a *status object*.
**Why it works:** A small, honest badge — "Third Place · seats 20, open late, welcomes laptops & lingerers" — reframes a shop from a transaction to a *place to be*. It's an identity object the shop and its regulars will share. Crucially for our honesty brand: it's a **descriptive, checkable claim** (seating, late hours, wifi, welcomes-you-to-stay), never a fabricated popularity score.
**Snippet:**
```html
<span class="badge badge--third-place" title="A place to stay, not just buy">
  <svg class="badge__glyph" aria-hidden="true"><!-- armchair --></svg>
  Third Place
</span>
```
```css
.badge--third-place{
  display:inline-flex;align-items:center;gap:.4rem;
  font:600 .68rem/1 Inter;letter-spacing:.12em;text-transform:uppercase;
  color:#C5A46D;padding:.4rem .6rem;border:1px solid rgba(197,164,109,.35);
  border-radius:2px;background:rgba(197,164,109,.06)}
.badge__glyph{width:14px;height:14px}
```
**Impact:** H · **Effort:** Low (a data flag per shop + one component). Only shops that genuinely qualify get it — scarcity keeps it credible.

### 4. Moderation-gated submit-your-event flow
**Where seen:** UIUX Trend submit-your-event; Strava club-created events; classic UGC directories.
**Why it works:** Lets the community *feed the hub* without letting spam onto an honesty-brand site. Consent stated up front, editorial discretion explicit, nothing publishes until a human approves. On a static site the form posts to a serverless endpoint / form service (Formspree, Netlify Forms, a Supabase function) and lands in a review queue — the page stays static.
**Snippet:**
```html
<form class="submit-event" method="post" action="/api/events/submit">
  <p class="submit-event__consent">
    Submitting stores your event and, <em>if we verify it</em>, lists it on
    Boba Night. We approve at our discretion — no fake or promotional-only events.
  </p>
  <label>Event name <input name="name" required></label>
  <label>Shop <input name="shop" list="shops" required></label>
  <label>When <input name="when" placeholder="Every Tue 7pm" required></label>
  <label>Your email (we verify, never published) <input type="email" name="email" required></label>
  <button>Submit for review</button>
</form>
```
**Impact:** M · **Effort:** Med (needs a form endpoint + a moderation habit). Ship the honesty copy even in v1.

### 5. Pre-rendered OG card per shop/event (every link unfurls designed)
**Where seen:** Vercel OG/Satori; knaap.dev static-site OG technique; Strava's shareable-by-default philosophy.
**Why it works:** When someone drops a Boba Night link in a group chat, iMessage/Discord/Slack unfurl the `og:image`. A bare URL is invisible; a designed obsidian card with the shop name and the pink glyph *is an ad*. On a static build, generate one 1200×630 PNG per shop at build time (or a shared template with the name composited) and reference it per page.
**Snippet:**
```html
<!-- per shop page <head> -->
<meta property="og:title" content="Boba Guys DTLA — Boba Night">
<meta property="og:image" content="https://bobanight.com/og/boba-guys-dtla.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```
```js
// build step: node-canvas draws the same card design used for in-app sharing,
// writes /og/<slug>.png. One template, N shops, zero runtime cost.
```
**Impact:** H · **Effort:** Med (a build script; reuses the move-#2 card design).

### 6. "I'm going" soft RSVP (count of intent, not fake attendance)
**Where seen:** Strava Group Events RSVP; Meetup "attending"; November Project's low-friction "just show up."
**Why it works:** A lightweight "I'm going" gives social proof *and* a reason to return, without an account wall. Honesty guardrail: show it only when real (a serverless counter), and if you can't verify, don't invent a number — show "Be the first to say you're in" instead of a fake 47. Intent counts are honest; attendance counts you didn't measure are not.
**Snippet:**
```html
<button class="rsvp" data-event="taro-tuesdays" aria-pressed="false">
  <span class="rsvp__label">I'm going</span>
  <span class="rsvp__count" hidden>0 in</span>
</button>
```
```css
.rsvp[aria-pressed="true"]{border-color:#ff3f6f;color:#ff3f6f}
.rsvp[aria-pressed="true"] .rsvp__count{color:#ff3f6f} /* the one glow */
```
**Impact:** M · **Effort:** Med (needs a counter endpoint; degrade to a plain calendar link if none).

### 7. City "tribe" hub page (recurring rhythm as the hero)
**Where seen:** November Project city pages; Strava club home.
**Why it works:** November Project's genius is that the *schedule is the homepage*. A Boba Night city page whose hero is "This week in LA boba" — a weekday grid of recurring meetups — turns a directory into a living calendar people check weekly. It reframes the site from reference to ritual.
**Snippet:**
```css
.week-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:1px;
  background:rgba(197,164,109,.18)} /* hairline gutters via gap bg */
.week-grid > *{background:#0B0C0E;padding:1rem;min-height:8rem}
.week-grid__day{font:600 .7rem/1 Inter;letter-spacing:.14em;
  text-transform:uppercase;color:#C5A46D}
@media(max-width:640px){.week-grid{grid-template-columns:1fr}}
```
**Impact:** H · **Effort:** Med (depends on having events data; empty state = "no meetups yet — start one").

### 8. Inside-language eyebrows & rituals (belonging copy)
**Where seen:** November Project ("Show Up!", "the tribe", first-name founders, ritual jargon).
**Why it works:** Shared vocabulary is the cheapest, strongest belonging mechanic. A recurring meetup with a *name* ("Taro Tuesdays," "Last-Call Lattes") and a repeated imperative eyebrow ("Show up. Sip. Stay.") makes members feel like insiders. Costs nothing, ships as copy, differentiates instantly from every generic Yelp-alike.
**Snippet:**
```html
<p class="eyebrow eyebrow--ritual">Show up · Sip · Stay</p>
```
```css
.eyebrow--ritual{font:600 .72rem/1 Inter;letter-spacing:.22em;
  text-transform:uppercase;color:#C5A46D}
```
**Impact:** M · **Effort:** Low (pure copy + type). High ROI on brand feel.

### 9. Streak / regular's "punch card" (personal, local, no account)
**Where seen:** Strava streaks & Local Legend; loyalty punch-card mental model.
**Why it works:** A private, `localStorage`-backed "shops visited" or "meetups attended" streak gives a solo user a reason to keep coming back and a milestone worth screenshotting ("10 boba nights"). No login, no PII, no server — honest because it only ever reflects the user's own taps on *this* device. Feeds move #2 (share the milestone card).
**Snippet:**
```js
function bump(slug){
  const seen = new Set(JSON.parse(localStorage.bn_visited||'[]'));
  seen.add(slug);
  localStorage.bn_visited = JSON.stringify([...seen]);
  return seen.size; // e.g. show "12 shops explored"
}
```
**Impact:** M · **Effort:** Low. Frame honestly ("your device only") to fit the brand.

### 10. Add-to-calendar as first-class CTA (RRULE → .ics)
**Where seen:** AddEvent recurring-rule generator; Strava event → calendar.
**Why it works:** The gap between "I'd like to go" and "I go" is remembering. A static `.ics` file with an `RRULE` drops the recurring boba night straight into Google/Apple Calendar with its own reminder — the retention step November Project gets from muscle memory, we get from the OS.
**Snippet:**
```
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:Taro Tuesdays @ Boba Guys DTLA
DTSTART;TZID=America/Los_Angeles:20260721T190000
RRULE:FREQ=WEEKLY;BYDAY=TU
LOCATION:Boba Guys, 333 S Alameda St, Los Angeles
URL:https://bobanight.com/events/taro-tuesdays
END:VEVENT
END:VCALENDAR
```
**Impact:** M · **Effort:** Low (one static file per recurring event; can be generated in the build).

### 11. Event `schema.org/Event` markup (community layer earns SEO)
**Where seen:** Strava/Meetup rich results; general structured-data best practice.
**Why it works:** Marking meetups up as `Event` with `eventSchedule`/`Schedule` (which supports `byDay` + `repeatFrequency`) makes them eligible for Google's event rich results and date carousels — free discovery that feeds the community loop. The honesty brand benefits: it's factual, dated, structured data, not a rating.
**Snippet:**
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Event",
 "name":"Taro Tuesdays",
 "eventSchedule":{"@type":"Schedule","byDay":"Tuesday",
   "repeatFrequency":"P1W","startTime":"19:00"},
 "location":{"@type":"Place","name":"Boba Guys DTLA"},
 "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode"}
</script>
```
**Impact:** M · **Effort:** Low (template partial; reuses event data).

### 12. "Start a boba night here" empty-state on every shop
**Where seen:** Strava "create an event" on club pages; November Project's "all you need to do is show up."
**Why it works:** Turns 334 passive listings into 334 seeds. A shop with no meetup shows a warm prompt — "No boba nights here yet. Be the one who starts it." — linking to the submit flow (move #4) pre-filled with that shop. Community grows bottom-up instead of waiting for staff to seed every venue.
**Snippet:**
```html
<div class="meetup-empty">
  <p>No boba nights here yet.</p>
  <a class="link-pink" href="/submit-event?shop=boba-guys-dtla">
    Be the one who starts it →</a>
</div>
```
```css
.meetup-empty{border:1px dashed rgba(197,164,109,.3);border-radius:2px;
  padding:1.25rem;text-align:center;color:rgba(244,239,231,.7)}
.link-pink{color:#ff3f6f} /* the single glow, used sparingly */
```
**Impact:** M · **Effort:** Low (empty-state component + query-param prefill).

---

## What now reads dated (avoid list)

- **Facebook Events embeds / "RSVP on Facebook" buttons.** Dead-feeling, tracker-heavy, off-brand. Own the event object; export to calendar instead.
- **Fake attendance / "1.2k going" inflated counts.** Directly violates the honesty brand and the reader can smell it. Show real intent or an honest empty state.
- **Generic third-party widgets** (Eventbrite iframes, Meetup embeds) dropped into the page — they shatter the obsidian editorial theme and load a stranger's CSS. Build native, tiny components.
- **Rainbow gamification** — big cartoon trophy/confetti badges, XP bars, leaderboards ranked 1-2-3. Wrong register for a champagne-hairline editorial site; keep status objects quiet and typographic.
- **"Social wall" auto-pulled Instagram feeds.** Slow, permission-fraught, visually noisy. A curated, self-authored card beats an embedded feed.
- **Autoplaying share pop-ups / "share to unlock."** Sharing must be a calm user-gesture button, never a dark-pattern gate.
- **Countdown-timer urgency** on recurring events — nonsensical for "every Tuesday" and cheapens the ritual. Cadence, not urgency.
- **Multi-step wizard modals** for submitting an event. One honest form on one page; moderation happens after, not via friction before.

---

## Recommended for Boba Night (apply these 3–5)

1. **The recurring-meetup object + city "this week" grid (moves #1, #7).** This is the whole thesis. An events data file → human-readable "every Tuesday" cadence → a weekday grid hero on each city page. It reframes the site from reference to ritual. Everything else hangs off this spine. *Start here.*
2. **Client-side shareable card via canvas + Web Share API (move #2), reused as pre-rendered OG images (move #5).** One card design, two outputs: the mobile share sheet and every link unfurl. This is the free-distribution engine — Strava's core insight applied to a static site. Draw obsidian + Fraunces + one pink glyph; ship it as the highest-leverage virality feature.
3. **Per-shop "third place" badge (move #3).** On-brand, honest, checkable, and it's an identity object shops and regulars will share. Cheap to build, strong differentiation, and it advances the "these are places to *be*, not just buy" story.
4. **Moderation-gated submit-your-event flow + "start one here" empty states (moves #4, #12).** Turns 334 listings into 334 community seeds without risking spam on an honesty-brand site. Ship the consent/discretion copy from day one even if the queue is manual.
5. **Add-to-calendar `.ics` + `schema.org/Event` markup (moves #10, #11).** Quiet retention + free SEO discovery, near-zero effort, both fully honest (factual, dated, structured). Bundle into the build that generates the event pages.

Deliberately deferred: soft RSVP counters (#6) and personal streaks (#9) are good *second-wave* additions once meetups exist — they need real data behind them to stay honest. Ship the ritual and the shareable card first; add the counters only when there's something true to count. Inside-language copy (#8) should be woven through all of the above rather than treated as a separate feature.
