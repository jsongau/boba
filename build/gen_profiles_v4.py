#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boba Night — profile-v4 batch generator (rebuilt; the original was never committed).

Regenerates the profile-v4 shop page for every OPEN shop from Supabase, matching the
live template (hero Google rating, Quick Facts entity block + price + tonight, hours
table, night map, corridor, nearby cities, order rail, share, JSON-LD). Chrome
(header/nav/footer/scripts) is reused byte-for-byte from an existing v4 page.

    python3 build/gen_profiles_v4.py --dry-run          # report only
    python3 build/gen_profiles_v4.py --slug <slug>      # one shop (writes)
    python3 build/gen_profiles_v4.py --limit 20         # first 20 (writes)
    python3 build/gen_profiles_v4.py                    # all open shops (writes)

NETWORK REQUIRED (Supabase) — run on the Mac. Verification hook: env NBV4_SAMPLE=<json>
uses that row list instead of fetching. Env NBV4_CHROME=<v4 html path> picks the chrome
source (defaults to the first existing v4 page found).

Locked: never regenerates the hand-edited Taro Yuan page.
"""
import json, os, re, sys, math, html, urllib.parse, urllib.request
from collections import defaultdict, Counter

SB   = "https://hfvbeqlefwwjlrbyxpbj.supabase.co"
KEY  = "sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.bobanight.com"
STAMP = "July 20, 2026"
SKIP_SLUGS = {"taro-yuan-city-of-industry"}
COLS = ("slug,name,city,county,state,address,zip,store_type,is_featured,status,phone,website,"
        "latitude,longitude,google_place_id,google_rating,google_review_count,price_level,"
        "seed_verify_needed,hours")

DAYS_MON = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]  # i=0..6 (Google order)
DOW_NAME = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]  # index by day int

# ---------------------------------------------------------------- helpers ----
def esc(s):  return html.escape("" if s is None else str(s), quote=True)
def uq(s):   return urllib.parse.quote("" if s is None else str(s), safe="")
def hh(u):   return u.replace("&", "&amp;")
def nbsp(s): return (s or "").replace(" ", "&nbsp;")

def slugify(s):
    s = re.sub(r"[’']", "", (s or "").lower())
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def fnum(v):
    try:    return float(v)
    except (TypeError, ValueError): return None

def fmt_mi(mi):
    r = round(float(mi), 1)
    return str(int(r)) if r == int(r) else f"{r:.1f}"

def haversine(a, b, c, d):
    R = 3958.7613
    p1, p2 = math.radians(a), math.radians(c)
    dp, dl = math.radians(c - a), math.radians(d - b)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(min(1, math.sqrt(x)))

SGV_CITIES = {"Arcadia","Covina","Pasadena","Walnut","Rowland Heights","Monterey Park",
    "City of Industry","El Monte","Diamond Bar","Rosemead","San Gabriel","Baldwin Park",
    "Temple City","Monrovia","Alhambra","South El Monte","Hacienda Heights","West Covina",
    "San Dimas","La Puente","Montebello","Duarte","Glendora","Azusa"}
REGION_LABEL = {"las-vegas":"Las Vegas Valley","sgv":"San Gabriel Valley","greater-la":"Greater LA","orange-county":"Orange County",
                "san-diego":"San Diego","inland-empire":"Inland Empire"}
def st_ab(state):
    return {"California": "CA", "Nevada": "NV"}.get((state or "California").strip() or "California", "CA")

def region_slug(county, city):
    c = (county or "").replace(" County","").strip()
    if c == "Clark": return "las-vegas"
    if c == "Orange": return "orange-county"
    if c == "San Diego": return "san-diego"
    if c in ("Riverside","San Bernardino"): return "inland-empire"
    if c == "Los Angeles": return "sgv" if city in SGV_CITIES else "greater-la"
    return "greater-la"

def type_bits(t):
    if (t or "").lower() == "chain":
        return dict(tag_cls="tag-chain", tag="Chain", herosub="Chain location",
                    ent="a chain location", qf="Chain tea shop", aside="Chain", mp="mp-chain")
    return dict(tag_cls="tag-orig", tag="Original", herosub="Independent tea house",
                ent="an independent tea house", qf="Independent tea house", aside="Specialty", mp="mp-orig")

PRICE = {1:"$ &middot; Inexpensive", 2:"$$ &middot; Moderate", 3:"$$$ &middot; Expensive", 4:"$$$$ &middot; Expensive"}

def monogram(name):
    for ch in (name or ""):
        if ch.isalnum(): return ch.upper()
    return "B"

def maps_href(name, addr, city, st="CA"):
    clean = re.sub(r"[^0-9A-Za-z ]", " ", name or "")   # live pages strip punctuation from the maps query
    return "https://www.google.com/maps/search/?api=1&query=" + uq(f"{clean} {addr} {city} {st}")

def t12(hhmm):
    """'1900'->'7:00 PM', '0000'->'12:00 AM', '1200'->'12:00 PM'."""
    h, m = int(hhmm[:2]), int(hhmm[2:])
    ap = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d}&nbsp;{ap}"

def periods_by_day(periods):
    """day int -> list of (open,close) HHMM, in Google's period shape."""
    by = defaultdict(list)
    for p in periods or []:
        o, c = p.get("open"), p.get("close")
        if not o or not c: continue
        by[o["day"]].append((o["time"], c["time"]))
    return by

def data_per(periods):
    out = []
    for p in periods or []:
        o, c = p.get("open"), p.get("close")
        if not o or not c: continue
        out.append([o["day"], o["time"], c["day"], c["time"]])
    return out

