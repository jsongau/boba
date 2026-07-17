# Events Hub / Calendar — Design Research

Topic: how a boba directory should present a lightweight EVENTS HUB — recurring vs one-off, cadence chips, RSVP/subscribe, calendar-as-hub, ICS/add-to-calendar affordances, event-card anatomy on dark themes.
Scope guard: Boba Night is a **static vanilla-JS site with no login and no backend**. There is no true RSVP database. So the useful patterns are: a browsable/filterable **agenda list** (calendar-as-hub), honest **cadence labeling**, and **add-to-calendar (.ics) as the only real "commit" affordance**. Everything below is filtered through that reality.

---

## Sources studied

- **Luma (luma.com) + Luma UI breakdown (screensdesign.com)** — the reference for "calendar-as-hub": tripartite discovery (categories / cities / curated calendars), an explicit "You are going" status pill, single-page create form with date/time in overlays, slide-up detail transitions. Confirms the hub → detail → commit spine.
- **Partiful (partiful.com) + Pratt IxD design critique** — playful/editorial dark-theme event pages; RSVP row ordered by *natural mapping* (Going / Maybe / Can't go); custom poster art as the hero. Also a cautionary tale: an element that "affords" clicking but only toggles = discoverability bug. Relevant to how we style chips vs buttons.
- **Resy event discovery hub (blog.resy.com/newsroom/event-discovery-ticketing)** — chronological "calendar format" city hubs; icon-based type tags (pin-drop = in-person, camera = virtual); cadence conveyed purely through date presentation (single date for one-offs, "December through February" month-span for series). Good model for cadence-by-typography.
- **Meetup (help.meetup.com repeating events)** — the canonical recurring-series model: a series page that lists upcoming instances; "repeats weekly" language; subscribe-to-group as the durable commit. Maps to our "recurring" chip + series grouping.
- **Eleken "Calendar UI Examples" + ui-patterns.com Event Calendar + uxpatterns.dev Calendar** — agenda vs month-grid tradeoffs; Today/This-week date grouping; filter chips for category; color must pair with a label (never color-alone); minimal data density per card. The backbone of the agenda-list recommendation.
- **calen.events ICS Integration Guide (RFC 5545) + MDN Blob/download** — exact .ics field stack (VEVENT/DTSTART/DTSTAMP/UID/RRULE), client-side Blob download, and the Google/Outlook add-to-calendar URL templates. This is the one genuinely functional "commit" we can ship statically.
- **CSS-Tricks "position: sticky and table headers" + Frontend Masters "weird parts of position: sticky"** — technique for sticky date-group headers in a scrolling agenda, and the gotchas (overflow ancestors kill it).

---

## Hot moves

### 1. Calendar-as-hub = a filterable **agenda list**, not a month grid
Where: Luma, Resy, Meetup all default to a vertical chronological list, not a 7×5 grid. A month grid is wrong for a directory with sparse events across 334 shops — mostly-empty cells look dead. A dated, grouped list reads full and scans fast.
Why it works: density matches reality (a few events/week), it's mobile-first by default, and it needs zero date-math JS.
```html
<ul class="agenda">
  <li class="agenda__day"><h2 class="agenda__date">Fri · Jul 18</h2></li>
  <li class="agenda__event"> …event card… </li>
  <li class="agenda__event"> …event card… </li>
  <li class="agenda__day"><h2 class="agenda__date">Sat · Jul 19</h2></li>
  …
</ul>
```
Impact: **H** — this is the core layout decision. Effort: **Low** (static markup, sort by date at build time).

### 2. Sticky date-group headers as champagne hairline dividers
Where: agenda pattern (Eleken, uxpatterns.dev) + CSS-Tricks sticky-header technique. As you scroll, the current day's date pins to the top so you never lose your place.
Why: gives a long single-column list structure without chrome; the header itself becomes the only "loud" hairline element on screen.
```css
.agenda__date{
  position: sticky; top: 0; z-index: 2;
  padding: .5rem 0;
  font: .72rem/1 "Inter"; letter-spacing:.14em; text-transform:uppercase;
  color: #C5A46D;                         /* champagne eyebrow */
  background: linear-gradient(#0B0C0E 70%, transparent);  /* fade, no hard edge */
  border-bottom: 1px solid rgba(197,164,109,.28);
}
/* GOTCHA: no ancestor between .agenda and viewport may have overflow:hidden/auto,
   or sticky silently dies. Keep the scroll on the page, not a wrapper. */
```
Impact: **M**. Effort: **Low**.

### 3. Cadence chips — one-off vs recurring, stated in words + a shape
Where: Meetup ("repeats weekly"), Resy (month-span implies series). Eleken's rule: **never encode meaning in color alone** — pair it with a label. A tiny chip on each card tells you if this is a single night or a standing thing.
Why: recurring vs one-off is the single most useful filter for "when can I go?" — and on a directory it doubles as an honesty signal (we're not faking urgency).
```html
<span class="chip chip--recurring">Every Thu</span>
<span class="chip chip--oneoff">One night only</span>
```
```css
.chip{ font:.68rem/1 "Inter"; letter-spacing:.08em; text-transform:uppercase;
  padding:.28em .6em; border-radius:2px; border:1px solid rgba(197,164,109,.35);
  color:#C5A46D; }
.chip--recurring{ border-style:dashed; }   /* dashed = repeats, a shape cue not a color cue */
.chip--oneoff{ color:#F4EFE7; border-color:rgba(244,239,231,.25); }
```
Impact: **H**. Effort: **Low**.

### 4. Cadence-by-typography: single date vs date-range vs "every"
Where: Resy — one-offs show `Sat, Nov 21`; series show `December → February`. The date line *is* the cadence signal before you even read the chip.
Why: zero extra UI; the eye learns "range = ongoing" instantly.
```
One-off :  FRI · JUL 18 · 7–10PM
Series  :  EVERY THU · 6PM onward
Season  :  JUL → SEP · rotating flavors
```
Render the middle token (`·`) as a champagne hairline glyph; keep the arrow `→` for ranges only. Impact: **M**. Effort: **Low**.

### 5. Filter chips row: cadence + area + type (chips, not a `<select>`)
Where: Luma's category/city vectors; Resy's pin-drop/camera type icons; Eleken filter-chips. A single horizontal, wrap-friendly chip row above the agenda; clicking toggles `.is-on` and hides non-matching `<li>`.
Why: tactile, thumb-friendly, no dropdown modal. Matches the directory's existing chip vocabulary (closed chips, area chips).
```js
// vanilla, no deps — data-attrs drive it
const chips = document.querySelectorAll('.filter [data-filter]');
const events = document.querySelectorAll('.agenda__event');
chips.forEach(c => c.addEventListener('click', () => {
  c.classList.toggle('is-on');
  const active = [...chips].filter(x=>x.classList.contains('is-on')).map(x=>x.dataset.filter);
  events.forEach(e => {
    const tags = e.dataset.tags.split(' ');
    e.hidden = active.length && !active.every(a => tags.includes(a));
  });
});
```
Impact: **H**. Effort: **Low–Med**.

### 6. The **.ics add-to-calendar** button = the one honest "commit"
Where: calen.events RFC 5545 guide. With no accounts, we can't do RSVP — but we CAN let someone add an event to their real calendar. This is the single most valuable interaction the hub can offer, and it's fully static.
Why: it converts browsing into a durable action without pretending we have a database. Honest-brand safe.
```js
function icsHref({title, startUTC, endUTC, desc='', loc=''}){
  const esc = s => s.replace(/([,;\\])/g,'\\$1').replace(/\n/g,'\\n');
  const body = [
    'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Boba Night//Events//EN',
    'BEGIN:VEVENT',
    `UID:${startUTC}-${Math.random().toString(36).slice(2)}@bobanight.com`,
    `DTSTAMP:${new Date().toISOString().replace(/[-:]|\.\d{3}/g,'')}`,
    `DTSTART:${startUTC}`, `DTEND:${endUTC}`,   // e.g. 20260718T190000Z
    `SUMMARY:${esc(title)}`, `DESCRIPTION:${esc(desc)}`, `LOCATION:${esc(loc)}`,
    'STATUS:CONFIRMED','END:VEVENT','END:VCALENDAR'
  ].join('\r\n');                                // CRLF is mandatory
  return URL.createObjectURL(new Blob([body],{type:'text/calendar'}));
}
// <a download="boba-night.ics" href="…"> Add to calendar </a>
```
Impact: **H**. Effort: **Med** (need clean start/end times per event; escape + CRLF are the traps).

### 7. Recurring series → **RRULE**, so one .ics carries the whole cadence
Where: RFC 5545 RRULE (`FREQ=WEEKLY;BYDAY=TH`). For a "Every Thursday" event, emit ONE VEVENT with a recurrence rule instead of dumping 12 rows.
Why: the user's calendar then owns the repeat; matches the "recurring" chip semantically; keeps the agenda list short.
```
DTSTART:20260718T190000Z
RRULE:FREQ=WEEKLY;BYDAY=TH;COUNT=12
```
Provide `UNTIL=…Z` or `COUNT=n` so it doesn't repeat forever. Impact: **M**. Effort: **Low** (one extra line in the ICS builder).

### 8. Native add-to-calendar menu (Google / Apple / Outlook), no library
Where: calen.events URL templates. Instead of a heavyweight add-to-calendar widget, a tiny `<details>` disclosure with three links: Google (render URL), Outlook (compose URL), Apple (the .ics blob). All static.
Why: covers ~all users, ships as HTML, degrades gracefully, no 40KB dependency.
```html
<details class="atc">
  <summary>Add to calendar</summary>
  <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&text=Boba+Night&dates=20260718T190000Z/20260718T220000Z&location=…">Google</a>
  <a download="event.ics" href="blob:…">Apple / .ics</a>
  <a href="https://outlook.live.com/calendar/0/action/compose?subject=Boba+Night&startdt=2026-07-18T19:00:00Z&enddt=2026-07-18T22:00:00Z">Outlook</a>
</details>
```
Impact: **M**. Effort: **Low**.

### 9. Event-card anatomy for a dark editorial theme
Where: synthesized from Luma (status pill), Partiful (poster hero), Resy (type icon + terse date), Eleken (minimal density). On obsidian, the card is defined by a **hairline border**, not a fill — fills muddy the black.
Structure, top → bottom:
1. eyebrow: `FRI · JUL 18` (champagne, letterspaced) + cadence chip, same row
2. title: Fraunces, 1.25–1.5rem — the venue/event name
3. one terse line: shop name · neighborhood · price band
4. footer row: type tag (in-person/tasting/popup) left, `Add to calendar` right
```css
.event{ border:1px solid rgba(197,164,109,.22); border-radius:2px;
  padding:1rem 1.1rem; background:transparent;
  transition:border-color .18s ease, transform .18s ease; }
.event:hover{ border-color:rgba(197,164,109,.5); transform:translateY(-2px); }
.event__title{ font-family:"Fraunces",serif; font-size:1.35rem; color:#F4EFE7; }
@media (prefers-reduced-motion:reduce){ .event{ transition:none } .event:hover{ transform:none } }
```
Impact: **H**. Effort: **Low**.

### 10. ONE glowing element per viewport — reserve the neon for "happening now"
Where: Boba Night's own one-glow rule + Luma's single "You are going" accent. Don't pink-ify every card. Reserve `#ff3f6f` for a single **"Tonight"** marker — the soonest event, or a live "on now" pill.
Why: preserves the brand's one-neon-per-viewport discipline; makes "tonight" genuinely scannable in a long list.
```css
.event--tonight .event__eyebrow{ color:#ff3f6f; }
.event--tonight::before{ content:"TONIGHT"; /* the one glow */
  color:#ff3f6f; text-shadow:0 0 12px rgba(255,63,111,.55);
  font:.68rem/1 "Inter"; letter-spacing:.16em; }
```
Only ever render one `.event--tonight` in view. Impact: **H** (signature moment). Effort: **Low**.

### 11. Honest empty & "no events near you" states
Where: Eleken empty-state guidance; Boba Night honesty brand. Sparse events are the norm — an empty week must feel intentional, not broken. No fake "12 events!" No countdown theater.
Why: an editorial empty state ("No boba nights this week in the Valley — check back Thursday") reads as curated confidence, not a bug.
```html
<li class="agenda__empty">
  <p class="agenda__empty-eyebrow">QUIET WEEK</p>
  <p>No events listed near you yet. New pop-ups post on Thursdays.</p>
</li>
```
Impact: **M**. Effort: **Low**.

### 12. "Subscribe to the calendar" via webcal:// (the durable, account-free RSVP)
Where: Meetup's subscribe-to-group; calen.events webcal feed. If you ever host a single hosted `events.ics` feed, users can subscribe once via `webcal://` and get every future boba night auto-synced — the closest static analog to "follow / RSVP."
Why: it's the one commit that keeps giving, with zero backend beyond a re-generated static .ics file.
```html
<a href="webcal://bobanight.com/events.ics">Subscribe to all boba nights</a>
```
(Same file served over https as the download; `webcal://` just tells the OS to subscribe & poll.) Impact: **M**. Effort: **Med** (need a build step that regenerates the feed file).

### 13. Detail reveal via `<details>`/native disclosure, not a route
Where: Luma's slide-up detail; but for a static directory, an inline expand keeps you in the list. Each card's full blurb lives in a `<details>` so it's crawlable, needs no JS, and animates open.
```css
.event__more[open] .event__body{ animation: reveal .22s ease both; }
@keyframes reveal{ from{ opacity:0; transform:translateY(-4px) } to{ opacity:1; transform:none } }
```
Impact: **M**. Effort: **Low**.

---

## What now reads dated (avoid list)

- **Full month-grid calendars** for a low-density event set — acres of empty cells scream "nothing's happening." Grids are for scheduling apps, not discovery.
- **Fake RSVP / "going" counters** with no backend — dishonest, and against brand. If we can't count real attendance, don't show a number.
- **Countdown timers** on every card ("Starts in 03:14:22!") — 2019 landing-page urgency theater; cheapens an editorial voice.
- **Heavy add-to-calendar JS widgets** (40KB+ libraries) when three static links + one Blob do the job.
- **Color-only category coding** (a red dot with no label) — fails accessibility and Eleken's pairing rule; on obsidian, subtle hues vanish anyway.
- **Carousels / horizontal side-scroll of events** — Partiful critique flagged the dead space and poor scan-ability; vertical agenda beats it.
- **Glassmorphism blur cards / drop shadows** on a true-black theme — shadows do nothing on #0B0C0E; the hairline border is the correct separator.
- **Modal-per-event routing** for a directory — breaks back-button and crawlability; inline `<details>` is better here.
- **Rainbow category chips** — collides with the one-neon rule; keep chips champagne, spend the pink once.

## Recommended for Boba Night (the 3–5 to actually apply)

1. **Agenda-list hub with sticky champagne date headers** (moves #1, #2) — the whole page is a dated vertical list, Today/This-week grouped, sticky date eyebrows. This is the layout; build it first.
2. **Cadence system: chip + date-typography, one-off vs recurring** (moves #3, #4) — dashed chip = recurring, solid = one-off; date line encodes cadence (`EVERY THU` / `JUL 18` / `JUL → SEP`). Honest, scannable, zero color abuse.
3. **The .ics "Add to calendar" affordance as the primary commit** (moves #6, #7, #8) — with RRULE for recurring series and a tiny native Google/Apple/Outlook `<details>` menu. This is the only real action the static hub can offer, and it's genuinely useful.
4. **Dark editorial event card + the single "TONIGHT" glow** (moves #9, #10) — hairline-border cards, Fraunces titles, and exactly one `#ff3f6f` "Tonight" marker per viewport for the soonest event. Signature moment, on-brand.
5. **Honest empty states + optional webcal subscribe** (moves #11, #12) — an editorial "quiet week" message instead of a broken-looking blank, and, if a build step exists, one `events.ics` feed users can subscribe to.

Ship 1–3 for a complete, functional, honest hub; 4 makes it feel like Boba Night; 5 is the polish/retention layer.
