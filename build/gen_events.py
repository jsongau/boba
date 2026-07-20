#!/usr/bin/env python3
"""build/gen_events.py — the Boba Night events system.

Inputs
    data/events.json        SERIES / OCCURRENCE model (source of truth)
    data/stores-data.json   directory shop records (for host location)
    templates/nav.html      canonical navigation partial (spliced in, kept in sync)

Outputs (all owned by task W4)
    meetups/index.html                 obsidian-themed hub, regenerated
    build/shop-events.json             shop_slug -> [series]  (for the profile generator)
    meetups/ics/<slug>.ics             per-series calendar, RRULE only when known
    meetups/ics/bobanight-events.ics   aggregate of every dated event

Honesty contract, enforced in code:
    * cadence_rrule drives the on-page cadence chip and a *computed* "Next:" line.
    * A "Next:" date is only ever computed from a real rrule or a real occurrence —
      never invented.
    * Event JSON-LD emits ONE node per MATERIALIZED occurrence (a dated entry in
      occurrences[]). Never eventSchedule, never an rrule-projected date.

Run:  python3 build/gen_events.py
"""
from __future__ import annotations

import html
import json
import os
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EVENTS_JSON = os.path.join(ROOT, "data", "events.json")
STORES_JSON = os.path.join(ROOT, "data", "stores-data.json")
NAV_PARTIAL = os.path.join(ROOT, "templates", "nav.html")

MEETUPS_HTML = os.path.join(ROOT, "meetups", "index.html")
CALENDAR_HTML = os.path.join(ROOT, "meetups", "calendar", "index.html")
INDEX_HTML = os.path.join(ROOT, "index.html")
SHOP_EVENTS = os.path.join(ROOT, "build", "shop-events.json")
ICS_DIR = os.path.join(ROOT, "meetups", "ics")

# how many days forward the homepage "This week" strip looks
STRIP_WINDOW_DAYS = 7
# how many days forward the venue calendar agenda projects
CALENDAR_WINDOW_DAYS = 56

SITE = "https://www.bobanight.com"
TZID = "America/Los_Angeles"

WEEKDAY_CODE = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
WEEKDAY_NAME = {0: "MONDAY", 1: "TUESDAY", 2: "WEDNESDAY", 3: "THURSDAY",
                4: "FRIDAY", 5: "SATURDAY", 6: "SUNDAY"}

KIND_LABEL = {
    "club": "Social club",
    "crawl": "Crawl",
    "run": "Run",
    "cupsleeve": "Cupsleeve",
    "collab": "Collab",
    "book-club": "Book club",
}


# --------------------------------------------------------------------------- IO
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


# ----------------------------------------------------------------- rrule helpers
def parse_rrule(rrule):
    """Return dict of RRULE parts, e.g. {'FREQ':'WEEKLY','BYDAY':'TH'}. None -> {}."""
    if not rrule:
        return {}
    parts = {}
    for chunk in rrule.split(";"):
        if "=" in chunk:
            k, v = chunk.split("=", 1)
            parts[k.strip().upper()] = v.strip().upper()
    return parts


def fmt_time_12h(hhmm):
    """'18:45' -> '6:45 PM'; '19:00' -> '7 PM'."""
    if not hhmm:
        return ""
    h, m = (int(x) for x in hhmm.split(":"))
    ap = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {ap}" if m else f"{h12} {ap}"


def cadence_chip(series):
    """The 'EVERY THURSDAY · 6:45 PM' style chip — crisp cadence ONLY, from a
    published rrule. Returns '' when the cadence is descriptive/irregular; the
    caller renders cadence_text as quiet meta instead of a filled pill."""
    parts = parse_rrule(series.get("cadence_rrule"))
    if parts.get("FREQ") == "WEEKLY" and "BYDAY" in parts:
        days = [WEEKDAY_NAME[WEEKDAY_CODE[d]] for d in parts["BYDAY"].split(",")
                if d in WEEKDAY_CODE]
        label = "EVERY " + " & ".join(days)
        t = fmt_time_12h(series.get("start_time"))
        return f"{label} · {t.upper()}" if t else label
    return ""


def next_from_rrule(series, today):
    """Next date a WEEKLY;BYDAY rrule fires on or after `today`. None otherwise."""
    parts = parse_rrule(series.get("cadence_rrule"))
    if parts.get("FREQ") != "WEEKLY" or "BYDAY" not in parts:
        return None
    targets = [WEEKDAY_CODE[d] for d in parts["BYDAY"].split(",") if d in WEEKDAY_CODE]
    if not targets:
        return None
    for i in range(0, 14):
        d = today + timedelta(days=i)
        if d.weekday() in targets:
            return d
    return None