def hours_rows(periods):
    """7 <tr> Mon..Sun with data-day and 'X to Y' (or Closed)."""
    by = periods_by_day(periods)
    rows = ""
    for i, day in enumerate(DAYS_MON):
        dnum = (i + 1) % 7                    # Mon=1..Sat=6,Sun=0
        segs = by.get(dnum, [])
        if segs:
            txt = ", ".join(f"{t12(o)} to {t12(c)}" for o, c in segs)
        else:
            txt = "Closed"
        rows += f'<tr data-day="{dnum}"><th scope="row">{day}</th><td>{txt}</td></tr>\n'
    return rows

def most_common_close(periods):
    closes = [c["time"] for p in periods or [] for c in [p.get("close")] if c]
    if not closes: return None
    return Counter(closes).most_common(1)[0][0]

def hours_uniform(periods):
    by = periods_by_day(periods)
    if len(by) != 7: return None
    sigs = {tuple(sorted(v)) for v in by.values()}
    if len(sigs) != 1: return None
    (o, c), = list(by.values())[0] if len(list(by.values())[0]) == 1 else (None,)
    segs = list(by.values())[0]
    if len(segs) != 1: return None
    return segs[0]                              # (open,close)

def ld_hours(periods):
    by = periods_by_day(periods)
    groups = defaultdict(list)
    for i, day in enumerate(DAYS_MON):
        dnum = (i + 1) % 7
        segs = by.get(dnum)
        if not segs: continue
        key = tuple(segs)
        groups[key].append(day)
    specs = []
    for key, days in groups.items():
        for (o, c) in key:
            specs.append({"@type":"OpeningHoursSpecification",
                          "dayOfWeek": days if len(days) > 1 else days[0],
                          "opens": f"{o[:2]}:{o[2:]}", "closes": f"{c[:2]}:{c[2:]}"})
    return specs

# ---------------------------------------------------------------- chrome -----
# UNIVERSAL CHROME (bobanight chrome kit): pages carry ZERO header/nav/footer
# markup, css, or js of their own. The five kit lines below are the entire
# contract; components live in the repo at /components/ (source of truth on
# GitHub, served by Vercel). Never bake chrome into a page again.
KIT_CSSLINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
    '<link rel="stylesheet" href="/css/site.css">\n'
    '<link rel="stylesheet" href="/css/motif.css">\n'
    '<link rel="stylesheet" href="/css/profile-v4.css">\n'
    '<link rel="stylesheet" href="/components/footer.css">')

def find_chrome_ref():
    return None

def load_chrome():
    return '<div id="bn-nav"></div>\n', '<div id="bn-footer"></div>', KIT_CSSLINKS

SCRIPTS = ('<script src="/js/motif.js" defer></script>\n'
           '<script defer src="/js/profile-v4.js"></script>\n'
           '<script src="/components/nav.js" defer></script>\n'
           '<script src="/components/footer.js" defer></script>\n')

# ---------------------------------------------------------------- geometry ---
def project(lat0, lng0, lat, lng, ppm):
    mn = (lat - lat0) * 69.0
    me = (lng - lng0) * 69.0 * math.cos(math.radians(lat0))
    return (max(4.0, min(96.0, 50 + me*ppm)), max(6.0, min(94.0, 50 - mn*ppm)))

RING_STEPS = [0.25, 0.5, 1, 2, 3, 5, 10]

# ---- order-rail art + verified-Toast data (v3 sticky) ----
UE_ART='<svg class="od-art" viewBox="0 0 28 28" aria-hidden="true"><path d="M8.6 11h10.8l-1.2 11.6a1.7 1.7 0 0 1-1.7 1.5h-5a1.7 1.7 0 0 1-1.7-1.5L8.6 11z" fill="rgba(6,193,103,.18)"/><path class="k" d="M8.6 11h10.8l-1.2 11.6a1.7 1.7 0 0 1-1.7 1.5h-5a1.7 1.7 0 0 1-1.7-1.5L8.6 11z"/><path class="k" d="M9 10.8a5.2 5.2 0 0 1 10 0"/><path class="k" d="M15.3 9.6l2.6-6.2"/><circle class="p" cx="12" cy="20.2" r="1.1"/><circle class="p" cx="15.6" cy="21" r="1.1"/><circle class="p" cx="13.8" cy="17.6" r="1.1"/></svg>'
DD_ART='<svg class="od-art" viewBox="0 0 28 28" aria-hidden="true"><path d="M6.4 10.4h15.2l-1.4 12.4a1.8 1.8 0 0 1-1.8 1.6H9.6a1.8 1.8 0 0 1-1.8-1.6L6.4 10.4z" fill="rgba(255,48,8,.15)"/><path class="k" d="M6.4 10.4h15.2l-1.4 12.4a1.8 1.8 0 0 1-1.8 1.6H9.6a1.8 1.8 0 0 1-1.8-1.6L6.4 10.4z"/><path class="k" d="M10.2 10.2V8.6a3.8 3.8 0 0 1 7.6 0v1.6"/><path class="k" d="M9 14.6h10"/><circle class="p" cx="11.6" cy="19.2" r="1"/><circle class="p" cx="14" cy="20.6" r="1"/><circle class="p" cx="16.4" cy="19.2" r="1"/></svg>'
TO_ART=('<svg class="od-art" viewBox="0 0 28 28" aria-hidden="true"><g transform="rotate(-8 14 14)">'
 '<path class="k" d="M6.4 13a3.5 3.5 0 0 1 7 0v5.4a1.2 1.2 0 0 1-1.2 1.2H7.6a1.2 1.2 0 0 1-1.2-1.2z"/>'
 '<path class="k" d="M8.3 13.2a1.7 1.7 0 0 1 3.4 0"/>'
 '<path class="k" d="M15.4 13.2h6l-.4 3.1a2.5 2.5 0 0 1-2.5 2.2h-.2a2.5 2.5 0 0 1-2.5-2.2z"/>'
 '<path class="k" d="M21.2 13.9a1.6 1.6 0 0 1 0 3"/>'
 '<path class="k" d="M13.9 19.4q4.3 1.3 8.6 0"/>'
 '<path class="k" d="M17 11.3q.75-1 0-2.1M19.4 11.3q.75-1 0-2.1"/>'
 '</g></svg>')
DIR_ART='<svg viewBox="0 0 24 24" aria-hidden="true"><path class="k" d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle class="k" cx="12" cy="10" r="2.6"/></svg>'
LEAD_CUP='<svg class="od-cup" viewBox="0 0 24 24" aria-hidden="true"><path class="k" d="M7.2 9.4h9.6l-1.1 10.4a1.5 1.5 0 0 1-1.5 1.3h-4.4a1.5 1.5 0 0 1-1.5-1.3L7.2 9.4z"/><path class="k" d="M7.6 9.2a4.6 4.6 0 0 1 8.8 0"/><path class="k" d="M13.1 8.2l2.3-5.4"/><circle class="p" cx="10.2" cy="17.6" r="1"/><circle class="p" cx="13.4" cy="18.4" r="1"/></svg>'
try:
    TOAST_LINKS = json.load(open(os.path.join(ROOT, "build", "toast_links.json"), encoding="utf-8"))
except Exception:
    TOAST_LINKS = {}


# ---------------------------------------------------------------- render -----
def build_page(shop, opens, chrome):
    header, footer, csslinks = chrome
    name, city, zipc = shop["name"], shop["city"], shop.get("zip") or ""
    addr = ((shop.get("address") or "").split(",")[0]).strip()   # street-only (drop ", City, CA zip, USA")
    lat, lng = shop["lat"], shop["lng"]
    slug, cs = shop["slug"], slugify(city)
    ST = st_ab(shop.get("state")); stp = ST.lower()
    reg = region_slug(shop.get("county"), city); reglab = REGION_LABEL[reg]
    tb = type_bits(shop.get("store_type"))
    periods = shop.get("periods") or []
    has_hours = bool(periods)
    url = f"{SITE}/boba/{stp}/{cs}/{slug}/"
    dirn = maps_href(name, addr, city, ST)
    full_addr = addr + (", " + city if city else "") + ", " + ST + ((" " + zipc) if zipc else "")
    if lat is not None and lng is not None:
        import base64 as _b64
        _pl = {"address": full_addr, "latitude": lat, "longitude": lng,
               "reference": shop.get("place_id") or "", "referenceType": "google_places"}
        _enc = _b64.b64encode(urllib.parse.quote(json.dumps(_pl, separators=(",", ":"))).encode()).decode()
        ue = "https://www.ubereats.com/search?diningMode=DELIVERY&q=" + uq(name) + "&pl=" + _enc
    else:
        ue = "https://www.ubereats.com/search?q=" + uq(name)
    dd = "https://www.doordash.com/search/store/" + uq(name) + "/"
    E = esc(name)
    county_bare = (shop.get("county") or "").replace("County", "").strip()

    # neighbours (open, other shops), nearest first
    nb = []
    for s in opens:
        if s["slug"] == slug: continue
        d = haversine(lat, lng, s["lat"], s["lng"])
        if d <= 12: nb.append((d, s))
    nb.sort(key=lambda t: t[0])
    within1 = sum(1 for d, _ in nb if d <= 1.0)
    shown = [(d, s) for d, s in nb if d <= 3.0][:10]

    # nearby cities (other cities), nearest shop dist, count, pick=max reviews
    bycity = defaultdict(list)
    for d, s in nb:
        if s["city"] and s["city"] != city:
            bycity[s["city"]].append((d, s))
    cities = []
    for cty, lst in bycity.items():
        lst.sort(key=lambda t: t[0])
        cnt = sum(1 for _ in lst)
        pick = max((s for _, s in lst), key=lambda s: s.get("reviews") or 0)
        cities.append((lst[0][0], cty, cnt, pick))
    cities.sort(key=lambda t: t[0])
    cities = cities[:8]

    # ---- head ----
    title = f"{name}, {city}: Boba Hours & Map (2026) | Boba Night"
    hpart = "Verified hours, " if has_hours else ""
    desc = f"{name} at {addr}, {city}. {tb['herosub']}. {hpart}map, and {within1} more boba shops nearby."
    head = ('<!DOCTYPE html><html lang="en"><head>\n<meta charset="UTF-8">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{title}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="canonical" href="{url}"><meta name="robots" content="noindex,follow">\n'
            f'{csslinks}\n</head><body>\n')

    # ---- breadcrumb ----
    crumb = (f'<nav class="crumb" aria-label="Breadcrumb">\n<a href="/">Home</a><span class="sep">/</span>\n'
             f'<a href="/area/{reg}/">{nbsp(reglab)}</a><span class="sep">/</span>\n'
             f'<a href="/boba/{stp}/{cs}/">{nbsp(esc(city))}</a><span class="sep">/</span>\n'
             f'<span aria-current="page">{E}</span>\n</nav>\n')

    # ---- hero ----
    rating = shop.get("rating"); reviews = shop.get("reviews")
    hero_rating = ""
    if rating:
        rq = "https://www.google.com/search?q=" + uq(f"{name} {city} reviews")
        rev = (f' &middot; <a href="{rq}" rel="nofollow noopener" target="_blank">{reviews}&nbsp;reviews on Google</a>'
               if reviews else "")
        hero_rating = (f' <span class="hero-rating"><span class="star" aria-hidden="true">&#9733;</span>'
                       f'{esc(rating)}{rev}</span>')
    status_pill = ('<span class="status pending js-status-pill"><span class="led"></span>Checking hours</span>'
                   if has_hours else '<span class="status pending"><span class="led"></span>Verifying hours</span>')
    hero = ('<!-- TPL:hero -->\n<section class="hero"><div class="hero-inner">\n'
            '<span class="av-orb" aria-hidden="true">\n  <span class="av-disc"><span class="av-sheen"></span></span>\n'
            '  <svg class="av-ell" viewBox="0 0 120 120" focusable="false"><ellipse cx="60" cy="60" rx="56" ry="19" transform="rotate(-16 60 60)"/></svg>\n'
            '  <span class="av-track"></span>\n  <span class="av-sat"></span>\n'
            f'  <span class="av-mono">{esc(monogram(name))}</span>\n  <span class="av-badge"></span>\n</span>\n'
            f'<div class="hero-body">\n<div class="hero-titlerow"><h1>{E}</h1></div>\n'
            f'<p class="hero-sub">{tb["herosub"]} in {nbsp(esc(city))}, {nbsp(reglab)}</p>\n'
            f'<div class="hero-meta"><span class="tag {tb["tag_cls"]}">{tb["tag"]}</span> {status_pill}{hero_rating}</div>\n'
            '<div class="hero-actions">\n'
            f'<a class="btn btn-primary" href="{dirn}" rel="nofollow noopener" target="_blank">Get directions</a>\n'
            '<button class="btn btn-ghost" type="button" data-share-open>Share this spot</button>\n'
            f'<button class="ps-heart js-save" type="button" aria-pressed="false" aria-label="Save {E} to your blackbook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-9.2-8.4A5 5 0 0 1 12 6a5 5 0 0 1 9.2 5.6C19 15.6 12 20 12 20z"/></svg></button>\n'
            '</div></div></div></section>\n<!-- /TPL:hero -->\n')

    # ---- quickfacts ----
    ent_hours = ""
    if has_hours:
        mc = most_common_close(periods)
        if mc: ent_hours = f" It is open until {t12(mc)} most nights."
    county_link = f'<a href="/cities/">{nbsp(esc(county_bare))} County</a>' if county_bare else ""
    tonight_row = '<div><dt>Tonight</dt><dd id="qfToday">See hours</dd></div>\n' if has_hours else ""
    price_row = ""
    if shop.get("price_level") in PRICE:
        price_row = f'<div><dt>Price</dt><dd>{PRICE[shop["price_level"]]}</dd></div>\n'
    quickfacts = ('<!-- TPL:quickfacts -->\n<section class="sec" id="facts">\n'
        f'<p class="qf-entity">{E} is {tb["ent"]} at {esc(addr)} in {esc(city)}, {esc(shop.get("state") or "California")}, in the {reglab}.{ent_hours}</p>\n'
        '<dl class="dl qf-grid">\n'
        f'<div><dt>Type</dt><dd>{tb["qf"]}</dd></div>\n'
        f'<div><dt>Area</dt><dd class="qf-stack"><a href="/boba/{stp}/{cs}/">{nbsp(esc(city))}</a>{county_link}<a href="/area/{reg}/">{nbsp(reglab)}</a></dd></div>\n'
        f'{tonight_row}'
        f'<div><dt>To go</dt><dd><a href="{hh(ue)}" rel="nofollow sponsored noopener" target="_blank">Uber&nbsp;Eats</a> and <a href="{hh(dd)}" rel="nofollow sponsored noopener" target="_blank">DoorDash</a></dd></div>\n'
        f'{price_row}</dl>\n\n</section>\n<!-- /TPL:quickfacts -->\n')

    # ---- about ----
    corridor = f" It pours in a corridor with {within1} more boba shops within a mile." if within1 else ""
    prov = "Name, address, and hours come from" if has_hours else "Name, address come from"
    about = ('<!-- TPL:about -->\n<section class="sec"><p class="p-summary"><span class="lbl">About</span>\n'
             f'{E} is {tb["ent"]} at {esc(addr)} in {esc(city)}, {esc(reglab)}.{corridor} '
             f'{prov} the shop&#x27;s public listing. Menu details show once we verify them from a primary source.</p></section>\n'
             '<!-- /TPL:about -->\n')

    # ---- hours ----
    if has_hours:
        hours = ('<!-- TPL:hours -->\n<section class="sec" id="hours">\n'
                 '<div class="hours-head"><h2>Hours</h2><span class="status pending js-status-pill"><span class="led"></span>Checking hours</span></div>\n'
                 f'<div class="hours-wrap"><table class="hours-t">\n<tbody>\n{hours_rows(periods)}</tbody></table></div>\n'
                 '<p class="note-line">Hours come from the shop\'s public listing. Changed? <a class="textlink" href="/report/">Report it</a> and we recheck.</p>\n'
                 '</section>\n<!-- /TPL:hours -->\n')
    else:
        hours = ('<!-- TPL:hours -->\n<section class="sec" id="hours">\n'
                 '<div class="hours-head"><h2>Hours</h2><span class="status pending"><span class="led"></span>Verifying</span></div>\n'
                 '<p class="is-muted">We&#x27;re verifying current hours against the shop&#x27;s listing. Use Get directions for live Google hours in the meantime.</p>\n'
                 '</section>\n<!-- /TPL:hours -->\n')

    # ---- share ----
    share_detail = "the address, tonight's closing time" if has_hours else "the address"
    share = ('<!-- TPL:share -->\n<section class="sec" id="pass">\n<div class="ps-pass">\n'
             '<p class="eyebrow">Pass it along</p>\n<h2>Going? Tell someone.</h2>\n'
             f'<p>The invite writes itself from verified details: {share_detail}.</p>\n'
             '<button class="btn btn-primary" type="button" data-share-open>Build the invite</button>\n'
             "<p class=\"note-line\">Sends by text or your phone's share sheet. We never post for you.</p>\n</div>\n</section>\n<!-- /TPL:share -->\n")

    # ---- map ----
    open_map = hh(f"/near-me/?shop={slug}&lat={lat}&lng={lng}&n={uq(name)}")
    if shown:
        D = shown[-1][0]
        ppm = 40.0 / D if D > 0 else 40.0
        rings = ""
        for r in RING_STEPS:
            if r <= D * 1.05:
                w = round(2 * r * ppm, 1)
                if w <= 96:
                    lbl = (str(int(r)) if r == int(r) else str(r)) + " mi"
                    rings += f'<span class="mp-ring" aria-hidden="true" style="width:{w}%;height:{w}%"><i>{lbl}</i></span>'
        if not rings:
            rings = '<span class="mp-ring" aria-hidden="true" style="width:60%%;height:60%%"><i>%s mi</i></span>' % fmt_mi(D)
        spots = ""
        for d, s in shown:
            stb = type_bits(s.get("store_type"))
            L, T = project(lat, lng, s["lat"], s["lng"], ppm)
            nm = hh(f"/near-me/?shop={s['slug']}&lat={s['lat']}&lng={s['lng']}&n={uq(s['name'])}")
            per = f" data-per='{json.dumps(data_per(s.get('periods')), separators=(chr(44),chr(58)))}'" if s.get("periods") else ""
            spots += (f'<a class="mp-spot {stb["mp"]}" href="/boba/{st_ab(s.get("state")).lower()}/{slugify(s["city"])}/{s["slug"]}/#map" style="left:{L}%;top:{T}%" '
                      f'data-n="{esc(s["name"])}" data-c="{esc(s["city"])}" data-mi="{fmt_mi(d)}" data-nm="{nm}" '
                      f'data-lat="{s["lat"]}" data-lng="{s["lng"]}"{per}><span class="mp-dot" aria-hidden="true"></span>'
                      f'<span class="bn-sr">{esc(s["name"])}, {fmt_mi(d)} miles away</span></a>\n')
    else:
        rings = '<span class="mp-ring" aria-hidden="true" style="width:42.6%;height:42.6%"><i>0.25 mi</i></span>'
        spots = ""
    center = (f'<button class="mp-center" type="button" aria-label="{E}, you are viewing this shop" '
              f'data-n="{E}" data-c="{esc(city)}" data-mi="0" data-lat="{lat}" data-lng="{lng}" data-nm="{open_map}">'
              '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg></button>')
    mapsec = ('<section class="sec" id="map"><h2>Find it on the Boba Night Map</h2>\n<!-- TPL:map -->\n'
              '<div class="map-main mp-wrap"><div class="mp-face">\n<div class="mp-leaf" id="mpLeaf" aria-hidden="true"></div>\n'
              f'<div class="mp-stage">\n{rings}\n{spots}{center}\n<div class="mp-card" id="mpCard" hidden></div>\n</div>\n</div>\n'
              f'<div class="map-foot"><div class="addr"><strong>{esc(addr)}</strong><span>{esc(city)}, {ST} {esc(zipc)}</span></div>\n'
              f'<a class="btn btn-primary" href="{open_map}">Open the Boba Night Map</a>\n'
              f'<a class="btn btn-ghost" href="{dirn}" rel="nofollow noopener" target="_blank">Get directions</a></div></div>\n'
              '<p class="note-line">Coordinates are geocoded and verified before this profile is indexed, so the pin never drifts from the real address. '
              '<span class="mp-credit">Map data <a href="https://www.openstreetmap.org/copyright" rel="nofollow noopener" target="_blank">OpenStreetMap</a>, '
              '<a href="https://carto.com/attributions" rel="nofollow noopener" target="_blank">CARTO</a>.</span></p>\n<!-- /TPL:map -->\n</section>\n')

    gtk = ('<section class="sec"><h2>Good to know <span class="tag tag-verifying">Verifying</span></h2>\n'
           '<p class="is-muted">Seating, wifi, non-dairy, and other details show only once a primary source confirms them.</p></section>\n')

    # ---- nearby shops ----
    nearby_shops = ""
    if shown:
        ps = ""
        for d, s in shown:
            stb = type_bits(s.get("store_type"))
            live = (f' <span class="ps-live" data-per=\'{json.dumps(data_per(s.get("periods")), separators=(chr(44),chr(58)))}\'></span>'
                    if s.get("periods") else "")
            ps += (f'<a class="ps-shop" href="/boba/{st_ab(s.get("state")).lower()}/{slugify(s["city"])}/{s["slug"]}/"><span class="n">{esc(s["name"])}</span>'
                   f'<span class="m"><span class="ps-mi">{fmt_mi(d)}&nbsp;mi</span><span>{esc(s["city"])}</span>'
                   f'<span class="tag {stb["tag_cls"]}">{stb["tag"]}</span>{live}</span></a>\n')
        intro = f'{within1} more shops pour within a mile, {len(shown)} within {fmt_mi(shown[-1][0])}&nbsp;miles. If the line is long, the next counter is close.'
        nearby_shops = ('<!-- TPL:nearby-shops -->\n<section class="sec" id="nearby">\n<p class="eyebrow">The corridor</p>\n'
                        f'<h2>More boba nearby</h2>\n<p class="is-muted" style="margin:0;max-width:60ch">{intro}</p>\n'
                        f'<div class="ps-shops">\n{ps}</div>\n'
                        f'<p class="note-line">Distances are straight-line from {E}&#x27;s verified coordinates. Original means an independent or single-origin house; Chain means a multi-location brand.</p>\n'
                        '</section>\n<!-- /TPL:nearby-shops -->\n')

    # ---- nearby cities ----
    nearby_cities = ""
    if cities:
        rows = ""
        for dist, cty, cnt, pick in cities:
            lead = "The one to know" if cnt == 1 else "Another good one"
            ptb = type_bits(pick.get("store_type"))
            db = ", an original tea house." if ptb["tag"] == "Original" else "."
            unit = "shop" if cnt == 1 else "shops"
            rows += (f'<div class="ps-city"><div class="row1"><a class="cl" href="/boba/{st_ab(pick.get("state")).lower()}/{slugify(cty)}/">Boba in {nbsp(esc(cty))}</a>'
                     f'<span class="ct">{cnt}&nbsp;{unit}, {fmt_mi(dist)}&nbsp;mi</span></div>'
                     f'<p class="pick">{lead} in {nbsp(esc(cty))}: <a href="/boba/{st_ab(pick.get("state")).lower()}/{slugify(cty)}/{pick["slug"]}/">{esc(pick["name"])}</a>{db}</p></div>\n')
        nearby_cities = ('<!-- TPL:nearby-cities -->\n<section class="sec" id="cities">\n<p class="eyebrow">Keep browsing</p>\n'
                         f'<h2>Boba towns around {esc(city)}</h2>\n<div class="ps-cities">\n{rows}</div>\n</section>\n<!-- /TPL:nearby-cities -->\n')

    # ---- faq ----
    if has_hours:
        u = hours_uniform(periods)
        if u:
            hsent = f"{E}&#x27;s listed hours are Monday through Sunday {t12(u[0])} to {t12(u[1])}."
        else:
            hsent = f"{E}&#x27;s hours vary by day; the table above lists each day."
        open_a = f'{hsent} The status badge at the top of this page shows live open or closed status.'
    else:
        open_a = f'We&#x27;re verifying {E}&#x27;s current hours against the shop&#x27;s listing. Use the Get directions button for live Google hours in the meantime.'
    faq = ('<!-- TPL:faq -->\n<section class="sec faq"><h2>FAQ</h2>\n'
           f'<h3>Where is {E}?</h3><p>{E} is at {esc(addr)} in {esc(city)}, {ST} {esc(zipc)}, in {esc(reglab)}.</p>\n'
           f'<h3>Is {E} open right now?</h3><p>{open_a}</p></section>\n<!-- /TPL:faq -->\n')

    # ---- explore ----
    explore = ('<!-- TPL:explore -->\n<section class="sec" id="keep-exploring">\n<p class="eyebrow">Keep exploring</p>\n'
               '<h2>Where to next</h2>\n<ul class="nearby-list xp-list">\n'
               f'<li><a href="/boba/{stp}/{cs}/">All boba in {esc(city)}</a></li>\n'
               '<li><a href="/best/open-late/">Boba open late across SoCal</a></li>\n'
               f'<li><a href="/area/{reg}/">All of the {esc(reglab)}</a></li>\n'
               '<li><a href="/best/brown-sugar/">Best brown sugar boba</a></li>\n'
               '<li><a href="/pantry/">The Pantry: every topping explained</a></li>\n'
               f'<li><a href="{open_map}">The full Boba Night Map</a></li>\n</ul>\n</section>\n<!-- /TPL:explore -->\n')

    # ---- facts aside ----
    today_row = '<div><dt>Today</dt><dd id="factsToday">See hours</dd></div>\n' if has_hours else ""
    facts = ('<!-- TPL:facts -->\n<aside class="g-aside"><div class="facts-card">\n'
             f'<p class="fc-title">Find {E}</p>\n<dl class="dl">\n'
             f'<div><dt>Address</dt><dd><a href="{dirn}" rel="nofollow noopener" target="_blank">{esc(addr)},<br>{nbsp(esc(city))}, {ST}&nbsp;{esc(zipc)}</a></dd></div>\n'
             f'<div><dt>Area</dt><dd><a href="/area/{reg}/">{esc(reglab)}</a></dd></div>\n'
             f'<div><dt>Type</dt><dd>{tb["aside"]}</dd></div>\n{today_row}</dl>\n'
             f'<p class="card-line">Checked {STAMP} &middot; hours from the shop\'s public listing</p>\n'
             '<p class="card-line">Is this your shop? <a class="textlink" href="/claim/">Claim this listing</a></p>\n'
             '<p class="card-line">Something wrong? <a class="textlink" href="/report/">Report it</a></p>\n</div></aside>\n<!-- /TPL:facts -->\n')

    # ---- JSON-LD ----
    shop_ld = {"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":name,"@id":url+"#shop",
               "url":url,"servesCuisine":"Bubble Tea"}
    if shop.get("price_level"): shop_ld["priceRange"] = "$" * int(shop["price_level"])
    shop_ld["address"] = {"@type":"PostalAddress","streetAddress":addr,"addressLocality":city,
                          "addressRegion":ST,"postalCode":zipc,"addressCountry":"US"}
    shop_ld["geo"] = {"@type":"GeoCoordinates","latitude":lat,"longitude":lng}
    if has_hours: shop_ld["openingHoursSpecification"] = ld_hours(periods)
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":reglab,"item":f"{SITE}/area/{reg}/"},
        {"@type":"ListItem","position":3,"name":city,"item":f"{SITE}/boba/{stp}/{cs}/"},
        {"@type":"ListItem","position":4,"name":name,"item":url}]}
    def plain(s): return re.sub("&#x27;","'", re.sub("&nbsp;"," ", s))
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":f"Where is {name}?","acceptedAnswer":{"@type":"Answer",
            "text":f"{name} is at {addr} in {city}, {ST} {zipc}, in {reglab}."}},
        {"@type":"Question","name":f"Is {name} open right now?","acceptedAnswer":{"@type":"Answer",
            "text":plain(open_a).replace(name, name)}}]}
    wp = {"@context":"https://schema.org","@type":"WebPage","@id":url+"#webpage","url":url,
          "name":f"{name}, {city}: Boba Hours & Map","dateModified":"2026-07-20",
          "about":{"@id":url+"#shop"},"speakable":{"@type":"SpeakableSpecification","cssSelector":[".qf-entity","#hours"]}}
    def ld(o): return f'<script type="application/ld+json">\n{json.dumps(o, ensure_ascii=False)}\n</script>\n'
    jsonld = ('<!-- TPL:jsonld-shop -->\n'+ld(shop_ld)+'<!-- /TPL:jsonld-shop -->\n'
              '<!-- TPL:jsonld-breadcrumb -->\n'+ld(bc)+'<!-- /TPL:jsonld-breadcrumb -->\n'
              '<!-- TPL:jsonld-faq -->\n'+ld(faqld)+'<!-- /TPL:jsonld-faq -->\n'
              '<!-- TPL:jsonld-webpage -->\n'+ld(wp)+'<!-- /TPL:jsonld-webpage -->\n')

    main = ('<main id="main" class="wrap">\n' + crumb + hero + '<div class="grid">\n<div class="g-main">\n' +
            quickfacts + about + hours + share + mapsec + gtk + nearby_shops + nearby_cities + faq + explore +
            '</div>\n' + facts + '</div>\n' + jsonld.rstrip("\n") + '</main>')

    # ---- order rail (v3: info block + Uber/DoorDash/Toast + Directions) ----
    _tinfo = TOAST_LINKS.get(slug) or {}
    if _tinfo.get("toast_url") and _tinfo.get("confidence") in ("high", "review"):
        toast_btn = ('<a class="od-svc od-svc--to" href="' + hh(_tinfo["toast_url"]) +
                     '" target="_blank" rel="nofollow sponsored noopener">' + TO_ART +
                     '<span class="od-n">Toast</span></a>')
    else:
        toast_btn = ('<span class="od-svc od-svc--to is-off" aria-disabled="true" title="Not available on Toast">' +
                     TO_ART + '<span class="od-n">Toast</span></span>')
    _meta = ""
    if shop.get("rating"):
        _meta += '<span class="od-rail-star">&#9733; ' + esc(shop["rating"]) + '</span>'
    if shop.get("reviews"):
        _meta += '<span class="od-rail-rev">' + format(int(shop["reviews"]), ",") + ' reviews</span>'
    if full_addr:
        _meta += '<span class="od-rail-dot">&middot;</span>' + esc(full_addr)
    order = ('<!-- TPL:order-rail -->\n'
        f'<nav class="od-rail" aria-label="Order {E} to go">\n'
        '  <span class="od-rail-lead">' + LEAD_CUP +
        f'<span class="od-rail-info"><b class="od-rail-name">{E}</b>'
        f'<span class="od-rail-meta">{_meta}</span></span></span>\n'
        '  <div class="od-rail-acts">\n'
        f'    <a class="od-svc od-svc--ue" href="{hh(ue)}" target="_blank" rel="nofollow sponsored noopener">{UE_ART}<span class="od-n">Uber&nbsp;Eats</span></a>\n'
        f'    <a class="od-svc od-svc--dd" href="{hh(dd)}" target="_blank" rel="nofollow sponsored noopener">{DD_ART}<span class="od-n">DoorDash</span></a>\n'
        f'    {toast_btn}\n'
        f'    <a class="od-dir" href="{dirn}" rel="nofollow noopener" target="_blank">{DIR_ART}<span>Directions</span></a>\n'
        '  </div>\n</nav>\n'
        '<p class="od-rail-note">Delivery and pickup by Uber Eats, DoorDash, or Toast. Menus and prices set by the service.</p>\n'
        '<!-- /TPL:order-rail -->\n')

    # ---- share modal ----
    stops = [(d, s) for d, s in shown if d <= 0.5][:3]
    crawl = ""
    if stops:
        chips = "".join(f'      <button class="ps-chip" type="button" data-stop="{i}" aria-pressed="false">{esc(s["name"])}<span class="mi">{fmt_mi(d)}&nbsp;mi</span></button>\n'
                        for i, (d, s) in enumerate(stops))
        crawl = ('    <span class="ps-lbl" id="psCrawlLbl">Make it a crawl</span>\n'
                 '    <div class="ps-chips" role="group" aria-labelledby="psCrawlLbl">\n' + chips + '    </div>\n'
                 f'    <p class="ps-hint" id="psHint" aria-live="polite">Up to two stops, all a short walk from {E}.</p>\n')
    modal = ('<!-- TPL:share-modal -->\n<div class="ps-modal" id="psModal" role="dialog" aria-modal="true" aria-labelledby="psTitle" hidden>\n'
             '  <div class="ps-scrim" data-share-close></div>\n  <div class="ps-box" role="document">\n'
             '    <div class="ps-mhead">\n      <div>\n        <h2 class="ps-mtitle" id="psTitle">Invite someone</h2>\n      </div>\n'
             '      <button class="ps-x" type="button" data-share-close aria-label="Close share dialog">&times;</button>\n    </div>\n'
             '    <span class="ps-lbl" id="psWhenLbl">When</span>\n    <div class="ps-chips" role="group" aria-labelledby="psWhenLbl">\n'
             '      <button class="ps-chip" type="button" data-when="tonight" aria-pressed="true">Tonight</button>\n'
             '      <button class="ps-chip" type="button" data-when="sevenpm" aria-pressed="false">7pm</button>\n'
             '      <button class="ps-chip" type="button" data-when="weekend" aria-pressed="false">This weekend</button>\n    </div>\n'
             f'{crawl}    <span class="ps-lbl">Your invite</span>\n    <p class="ps-preview" id="psPreview" aria-live="polite"></p>\n'
             '    <div class="ps-mact">\n      <a class="btn btn-primary" id="psSms" href="sms:?&amp;body=">Text the invite</a>\n'
             '      <button class="btn btn-ghost" id="psNative" type="button" hidden>Share&hellip;</button>\n'
             '      <button class="btn btn-ghost" id="psCopyMsg" type="button">Copy invite</button>\n    </div>\n'
             '    <p class="ps-mnote">Nothing is posted anywhere. The message goes only where you send it.</p>\n  </div>\n</div>\n<!-- /TPL:share-modal -->\n')

    # ---- bn-shop-data ----
    sd = {"slug":slug,"name":name,"addr":addr,"city":city,"url":url,
          "periods":data_per(periods),"stops":[{"n":s["name"],"mi":fmt_mi(d)} for d,s in stops]}
    shopdata = ('<!-- TPL:shop-data -->\n<script id="bn-shop-data" type="application/json">\n'
                + json.dumps(sd, ensure_ascii=False) + '\n</script>\n<!-- /TPL:shop-data -->\n')

    return head + header + main + "\n" + footer + "\n" + order + modal + shopdata + SCRIPTS + '</body></html>\n'