def next_from_occurrences(series, today):
    """Earliest materialized occurrence date on or after `today`. None otherwise."""
    dates = []
    for occ in series.get("occurrences", []):
        try:
            d = datetime.strptime(occ["date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        if d >= today:
            dates.append(d)
    return min(dates) if dates else None


def compute_next(series, today):
    """(next_date, basis) where basis is 'occurrence' | 'rrule' | None.
    Occurrences (materialized, verified) win over rrule projections."""
    d = next_from_occurrences(series, today)
    if d:
        return d, "occurrence"
    d = next_from_rrule(series, today)
    if d:
        return d, "rrule"
    return None, None


# ------------------------------------------------------------------- shop lookup
def build_shop_index(stores):
    idx = {}
    for s in stores:
        idx[s["slug"]] = s
    return idx


def shop_profile_url(shop):
    """Best-effort directory profile URL from a store record."""
    city_slug = (shop.get("city") or "").strip().lower().replace(" ", "-")
    return f"/boba/ca/{city_slug}/{shop['slug']}/"


def shop_location_line(shop):
    bits = [shop.get("name"), shop.get("address"), shop.get("city")]
    return ", ".join(b for b in bits if b)


# --------------------------------------------------------------------------- ICS
def ics_escape(text):
    """RFC 5545 §3.3.11 TEXT escaping."""
    return (str(text).replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def fold_line(line):
    """RFC 5545 §3.1 line folding at 75 octets, continuation with a leading space."""
    out = []
    raw = line.encode("utf-8")
    while len(raw) > 75:
        # find a safe cut that does not split a multibyte char
        cut = 75
        while cut > 0 and (raw[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(raw[:cut].decode("utf-8"))
        raw = b" " + raw[cut:]
    out.append(raw.decode("utf-8"))
    return "\r\n".join(out)


def dtstamp_utc():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def vevent_for_series(series, shop_index, stamp):
    """Return a list of VEVENT line-groups for a series, or [] if it has no dated
    anchor. RRULE emitted only when cadence_rrule is set; single VEVENTs for each
    materialized occurrence."""
    events = []
    uid_base = series["slug"]
    summary = series["title"]
    desc = series.get("vibe", "")
    url = series.get("host_url", "")

    # location from the first associated shop, if any
    loc = ""
    for slug in series.get("shop_slugs", []):
        shop = shop_index.get(slug)
        if shop:
            loc = shop_location_line(shop)
            break
    if not loc and series.get("host_venues"):
        loc = series["host_venues"][0]

    # 1) RRULE-backed recurring event (pattern is published, e.g. weekly Thursday)
    parts = parse_rrule(series.get("cadence_rrule"))
    if parts.get("FREQ") == "WEEKLY" and "BYDAY" in parts:
        anchor = next_from_rrule(series, date.today())
        st = series.get("start_time", "19:00")
        sh, sm = (int(x) for x in st.split(":"))
        dur = int(series.get("duration_min", 120))
        start_dt = datetime(anchor.year, anchor.month, anchor.day, sh, sm)
        end_dt = start_dt + timedelta(minutes=dur)
        lines = [
            "BEGIN:VEVENT",
            f"UID:{uid_base}-rrule@bobanight.com",
            f"DTSTAMP:{stamp}",
            f"DTSTART;TZID={TZID}:{start_dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND;TZID={TZID}:{end_dt.strftime('%Y%m%dT%H%M%S')}",
            f"RRULE:{series['cadence_rrule']}",
            f"SUMMARY:{ics_escape(summary)}",
        ]
        if loc:
            lines.append(f"LOCATION:{ics_escape(loc)}")
        if desc:
            lines.append(f"DESCRIPTION:{ics_escape(desc)}")
        if url:
            lines.append(f"URL:{ics_escape(url)}")
        lines.append("END:VEVENT")
        events.append(lines)

    # 2) One VEVENT per MATERIALIZED occurrence (verified dates only)
    for i, occ in enumerate(series.get("occurrences", [])):
        try:
            d = datetime.strptime(occ["date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        lines = [
            "BEGIN:VEVENT",
            f"UID:{uid_base}-{occ['date'].replace('-', '')}@bobanight.com",
            f"DTSTAMP:{stamp}",
        ]
        if occ.get("all_day"):
            lines.append(f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}")
            lines.append(f"DTEND;VALUE=DATE:{(d + timedelta(days=1)).strftime('%Y%m%d')}")
        else:
            st = occ.get("time", series.get("start_time", "19:00"))
            sh, sm = (int(x) for x in st.split(":"))
            dur = int(series.get("duration_min", 120))
            start_dt = datetime(d.year, d.month, d.day, sh, sm)
            end_dt = start_dt + timedelta(minutes=dur)
            lines.append(f"DTSTART;TZID={TZID}:{start_dt.strftime('%Y%m%dT%H%M%S')}")
            lines.append(f"DTEND;TZID={TZID}:{end_dt.strftime('%Y%m%dT%H%M%S')}")
        lines.append(f"SUMMARY:{ics_escape(summary)}")
        occ_loc = loc
        if occ.get("note"):
            desc2 = f"{desc} — {occ['note']}" if desc else occ["note"]
        else:
            desc2 = desc
        if occ_loc:
            lines.append(f"LOCATION:{ics_escape(occ_loc)}")
        if desc2:
            lines.append(f"DESCRIPTION:{ics_escape(desc2)}")
        occ_url = occ.get("url") or url
        if occ_url:
            lines.append(f"URL:{ics_escape(occ_url)}")
        lines.append("END:VEVENT")
        events.append(lines)

    return events


def wrap_calendar(vevent_groups, name):
    head = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Boba Night//Meetups//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape(name)}",
        f"X-WR-TIMEZONE:{TZID}",
    ]
    body = []
    for grp in vevent_groups:
        body.extend(grp)
    tail = ["END:VCALENDAR"]
    all_lines = head + body + tail
    return "\r\n".join(fold_line(ln) for ln in all_lines) + "\r\n"


def has_dates(series):
    return bool(parse_rrule(series.get("cadence_rrule")).get("FREQ")) or \
        bool(series.get("occurrences"))


# ---------------------------------------------------------------------- JSON-LD
def event_ld_nodes(series_list, shop_index):
    """One Event node per MATERIALIZED occurrence. Never rrule projections."""
    nodes = []
    for s in series_list:
        for occ in s.get("occurrences", []):
            try:
                datetime.strptime(occ["date"], "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            node = {
                "@type": "Event",
                "name": s["title"],
                "startDate": occ["date"],
                "eventStatus": "https://schema.org/EventScheduled",
                "description": s.get("vibe", ""),
                "url": occ.get("url") or s.get("host_url", ""),
                "organizer": {
                    "@type": "Organization",
                    "name": s.get("host_name", s["title"]),
                    "url": s.get("host_url", ""),
                },
            }
            # location: a real shop Place if associated, else VirtualLocation for
            # virtual series, else the host venue as a named Place.
            shop = None
            for slug in s.get("shop_slugs", []):
                if slug in shop_index:
                    shop = shop_index[slug]
                    break
            if shop:
                place = {
                    "@type": "Place",
                    "name": shop.get("name"),
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": shop.get("address"),
                        "addressLocality": shop.get("city"),
                        "addressRegion": "CA",
                        "addressCountry": "US",
                    },
                }
                if shop.get("latitude") and shop.get("longitude"):
                    place["geo"] = {
                        "@type": "GeoCoordinates",
                        "latitude": shop["latitude"],
                        "longitude": shop["longitude"],
                    }
                node["location"] = place
                node["eventAttendanceMode"] = \
                    "https://schema.org/OfflineEventAttendanceMode"
            elif s.get("region", "").lower().startswith("virtual"):
                node["eventAttendanceMode"] = \
                    "https://schema.org/OnlineEventAttendanceMode"
                node["location"] = {
                    "@type": "VirtualLocation",
                    "url": occ.get("url") or s.get("host_url", ""),
                }
            elif s.get("host_venues"):
                node["location"] = {"@type": "Place", "name": s["host_venues"][0]}
            nodes.append(node)
    return nodes


# --------------------------------------------------------------------- shop map
def build_shop_events(series_list, shop_index, today):
    """shop_slug -> [ {series fields the profile generator needs} ]."""
    out = {}
    for s in series_list:
        nd, basis = compute_next(s, today)
        entry = {
            "slug": s["slug"],
            "title": s["title"],
            "kind": s["kind"],
            "vibe": s["vibe"],
            "cadence_text": s.get("cadence_text", ""),
            "cadence_chip": cadence_chip(s),
            "host_name": s.get("host_name", ""),
            "host_url": s.get("host_url", ""),
            "next_date": nd.isoformat() if nd else None,
            "next_basis": basis,
            "ics": f"/meetups/ics/{s['slug']}.ics" if has_dates(s) else None,
            "meetups_url": f"/meetups/#{s['slug']}",
        }
        for slug in s.get("shop_slugs", []):
            if slug in shop_index:
                out.setdefault(slug, []).append(entry)
    return out


# ------------------------------------------------------------------- HTML build
def load_nav():
    try:
        with open(NAV_PARTIAL, encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return '<a class="bn-skip" href="#main">Skip to content</a>'


def fmt_human_date(d):
    return d.strftime("%a, %b ") + str(d.day) + d.strftime(", %Y")


SECTION_ORDER = [
    ("clubs", "Boba social clubs", ["club", "book-club"]),
    ("crawls", "Crawls, runs &amp; circuits", ["crawl", "run"]),
    ("fandom", "Fandom nights", ["cupsleeve", "collab"]),
]


def region_class(region):
    r = region.lower()
    if "626" in r:
        return "w4-tag--sgv"
    return ""


def render_card(s, shop_index, today):
    nd, basis = compute_next(s, today)
    chip = cadence_chip(s)
    kind = KIND_LABEL.get(s["kind"], s["kind"].title())

    # associated directory shops (linked) — real associations only
    shop_links = []
    for slug in s.get("shop_slugs", []):
        shop = shop_index.get(slug)
        if shop:
            shop_links.append(
                f'<a href="{esc(shop_profile_url(shop))}">{esc(shop["name"])}'
                f' <span class="w4-in">{esc(shop["city"])}</span></a>'
            )

    parts = [f'<article class="w4-card" id="{esc(s["slug"])}">']
    parts.append('<div class="w4-card-head">')
    parts.append(
        f'<span class="w4-tag {region_class(s["region"])}">{esc(s["region"])}</span>'
        f'<span class="w4-tag w4-tag--kind">{esc(kind)}</span>'
    )
    parts.append("</div>")
    parts.append(f'<h3>{esc(s["title"])}</h3>')

    # cadence chip (crisp rrule cadence only) or quiet cadence text; plus a
    # computed Next (only ever from a real rrule / materialized occurrence)
    meta_bits = []
    if chip:
        meta_bits.append(f'<span class="w4-chip">{esc(chip)}</span>')
    elif s.get("cadence_text"):
        meta_bits.append(f'<span class="w4-cad">{esc(s["cadence_text"])}</span>')
    if nd:
        meta_bits.append(
            f'<span class="w4-next"><span class="w4-next-k">Next</span> '
            f'{esc(fmt_human_date(nd))}</span>'
        )
    if meta_bits:
        parts.append('<div class="w4-meta">' + "".join(meta_bits) + "</div>")

    parts.append(f'<p class="w4-vibe">{s["vibe"]}</p>')  # vibe holds curly quotes; pre-escaped in data

    if shop_links:
        parts.append(
            '<p class="w4-shops"><span class="w4-shops-k">In our directory:</span> '
            + " · ".join(shop_links) + "</p>"
        )

    # links row: organizer (truth) + optional .ics
    links = [
        f'<a class="w4-src" href="{esc(s["host_url"])}" rel="noopener" '
        f'target="_blank">{esc(s["host_name"])} &#8599;</a>'
    ]
    if has_dates(s):
        links.append(
            f'<a class="w4-ics" href="/meetups/ics/{esc(s["slug"])}.ics">'
            f'Add to calendar (.ics)</a>'
        )
    parts.append('<div class="w4-links">' + "".join(links) + "</div>")
    parts.append(f'<p class="w4-checked">Organizer listing checked '
                 f'{esc(s["source_checked"])}</p>')
    parts.append("</article>")
    return "\n".join(parts)


def render_html(events, shop_index, today):
    nav = load_nav()
    series = events["series"]

    sections_html = []
    for anchor, heading, kinds in SECTION_ORDER:
        cards = [render_card(s, shop_index, today) for s in series if s["kind"] in kinds]
        if not cards:
            continue
        sections_html.append(
            f'<section class="w4-sec" id="{anchor}">'
            f'<div class="w4-sec-head"><span class="idx">{len(cards):02d}</span>'
            f'<h2>{heading}</h2></div>'
            f'<div class="w4-grid">{"".join(cards)}</div></section>'
        )

    ld_nodes = event_ld_nodes(series, shop_index)
    itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Boba meetups and clubs in Southern California",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": s["title"],
             "url": s["host_url"]}
            for i, s in enumerate(series)
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Meetups & clubs",
             "item": SITE + "/meetups/"},
        ],
    }
    ld_blocks = [json.dumps(itemlist, ensure_ascii=False),
                 json.dumps(breadcrumb, ensure_ascii=False)]
    for node in ld_nodes:
        node_full = {"@context": "https://schema.org"}
        node_full.update(node)
        ld_blocks.append(json.dumps(node_full, ensure_ascii=False))
    ld_html = "\n".join(
        f'<script type="application/ld+json">\n{b}\n</script>' for b in ld_blocks
    )

    css = CARD_CSS
    return PAGE_TEMPLATE.format(
        nav=nav, css=css, sections="".join(sections_html), ld=ld_html,
        year=today.year,
    )


CARD_CSS = """
/* W4 events hub — layered on luxury-homepage.css, obsidian theme. New rules only. */
.w4-crumb{font-family:var(--sans);font-size:.78rem;letter-spacing:.02em;color:var(--muted-dk);
  display:flex;gap:.5rem;align-items:center;padding:1.6rem 0 0}
.w4-crumb a{color:var(--muted-dk)}.w4-crumb a:hover{color:var(--pearl)}
.w4-crumb .sep{opacity:.5}
.w4-head{padding:2.2rem 0 1rem;max-width:60ch}
.w4-head h1{font-size:clamp(2.2rem,5.4vw,3.6rem);margin:.3rem 0 1rem}
.w4-notice{display:flex;gap:.8rem;align-items:flex-start;border:1px solid var(--line-dk);
  border-radius:3px;padding:1rem 1.2rem;margin:1.4rem 0 0;background:rgba(244,239,231,.03);
  font-size:.9rem;color:var(--silver)}
.w4-notice .w4-note-k{font-size:.66rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:var(--champagne);white-space:nowrap;padding-top:.15rem}
.w4-sec{padding:clamp(2.4rem,5vw,3.6rem) 0 0}
.w4-sec-head{display:flex;align-items:baseline;gap:.9rem;border-bottom:1px solid var(--line-dk);
  padding-bottom:.9rem;margin-bottom:1.6rem}
.w4-sec-head h2{font-size:clamp(1.5rem,3.2vw,2.1rem)}
.w4-grid{display:grid;gap:1px;background:var(--line-dk);border:1px solid var(--line-dk);border-radius:6px;overflow:hidden}
@media(min-width:780px){.w4-grid{grid-template-columns:1fr 1fr}}
.w4-card{background:var(--smoked);padding:1.5rem 1.6rem 1.35rem;display:flex;flex-direction:column;gap:.55rem}
.w4-card-head{display:flex;gap:.4rem;flex-wrap:wrap}
.w4-tag{font-family:var(--sans);font-size:.62rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  padding:.28em .6em;border-radius:2px;border:1px solid var(--line-dk);color:var(--silver);background:rgba(244,239,231,.03)}
.w4-tag--sgv{color:var(--champagne);border-color:rgba(197,164,109,.4)}
.w4-tag--kind{color:var(--muted-dk)}
.w4-card h3{font-size:1.28rem;line-height:1.12;margin:.1rem 0 0}
.w4-meta{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.15rem 0 .1rem}
.w4-chip{font-family:var(--sans);font-size:.64rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
  color:var(--obsidian);background:var(--champagne);padding:.32em .7em;border-radius:2px}
.w4-cad{font-family:var(--sans);font-size:.78rem;color:var(--silver)}
.w4-next{font-family:var(--sans);font-size:.8rem;color:var(--pearl)}
.w4-next-k{font-size:.6rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--syrup);margin-right:.3rem}
.w4-vibe{font-size:.96rem;color:var(--silver);line-height:1.5;margin:.15rem 0 .1rem}
.w4-shops{font-size:.85rem;color:var(--silver);margin:.1rem 0}
.w4-shops-k{font-size:.62rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted-dk);margin-right:.35rem}
.w4-shops a{color:var(--pearl);border-bottom:1px solid var(--line-dk)}
.w4-shops a:hover{border-color:var(--champagne)}
.w4-shops .w4-in{color:var(--muted-dk);font-size:.8em}
.w4-links{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;margin-top:auto;padding-top:.5rem}
.w4-src{font-size:.82rem;font-weight:600;color:var(--pearl);border-bottom:1px solid var(--champagne);padding-bottom:1px}
.w4-src:hover{color:#fff}
.w4-ics{font-size:.82rem;color:var(--muted-dk);border-bottom:1px solid var(--line-dk);padding-bottom:1px}
.w4-ics:hover{color:var(--silver)}
.w4-checked{font-size:.7rem;color:var(--muted-dk);margin:.35rem 0 0}
.w4-host{margin-top:clamp(2.4rem,5vw,3.6rem)}
.w4-host .btn{margin-top:1rem}
.w4-faq{margin-top:clamp(2.4rem,5vw,3.6rem);border-top:1px solid var(--line-dk);padding-top:1.6rem}
.w4-faq h3{font-size:1.08rem;margin:1.3rem 0 .3rem}
.w4-faq p{color:var(--silver);font-size:.94rem;max-width:64ch}
.w4-faq a,.w4-host a.link-quiet{color:var(--champagne)}
.w4-calcta{display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between;
  margin-top:1.6rem;border:1px solid rgba(197,164,109,.4);border-radius:6px;padding:1.2rem 1.4rem;
  background:rgba(197,164,109,.05);transition:border-color .16s var(--ease),background .16s var(--ease)}
.w4-calcta:hover{border-color:var(--champagne);background:rgba(197,164,109,.09)}
.w4-calcta-body{display:flex;flex-direction:column;gap:.25rem;max-width:52ch}
.w4-calcta-k{font-family:var(--sans);font-size:.66rem;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--champagne)}
.w4-calcta-t{color:var(--silver);font-size:.92rem;line-height:1.45}
.w4-calcta-go{font-family:var(--sans);font-size:.85rem;font-weight:600;color:var(--pearl);
  border:1px solid var(--line-dk);border-radius:2px;padding:.55rem .9rem;white-space:nowrap}
.w4-calcta:hover .w4-calcta-go{border-color:var(--champagne);color:#fff}
.w4-calcta:focus-visible{outline:2px solid var(--champagne);outline-offset:3px}
"""


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boba Meetups &amp; Clubs in Southern California (2026) | Boba Night</title>
<meta name="description" content="Run clubs, mahjong nights, book clubs, and cupsleeve events that meet at SoCal boba shops. Every listing sourced and linked to the organizer. Boba Night.">
<link rel="canonical" href="https://www.bobanight.com/meetups/">
<meta name="theme-color" content="#0B0C0E">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="text/calendar" title="Boba Night events" href="/meetups/ics/bobanight-events.ics">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/luxury-homepage.css">
<link rel="stylesheet" href="/css/nav-midnight.css">
<style id="w4">{css}</style>
</head>
<body>
{nav}
<main id="main" class="wrap">
<nav class="w4-crumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">/</span><span aria-current="page">Meetups &amp; clubs</span></nav>
<div class="w4-head">
<p class="eyebrow">The social calendar</p>
<h1>Meetups &amp; clubs that run on boba</h1>
<p class="lede">Southern California treats boba shops as third places. Clubs meet in them, crawls route through them, and fandoms take them over for a night. Everything below is a real group with a real public page; <b>details come from each organizer's own listing</b>, so check their page before you go.</p>
<div class="w4-notice"><span class="w4-note-k">Sourced</span>
<span>We list only what an organizer publishes, and we link straight to them. Days and venues change, so the organizer's page is always the truth. A &ldquo;Next&rdquo; date, when shown, is computed from the organizer's stated schedule, not asserted by us. Nothing here is sponsored.</span></div>
</div>
<a class="w4-calcta" href="/meetups/calendar/">
<span class="w4-calcta-body"><span class="w4-calcta-k">The venue calendar</span>
<span class="w4-calcta-t">Every dated meetup laid out month by month, each linked to the shop and the organizer, with .ics files to import.</span></span>
<span class="w4-calcta-go">Open the calendar</span></a>
{sections}
<section class="w4-host" id="host">
<div class="w4-sec-head"><span class="idx">+</span><h2>Run a club? Put your boba stop on the map.</h2></div>
<p class="lede">Real jogging clubs in the 626 end their runs at coffee and beer. As far as we can find, <b>no SoCal run club has a published boba-shop home yet</b>. If yours does, or you're a shop that wants to host one, we'll list it with a link to your page. Listing is free, and we only publish what your own page says.</p>
<a class="btn btn-primary" href="/meetups/submit/">Submit a meetup &#8599;</a>
</section>
<section class="w4-faq" id="faq">
<div class="w4-sec-head"><span class="idx">?</span><h2>FAQ</h2></div>
<h3>How do we know these are real?</h3><p>Every listing links to the organizer's own public page: Meetup, Instagram, Partiful, or an official site. We publish nothing we can't link.</p>
<h3>Are the days and times current?</h3><p>Schedules change without telling us, so we point you at the organizer's page instead of asserting times ourselves. When we show a cadence or a &ldquo;Next&rdquo; date, it's computed from what their page stated at our last check.</p>
<h3>Can I add one to my calendar?</h3><p>Where an organizer publishes a fixed schedule or a dated event, we generate an <code>.ics</code> file you can import. Times follow the organizer, so confirm on their page.</p>
<h3>Meeting someone from an app instead?</h3><p>Different mission, same drinks. Start with the <a href="/#first-meet">First Meet guide</a> on our homepage, then pick a <a href="/best/first-date/">first-meet room</a>.</p>
</section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <span class="wordmark" style="font-size:1.5rem">Boba <b>Night</b><span class="soc">Society</span></span>
        <p style="margin:1rem 0 0;max-width:34ch;color:var(--muted-dk);font-size:.9rem">The night guide to Southern California boba. Menus checked, sources shown, nothing invented.</p>
      </div>
      <div class="foot-col"><h5>Meetups</h5><a href="/meetups/calendar/">The calendar</a><a href="/meetups/#clubs">Social clubs</a><a href="/meetups/#crawls">Crawls &amp; runs</a><a href="/meetups/#fandom">Fandom nights</a><a href="/meetups/submit/">Submit a meetup</a></div>
      <div class="foot-col"><h5>Explore</h5><a href="/directory/">The directory</a><a href="/cities/">Cities</a><a href="/area/sgv/">The 626</a><a href="/area/orange-county/">Orange County</a></div>
      <div class="foot-col"><h5>The Menu</h5><a href="/best/matcha/">Matcha</a><a href="/best/fruit-tea/">Fruit tea</a><a href="/best/brown-sugar/">Brown sugar</a><a href="/best/non-dairy/">Dairy-free</a></div>
    </div>
    <div class="foot-bottom"><span>&copy; {year} Boba Night Society · Southern California</span><span>Listings checked per organizer · No paid placement · <a href="/meetups/submit/" style="color:var(--silver)">Submit a meetup</a></span></div>
  </div>
</footer>
<script src="/js/nav-midnight.js" defer></script>
{ld}
</body>
</html>
"""


# ---------------------------------------------------------------- date helpers
def within_window(nd, today, days):
    return nd is not None and today <= nd <= today + timedelta(days=days)


def fmt_num_date(d):
    """(mon_upper, day_int, weekday_upper) e.g. ('JUL', 23, 'THU')."""
    return d.strftime("%b").upper(), d.day, d.strftime("%a").upper()


def events_today(series_list, today):
    """Series with a REAL dated event landing exactly on `today`.
    A materialized occurrence dated today, or an rrule that fires today.
    Never invents. Returns list of (series, basis)."""
    hits = []
    for s in series_list:
        on_today = False
        basis = None
        for occ in s.get("occurrences", []):
            try:
                d = datetime.strptime(occ["date"], "%Y-%m-%d").date()
            except (KeyError, ValueError):
                continue
            if d == today:
                on_today, basis = True, "occurrence"
                break
        if not on_today:
            parts = parse_rrule(s.get("cadence_rrule"))
            if parts.get("FREQ") == "WEEKLY" and "BYDAY" in parts:
                targets = [WEEKDAY_CODE[d] for d in parts["BYDAY"].split(",")
                           if d in WEEKDAY_CODE]
                if today.weekday() in targets:
                    on_today, basis = True, "rrule"
        if on_today:
            hits.append((s, basis))
    return hits


def venue_html(s, shop_index, cls="cal-venue"):
    """Linked directory shop when a real association exists, else the plain
    host-venue text. Never fabricates a link."""
    for slug in s.get("shop_slugs", []):
        shop = shop_index.get(slug)
        if shop:
            return (f'<a class="{cls}" href="{esc(shop_profile_url(shop))}">'
                    f'{esc(shop["name"])}'
                    f'<span class="cal-city">{esc(shop["city"])}</span></a>')
    if s.get("host_venues"):
        return (f'<span class="{cls} {cls}--plain">'
                f'{esc(s["host_venues"][0])}</span>')
    return ""


def basis_note(basis):
    if basis == "occurrence":
        return "Confirmed date on the organizer&rsquo;s page."
    if basis == "rrule":
        return "From the organizer&rsquo;s published weekly schedule; confirm before you go."
    return ""


# ------------------------------------------------------- homepage "This week"
def render_day_card(s, shop_index, today):
    nd, basis = compute_next(s, today)
    mo, day, wd = fmt_num_date(nd)
    chip = cadence_chip(s)
    kind = KIND_LABEL.get(s["kind"], s["kind"].title())
    vh = venue_html(s, shop_index, "cal-venue")

    meta = []
    if chip:
        meta.append(f'<span class="cal-chip">{esc(chip)}</span>')
    elif s.get("cadence_text"):
        meta.append(f'<span class="cal-cad">{esc(s["cadence_text"])}</span>')

    parts = ['<article class="cal-card">']
    parts.append(
        f'<div class="cal-date" aria-hidden="true"><span class="cal-mo">{mo}</span>'
        f'<span class="cal-num">{day}</span><span class="cal-wd">{wd}</span></div>'
    )
    parts.append('<div class="cal-body">')
    parts.append(f'<span class="cal-kind">{esc(kind)}</span>')
    parts.append(
        f'<h3 class="cal-title">{esc(s["title"])} '
        f'<span class="cal-sr">on {wd} {mo} {day}</span></h3>'
    )
    if vh:
        parts.append(vh)
    if meta:
        parts.append('<div class="cal-meta">' + "".join(meta) + "</div>")
    parts.append(
        f'<a class="cal-org" href="{esc(s["host_url"])}" rel="noopener" '
        f'target="_blank">{esc(s["host_name"])}</a>'
    )
    parts.append(f'<p class="cal-basis">{basis_note(basis)}</p>')
    parts.append("</div></article>")
    return "".join(parts)


def render_regular_row(series_list, today):
    """Standing clubs shown as cadence, never a date. Used as the honest
    fallback and as quiet context under the dated cards."""
    items = []
    for s in series_list:
        cad = s.get("cadence_text") or cadence_chip(s)
        items.append(
            f'<li><a class="cal-reg-t" href="{esc(s["host_url"])}" rel="noopener" '
            f'target="_blank">{esc(s["title"])}</a>'
            f'<span class="cal-reg-cad">{esc(cad)}</span></li>'
        )
    if not items:
        return ""
    return ('<div class="cal-reg"><p class="cal-reg-k">Regular meetups</p>'
            '<ul class="cal-reg-list">' + "".join(items) + "</ul></div>")


def render_homepage_strip(series_list, shop_index, today):
    this_week = [s for s in series_list
                 if within_window(compute_next(s, today)[0], today, STRIP_WINDOW_DAYS)]
    this_week.sort(key=lambda s: compute_next(s, today)[0])
    regular = [s for s in series_list if s not in this_week]

    if this_week:
        heading = "On the calendar this week"
        lede = ("Real clubs and crawls that meet at Southern California boba shops. "
                "Dates below are computed from each organizer&rsquo;s own page or their "
                "published schedule, never invented.")
        cards = "".join(render_day_card(s, shop_index, today) for s in this_week)
        body = f'<div class="cal-strip-grid">{cards}</div>'
        body += render_regular_row(regular, today)
    else:
        heading = "Meetups that run on boba"
        lede = ("No club has a dated meetup on its page for the next seven days, so "
                "here are the standing groups and how often they gather. We show a date "
                "only when an organizer publishes one.")
        body = render_regular_row(series_list, today)

    return f"""
  <section class="sx" id="social-calendar" aria-label="The social calendar">
    <div class="wrap">
      <div class="boba-divider reveal"></div>
      <div class="section-head reveal"><p class="eyebrow">The social calendar</p>
        <h2>{heading}</h2><p class="lede">{lede}</p></div>
      <div class="reveal">{body}</div>
      <div class="cal-strip-foot reveal">
        <a class="btn btn-line" href="/meetups/">See all meetups &amp; clubs</a>
        <a class="btn btn-line" href="/meetups/calendar/">Open the venue calendar</a>
      </div>
    </div>
  </section>
  <style id="social-calendar-css">{STRIP_CSS}</style>"""


STRIP_CSS = """
#social-calendar .cal-strip-grid{display:grid;gap:1px;background:var(--line-dk);
  border:1px solid var(--line-dk);border-radius:6px;overflow:hidden;margin-bottom:1.4rem;
  grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
#social-calendar .cal-card{background:var(--smoked);padding:1.35rem 1.5rem;display:flex;gap:1.2rem;align-items:flex-start}
#social-calendar .cal-date{flex:none;width:4.2rem;text-align:center;border:1px solid var(--line-dk);
  border-radius:3px;padding:.55rem 0 .5rem;background:rgba(244,239,231,.02)}
#social-calendar .cal-mo{display:block;font-family:var(--sans);font-size:.6rem;font-weight:600;
  letter-spacing:.16em;color:var(--champagne)}
#social-calendar .cal-num{display:block;font-family:var(--serif);font-size:2.4rem;line-height:1;
  font-weight:400;color:var(--pearl);margin:.05rem 0}
#social-calendar .cal-wd{display:block;font-family:var(--sans);font-size:.6rem;font-weight:600;
  letter-spacing:.16em;color:var(--muted-dk)}
#social-calendar .cal-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:.4rem}
#social-calendar .cal-kind{font-family:var(--sans);font-size:.62rem;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted-dk)}
#social-calendar .cal-title{font-size:1.2rem;line-height:1.15;margin:0}
#social-calendar .cal-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
#social-calendar .cal-venue{font-size:.86rem;color:var(--pearl);border-bottom:1px solid var(--line-dk);
  align-self:flex-start;padding-bottom:1px;transition:border-color .16s var(--ease)}
#social-calendar .cal-venue:hover{border-color:var(--champagne)}
#social-calendar .cal-venue--plain{color:var(--silver);border:0}
#social-calendar .cal-city{color:var(--muted-dk);font-size:.82em;margin-left:.4rem}
#social-calendar .cal-meta{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}
#social-calendar .cal-chip{font-family:var(--sans);font-size:.6rem;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--obsidian);background:var(--champagne);padding:.3em .65em;border-radius:2px}
#social-calendar .cal-cad{font-family:var(--sans);font-size:.8rem;color:var(--silver)}
#social-calendar .cal-org{font-size:.82rem;font-weight:600;color:var(--pearl);
  border-bottom:1px solid var(--champagne);align-self:flex-start;padding-bottom:1px}