# ---------------------------------------------------------------- data -------
def fetch_all():
    s = os.environ.get("NBV4_SAMPLE")
    if s: return json.load(open(s, encoding="utf-8"))
    rows, page, size = [], 0, 1000
    while True:
        q = ("/rest/v1/niteboba?select="+COLS+"&status=eq.open&latitude=not.is.null&longitude=not.is.null"
             "&order=name.asc&limit=%d&offset=%d" % (size, page*size))
        req = urllib.request.Request(SB+q, headers={"apikey":KEY,"Authorization":"Bearer "+KEY,"Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            batch = json.load(r)
        rows.extend(batch)
        if len(batch) < size: break
        page += 1
    return rows

def norm(r):
    h = r.get("hours") or {}
    return {"slug":r["slug"],"name":r["name"],"city":r.get("city") or "","county":r.get("county"),
            "address":r.get("address"),"zip":r.get("zip"),"store_type":r.get("store_type"),
            "status":r.get("status"),"state":r.get("state"),"lat":fnum(r.get("latitude")),"lng":fnum(r.get("longitude")),
            "rating":r.get("google_rating"),"reviews":r.get("google_review_count"),"place_id":r.get("google_place_id"),
            "price_level":r.get("price_level"),"periods":h.get("periods") or []}

def main(argv):
    rows = [norm(r) for r in fetch_all()]
    opens = [s for s in rows if s["lat"] is not None and s["lng"] is not None]
    chrome = load_chrome()
    dry = "--dry-run" in argv
    only = argv[argv.index("--slug")+1] if "--slug" in argv else None
    lim  = int(argv[argv.index("--limit")+1]) if "--limit" in argv else None
    targets = [s for s in opens if s["slug"] not in SKIP_SLUGS]
    if only: targets = [s for s in targets if s["slug"] == only]
    if lim:  targets = targets[:lim]
    print("open shops: %d | generating: %d | chrome ref ok | dry=%s" % (len(opens), len(targets), dry))
    wrote = 0
    for s in targets:
        page = build_page(s, opens, chrome)
        dest = os.path.join(ROOT, "boba", st_ab(s.get("state")).lower(), slugify(s["city"]), s["slug"], "index.html")
        if dry:
            if wrote < 3: print("  would write", os.path.relpath(dest, ROOT), "(%d bytes)" % len(page))
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "w", encoding="utf-8").write(page)
        wrote += 1
    print(("DRY-RUN: would write %d pages" if dry else "wrote %d pages") % wrote)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