#social-calendar .cal-org:hover{color:#fff}
#social-calendar .cal-basis{font-size:.72rem;color:var(--muted-dk);margin:.1rem 0 0}
#social-calendar .cal-reg{border:1px solid var(--line-dk);border-radius:6px;padding:1.1rem 1.4rem;background:var(--smoked)}
#social-calendar .cal-reg-k{font-family:var(--sans);font-size:.66rem;font-weight:600;letter-spacing:.16em;
  text-transform:uppercase;color:var(--champagne);margin:0 0 .7rem}
#social-calendar .cal-reg-list{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}
@media(min-width:720px){#social-calendar .cal-reg-list{grid-template-columns:1fr 1fr;gap:.6rem 2rem}}
#social-calendar .cal-reg-list li{display:flex;flex-direction:column;gap:.1rem;border-left:2px solid var(--line-dk);padding-left:.7rem}
#social-calendar .cal-reg-t{font-size:.92rem;font-weight:600;color:var(--pearl)}
#social-calendar .cal-reg-t:hover{color:#fff}
#social-calendar .cal-reg-cad{font-size:.78rem;color:var(--muted-dk)}
#social-calendar .cal-strip-foot{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.4rem}
#social-calendar a:focus-visible,#social-calendar .btn:focus-visible{outline:2px solid var(--champagne);outline-offset:3px;border-radius:2px}
"""


# -------------------------------------------------------------- "Tonight" toast
def render_toast(series_list, shop_index, today):
    """A small dismissible toast ONLY when a real event lands today. Empty string
    otherwise, so the homepage never fabricates a 'Tonight'."""
    hits = events_today(series_list, today)
    if not hits:
        return ""
    s, basis = hits[0]
    # venue phrase: real shop name, else host venue text
    where = ""
    for slug in s.get("shop_slugs", []):
        shop = shop_index.get(slug)
        if shop:
            where = shop["name"]
            break
    if not where and s.get("host_venues"):
        where = s["host_venues"][0]
    where_txt = f" at {esc(where)}" if where else ""
    href = "/meetups/calendar/"
    key = f"bn_tonight_{today.isoformat()}"
    return f"""
<div class="bn-tonight boba-surprise" id="bnTonight" role="status" aria-live="polite" data-key="{key}" hidden>
  <span class="bn-tnt-k">Tonight</span>
  <p class="bn-tnt-msg">{esc(s["title"])}{where_txt}</p>
  <a class="bn-tnt-link" href="{href}">See the calendar</a>
  <button class="bn-tnt-x" type="button" aria-label="Dismiss tonight&rsquo;s note">&times;</button>
</div>
<style id="bn-tonight-css">
.bn-tonight{{position:fixed;left:1rem;bottom:1rem;z-index:60;max-width:22rem;
  display:flex;flex-wrap:wrap;align-items:center;gap:.5rem .8rem;
  background:var(--smoked);border:1px solid var(--line-dk);border-radius:4px;
  padding:.85rem 1rem;box-shadow:0 8px 30px rgba(0,0,0,.5)}}
.bn-tonight.bn-tnt-in{{animation:bn-tnt-rise .22s var(--ease) both}}
@keyframes bn-tnt-rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.bn-tnt-k{{font-family:var(--sans);font-size:.6rem;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--champagne)}}
.bn-tnt-msg{{flex:1 1 100%;font-size:.9rem;color:var(--pearl);margin:0;line-height:1.35}}
.bn-tnt-link{{font-size:.8rem;font-weight:600;color:var(--pearl);border-bottom:1px solid var(--champagne);padding-bottom:1px}}
.bn-tnt-link:hover{{color:#fff}}
.bn-tnt-x{{margin-left:auto;background:none;border:0;color:var(--muted-dk);font-size:1.2rem;
  line-height:1;cursor:pointer;padding:.1rem .3rem}}
.bn-tnt-x:hover{{color:var(--pearl)}}
.bn-tonight:focus-within,.bn-tnt-x:focus-visible,.bn-tnt-link:focus-visible{{outline:2px solid var(--champagne);outline-offset:2px}}
@media(prefers-reduced-motion:reduce){{.bn-tonight.bn-tnt-in{{animation:none}}}}
</style>
<script>
(function(){{
  var el=document.getElementById('bnTonight');
  if(!el)return;
  var key=el.getAttribute('data-key');
  try{{if(localStorage.getItem(key)==='1'){{el.parentNode.removeChild(el);return;}}}}catch(e){{}}
  el.hidden=false;el.classList.add('bn-tnt-in');
  try{{if(window.BobaSound&&window.BobaSound.enabled)window.BobaSound.chime('reveal');}}catch(e){{}}
  el.querySelector('.bn-tnt-x').addEventListener('click',function(){{
    try{{if(window.BobaSound&&window.BobaSound.enabled)window.BobaSound.pop();}}catch(e){{}}
    el.style.transition='opacity .18s,transform .18s';el.style.opacity='0';el.style.transform='translateY(8px)';
    try{{localStorage.setItem(key,'1');}}catch(e){{}}
    setTimeout(function(){{if(el.parentNode)el.parentNode.removeChild(el);}},200);
  }});
}})();
</script>"""


# -------------------------------------------------------------- venue calendar
def collect_agenda(series_list, shop_index, today, window_days):
    """Dated entries in the forward window. Materialized occurrences (confirmed)
    plus rrule projections (recurring, from a published schedule). No guesses."""
    end = today + timedelta(days=window_days)
    entries = []
    for s in series_list:
        for occ in s.get("occurrences", []):
            try:
                d = datetime.strptime(occ["date"], "%Y-%m-%d").date()
            except (KeyError, ValueError):
                continue
            if today <= d <= end:
                entries.append({"date": d, "series": s, "basis": "occurrence",
                                "url": occ.get("url") or s.get("host_url", "")})
        parts = parse_rrule(s.get("cadence_rrule"))
        if parts.get("FREQ") == "WEEKLY" and "BYDAY" in parts:
            targets = [WEEKDAY_CODE[c] for c in parts["BYDAY"].split(",")
                       if c in WEEKDAY_CODE]
            dd = today
            while dd <= end:
                if dd.weekday() in targets:
                    entries.append({"date": dd, "series": s, "basis": "rrule",
                                    "url": s.get("host_url", "")})
                dd += timedelta(days=1)
    entries.sort(key=lambda e: (e["date"], e["series"]["title"]))
    return entries


def render_agenda_entry(e, shop_index, today):
    s = e["series"]
    chip = cadence_chip(s)
    kind = KIND_LABEL.get(s["kind"], s["kind"].title())
    vh = venue_html(s, shop_index, "cal-venue")
    tag = ("Recurring" if e["basis"] == "rrule" else "Confirmed")
    tag_cls = "cal-ag-tag--rrule" if e["basis"] == "rrule" else "cal-ag-tag--occ"
    time_txt = fmt_time_12h(s.get("start_time")) if e["basis"] == "rrule" else ""
    links = [
        f'<a class="cal-org" href="{esc(e["url"])}" rel="noopener" target="_blank">'
        f'{esc(s["host_name"])}</a>'
    ]
    if has_dates(s):
        links.append(f'<a class="cal-ics" href="/meetups/ics/{esc(s["slug"])}.ics">'
                     f'Add to calendar (.ics)</a>')
    meta = []
    if chip:
        meta.append(f'<span class="cal-chip">{esc(chip)}</span>')
    elif time_txt:
        meta.append(f'<span class="cal-cad">{esc(time_txt)}</span>')
    parts = ['<div class="cal-ag-row">']
    parts.append(f'<span class="cal-ag-tag {tag_cls}">{tag}</span>')
    parts.append('<div class="cal-ag-body">')
    parts.append(f'<span class="cal-kind">{esc(kind)}</span>')
    parts.append(f'<h3 class="cal-ag-title">{esc(s["title"])}</h3>')
    if vh:
        parts.append(vh)
    if meta:
        parts.append('<div class="cal-meta">' + "".join(meta) + "</div>")
    parts.append('<div class="cal-ag-links">' + "".join(links) + "</div>")
    parts.append("</div></div>")
    return "".join(parts)


def render_calendar_agenda(series_list, shop_index, today, window_days):
    entries = collect_agenda(series_list, shop_index, today, window_days)
    end = today + timedelta(days=window_days)

    # group by (year, month) -> {date -> [entries]}
    by_month = {}
    for e in entries:
        ym = (e["date"].year, e["date"].month)
        by_month.setdefault(ym, {}).setdefault(e["date"], []).append(e)

    # iterate every month spanned by the window so empty months read plainly
    months = []
    y, m = today.year, today.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1

    out = []
    for ym in months:
        y, m = ym
        label = date(y, m, 1).strftime("%B %Y")
        out.append(f'<section class="cal-month"><h2 class="cal-month-h">{label}</h2>')
        days = by_month.get(ym)
        if not days:
            out.append('<p class="cal-empty">No dated events listed this month. '
                       'Standing clubs still gather, see their cadence below.</p>')
        else:
            for d in sorted(days):
                mo, dn, wd = fmt_num_date(d)
                rows = "".join(render_agenda_entry(e, shop_index, today)
                               for e in days[d])
                out.append(
                    '<div class="cal-day">'
                    f'<div class="cal-day-date"><span class="cal-mo">{mo}</span>'
                    f'<span class="cal-num">{dn}</span>'
                    f'<span class="cal-wd">{wd}</span></div>'
                    f'<div class="cal-day-rows">{rows}</div></div>'
                )
        out.append("</section>")
    return "".join(out)


def render_calendar_page(events, shop_index, today):
    nav = load_nav()
    series = events["series"]
    agenda = render_calendar_agenda(series, shop_index, today, CALENDAR_WINDOW_DAYS)
    standing = [s for s in series if not has_dates(s)]
    standing_html = ""
    if standing:
        items = "".join(
            f'<li><a class="cal-reg-t" href="{esc(s["host_url"])}" rel="noopener" '
            f'target="_blank">{esc(s["title"])}</a>'
            f'<span class="cal-reg-cad">{esc(s.get("cadence_text",""))}</span></li>'
            for s in standing
        )
        standing_html = (
            '<section class="cal-standing"><h2 class="cal-month-h">'
            'Standing clubs, dates posted ad hoc</h2>'
            '<p class="cal-standing-lede">These groups meet on their own rhythm and '
            'post each gathering when it is set. No fixed calendar date, so we link you '
            'straight to their page.</p>'
            f'<ul class="cal-reg-list">{items}</ul></section>'
        )

    ld_nodes = event_ld_nodes(series, shop_index)
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Meetups & clubs",
             "item": SITE + "/meetups/"},
            {"@type": "ListItem", "position": 3, "name": "Calendar",
             "item": SITE + "/meetups/calendar/"},
        ],
    }
    ld_blocks = [json.dumps(breadcrumb, ensure_ascii=False)]
    for node in ld_nodes:
        nf = {"@context": "https://schema.org"}
        nf.update(node)
        ld_blocks.append(json.dumps(nf, ensure_ascii=False))
    ld_html = "\n".join(
        f'<script type="application/ld+json">\n{b}\n</script>' for b in ld_blocks
    )
    window_end = today + timedelta(days=CALENDAR_WINDOW_DAYS)
    range_txt = f"{today.strftime('%b %-d')} to {window_end.strftime('%b %-d, %Y')}"
    return CALENDAR_TEMPLATE.format(
        nav=nav, css=CALENDAR_CSS, agenda=agenda, standing=standing_html,
        ld=ld_html, year=today.year, range_txt=range_txt,
    )


CALENDAR_CSS = """
.cal-crumb{font-family:var(--sans);font-size:.78rem;letter-spacing:.02em;color:var(--muted-dk);
  display:flex;gap:.5rem;align-items:center;padding:1.6rem 0 0}
.cal-crumb a{color:var(--muted-dk)}.cal-crumb a:hover{color:var(--pearl)}
.cal-crumb .sep{opacity:.5}
.cal-head{padding:2.2rem 0 1rem;max-width:62ch}
.cal-head h1{font-size:clamp(2.2rem,5.4vw,3.6rem);margin:.3rem 0 1rem}
.cal-notice{display:flex;gap:.8rem;align-items:flex-start;border:1px solid var(--line-dk);
  border-radius:3px;padding:1rem 1.2rem;margin:1.4rem 0 0;background:rgba(244,239,231,.03);
  font-size:.9rem;color:var(--silver)}
.cal-notice .cal-note-k{font-size:.66rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;
  color:var(--champagne);white-space:nowrap;padding-top:.15rem}
.cal-range{font-family:var(--sans);font-size:.72rem;font-weight:600;letter-spacing:.16em;
  text-transform:uppercase;color:var(--champagne);margin:0 0 .3rem}
.cal-month{padding:clamp(1.8rem,4vw,2.6rem) 0 0}
.cal-month-h{font-size:clamp(1.4rem,3vw,1.9rem);border-bottom:1px solid var(--line-dk);
  padding-bottom:.7rem;margin-bottom:1.2rem}
.cal-empty{color:var(--muted-dk);font-size:.92rem;padding:.2rem 0 .4rem}
.cal-day{display:grid;grid-template-columns:4.2rem 1fr;gap:1.2rem;padding:.9rem 0;border-bottom:1px solid var(--line-dk)}
.cal-day:last-child{border-bottom:0}
.cal-day-date{text-align:center;border:1px solid var(--line-dk);border-radius:3px;
  padding:.5rem 0;height:max-content;background:rgba(244,239,231,.02)}
.cal-mo{display:block;font-family:var(--sans);font-size:.6rem;font-weight:600;letter-spacing:.16em;color:var(--champagne)}
.cal-num{display:block;font-family:var(--serif);font-size:2rem;line-height:1;color:var(--pearl);margin:.05rem 0}
.cal-wd{display:block;font-family:var(--sans);font-size:.58rem;font-weight:600;letter-spacing:.16em;color:var(--muted-dk)}
.cal-day-rows{display:flex;flex-direction:column;gap:1px;background:var(--line-dk);border:1px solid var(--line-dk);border-radius:5px;overflow:hidden}
.cal-ag-row{background:var(--smoked);padding:1rem 1.2rem;display:flex;gap:1rem;align-items:flex-start}
.cal-ag-tag{flex:none;font-family:var(--sans);font-size:.58rem;font-weight:600;letter-spacing:.12em;
  text-transform:uppercase;padding:.3em .6em;border-radius:2px;border:1px solid var(--line-dk);margin-top:.15rem}
.cal-ag-tag--rrule{color:var(--silver)}
.cal-ag-tag--occ{color:var(--champagne);border-color:rgba(197,164,109,.4)}
.cal-ag-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:.35rem}
.cal-kind{font-family:var(--sans);font-size:.62rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted-dk)}
.cal-ag-title{font-size:1.12rem;line-height:1.15;margin:0}
.cal-venue{font-size:.86rem;color:var(--pearl);border-bottom:1px solid var(--line-dk);align-self:flex-start;padding-bottom:1px;transition:border-color .16s var(--ease)}
.cal-venue:hover{border-color:var(--champagne)}
.cal-venue--plain{color:var(--silver);border:0}
.cal-city{color:var(--muted-dk);font-size:.82em;margin-left:.4rem}
.cal-meta{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}
.cal-chip{font-family:var(--sans);font-size:.6rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  color:var(--obsidian);background:var(--champagne);padding:.3em .65em;border-radius:2px}
.cal-cad{font-family:var(--sans);font-size:.8rem;color:var(--silver)}
.cal-ag-links{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;margin-top:.15rem}
.cal-org{font-size:.82rem;font-weight:600;color:var(--pearl);border-bottom:1px solid var(--champagne);padding-bottom:1px}
.cal-org:hover{color:#fff}
.cal-ics{font-size:.82rem;color:var(--muted-dk);border-bottom:1px solid var(--line-dk);padding-bottom:1px}
.cal-ics:hover{color:var(--silver)}
.cal-standing{margin-top:clamp(2.4rem,5vw,3.6rem);border-top:1px solid var(--line-dk);padding-top:1.6rem}
.cal-standing-lede{color:var(--silver);font-size:.94rem;max-width:64ch;margin:.2rem 0 1.2rem}
.cal-reg-list{list-style:none;margin:0;padding:0;display:grid;gap:.7rem}
@media(min-width:720px){.cal-reg-list{grid-template-columns:1fr 1fr;gap:.8rem 2rem}}
.cal-reg-list li{display:flex;flex-direction:column;gap:.1rem;border-left:2px solid var(--line-dk);padding-left:.75rem}
.cal-reg-t{font-size:.94rem;font-weight:600;color:var(--pearl)}.cal-reg-t:hover{color:#fff}
.cal-reg-cad{font-size:.8rem;color:var(--muted-dk)}
.cal-foot{margin-top:clamp(2.4rem,5vw,3.6rem);display:flex;flex-wrap:wrap;gap:.7rem}
main a:focus-visible,main .btn:focus-visible{outline:2px solid var(--champagne);outline-offset:3px;border-radius:2px}
"""


CALENDAR_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boba Meetup Calendar: Scheduled Events at SoCal Boba Shops | Boba Night</title>
<meta name="description" content="A month-by-month calendar of dated boba meetups across Southern California. Every date links to the venue profile and the organizer, with .ics files to import. Boba Night.">
<link rel="canonical" href="https://www.bobanight.com/meetups/calendar/">
<meta name="theme-color" content="#0B0C0E">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="robots" content="index,follow">
<link rel="alternate" type="text/calendar" title="Boba Night events" href="/meetups/ics/bobanight-events.ics">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/luxury-homepage.css">
<link rel="stylesheet" href="/css/nav-midnight.css">
<link rel="stylesheet" href="/css/motif.css">
<link rel="stylesheet" href="/css/sound.css">
<style id="cal">{css}</style>
</head>
<body>
{nav}
<main id="main" class="wrap">
<nav class="cal-crumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">/</span><a href="/meetups/">Meetups &amp; clubs</a><span class="sep">/</span><span aria-current="page">Calendar</span></nav>
<div class="cal-head">
<p class="eyebrow">The venue calendar</p>
<h1>The boba meetup calendar</h1>
<p class="lede">Every dated gathering we can stand behind, grouped by the day it lands. Each entry links to the shop in our directory and to the organizer&rsquo;s own page. Times and days follow the organizer, so confirm before you go.</p>
<div class="cal-notice"><span class="cal-note-k">How dates work</span>
<span>A <b>Confirmed</b> tag marks a one-off date an organizer posted. A <b>Recurring</b> tag marks a day computed from a published weekly schedule, not a date we invented. Groups without a fixed schedule appear at the bottom with a link to their page.</span></div>
</div>
<p class="cal-range">Showing {range_txt}</p>
{agenda}
{standing}
<div class="cal-foot">
<a class="btn btn-line" href="/meetups/">Back to meetups &amp; clubs</a>
<a class="btn btn-line" href="/meetups/ics/bobanight-events.ics">Subscribe to every date (.ics)</a>
</div>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col">
        <span class="wordmark" style="font-size:1.5rem">Boba <b>Night</b><span class="soc">Society</span></span>
        <p style="margin:1rem 0 0;max-width:34ch;color:var(--muted-dk);font-size:.9rem">The night guide to Southern California boba. Menus checked, sources shown, nothing invented.</p>
      </div>
      <div class="foot-col"><h5>Meetups</h5><a href="/meetups/">All meetups</a><a href="/meetups/calendar/">The calendar</a><a href="/meetups/#clubs">Social clubs</a><a href="/meetups/submit/">Submit a meetup</a></div>
      <div class="foot-col"><h5>Explore</h5><a href="/directory/">The directory</a><a href="/cities/">Cities</a><a href="/area/sgv/">The 626</a><a href="/area/orange-county/">Orange County</a></div>
      <div class="foot-col"><h5>The Menu</h5><a href="/best/matcha/">Matcha</a><a href="/best/fruit-tea/">Fruit tea</a><a href="/best/brown-sugar/">Brown sugar</a><a href="/best/non-dairy/">Dairy-free</a></div>
    </div>
    <div class="foot-bottom"><span>&copy; {year} Boba Night Society &middot; Southern California</span><span>Dates per each organizer &middot; No paid placement &middot; <a href="/meetups/submit/" style="color:var(--silver)">Submit a meetup</a></span></div>
  </div>
</footer>
<script src="/js/nav-midnight.js" defer></script>
<script src="/js/motif.js" defer></script>
<script src="/js/sound.js" defer></script>
{ld}
</body>
</html>
"""


# ----------------------------------------------------------- marker splicing
def write_between_markers(path, start, end, content):
    """Replace text between two HTML-comment markers in `path`. Returns True on
    success. Leaves the file untouched (and warns) if markers are missing."""
    with open(path, encoding="utf-8") as f:
        html_txt = f.read()
    a = html_txt.find(start)
    b = html_txt.find(end)
    if a == -1 or b == -1 or b < a:
        print(f"  WARNING: markers {start!r}/{end!r} not found in {path}; skipped")
        return False
    a_end = a + len(start)
    new = html_txt[:a_end] + content + "\n  " + html_txt[b:]
    if new != html_txt:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return True


# --------------------------------------------------------------------------- main
def main():
    events = load_json(EVENTS_JSON)
    stores = load_json(STORES_JSON)
    shop_index = build_shop_index(stores)
    series = events["series"]
    today = date.today()

    os.makedirs(ICS_DIR, exist_ok=True)

    # (a) meetups/index.html
    html_out = render_html(events, shop_index, today)
    with open(MEETUPS_HTML, "w", encoding="utf-8") as f:
        f.write(html_out)

    # (a2) meetups/calendar/index.html
    os.makedirs(os.path.dirname(CALENDAR_HTML), exist_ok=True)
    cal_out = render_calendar_page(events, shop_index, today)
    with open(CALENDAR_HTML, "w", encoding="utf-8") as f:
        f.write(cal_out)

    # (a3) homepage "This week" strip + "Tonight" toast, spliced into index.html
    strip_html = render_homepage_strip(series, shop_index, today)
    strip_ok = write_between_markers(
        INDEX_HTML, "<!-- BUILD:EVENTS-STRIP:START -->",
        "<!-- BUILD:EVENTS-STRIP:END -->", strip_html)
    toast_html = render_toast(series, shop_index, today)
    toast_ok = write_between_markers(
        INDEX_HTML, "<!-- BUILD:EVENTS-TOAST:START -->",
        "<!-- BUILD:EVENTS-TOAST:END -->", toast_html)
    today_hits = events_today(series, today)

    # (b) build/shop-events.json
    shop_events = build_shop_events(series, shop_index, today)
    with open(SHOP_EVENTS, "w", encoding="utf-8") as f:
        json.dump(shop_events, f, ensure_ascii=False, indent=2)

    # (c) per-series .ics + aggregate
    stamp = dtstamp_utc()
    all_groups = []
    ics_written = 0
    for s in series:
        groups = vevent_for_series(s, shop_index, stamp)
        if not groups:
            continue
        cal = wrap_calendar(groups, f"Boba Night — {s['title']}")
        with open(os.path.join(ICS_DIR, f"{s['slug']}.ics"), "w",
                  encoding="utf-8", newline="") as f:
            f.write(cal)
        ics_written += 1
        all_groups.extend(groups)
    agg = wrap_calendar(all_groups, "Boba Night — all events")
    with open(os.path.join(ICS_DIR, "bobanight-events.ics"), "w",
              encoding="utf-8", newline="") as f:
        f.write(agg)

    # report
    ld_count = len(event_ld_nodes(series, shop_index))
    this_week = [s for s in series
                 if within_window(compute_next(s, today)[0], today, STRIP_WINDOW_DAYS)]
    print(f"gen_events: {len(series)} series")
    print(f"  meetups/index.html written")
    print(f"  meetups/calendar/index.html written")
    print(f"  index.html strip spliced: {strip_ok} "
          f"({len(this_week)} dated this week: "
          f"{[compute_next(s, today)[0].isoformat()+' '+s['slug'] for s in this_week]})")
    print(f"  index.html toast spliced: {toast_ok} "
          f"(events today {today.isoformat()}: {[s['slug'] for s, _ in today_hits]})")
    print(f"  shop-events.json: {len(shop_events)} shops mapped -> "
          f"{sorted(shop_events)}")
    print(f"  .ics: {ics_written} per-series + 1 aggregate "
          f"({len(all_groups)} VEVENTs)")
    print(f"  Event JSON-LD nodes (materialized occurrences only): {ld_count}")


if __name__ == "__main__":
    main()
