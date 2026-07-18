#!/usr/bin/env python3
"""
Boba Night — anti-Yelp profile generator (W3).

Reads data/stores-data.json (Google Places shape: periods + weekday_text) and
writes one obsidian-editorial profile page per shop. No stars, no invented facts:
a dated VERIFICATION LEDGER stands in for ratings, hours are baked as JSON and
resolved client-side against America/Los_Angeles, and nearby shops carry real
haversine distances.

CLI:
  python3 build/gen_profiles.py <slug>          # one profile
  python3 build/gen_profiles.py <slug> --out P  # one profile, explicit output path
  python3 build/gen_profiles.py --all           # every shop (use with care)

Two template states:
  OPEN     — full ledger, guava LED (the page's one neon spend), tonight strip,
             action row, indexable when it has verified hours AND coords AND open.
  CLOSED   — the epitaph. Desaturated, no guava, past-tense dek, no action row /
             tonight strip, "Still pouring nearby" rail, permanentlyClosed schema,
             always noindex.
"""
import json, re, os, html, math, datetime, sys

# Bake the site's unified nav directly into every profile (no separate
# apply_nav pass needed). render_header() returns the canonical header partial
# — skip link, sticky mega-nav, search overlay, mobile drawer, bottom bar.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_data import render_header

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA  = os.path.join(ROOT, "data", "stores-data.json")
SITE  = "https://www.bobanight.com"
TODAY = datetime.date.today()
STAMP = TODAY.strftime("%-d %b %Y").upper()          # e.g. "17 JUL 2026"

# ---- region mapping (mirrors gen_site.py; keep in sync) --------------------
SGV_CITIES = {"Arcadia","Covina","Pasadena","Walnut","Rowland Heights","Monterey Park",
              "City of Industry","El Monte","Diamond Bar","Rosemead","San Gabriel",
              "Baldwin Park","Temple City","Monrovia"}
REGIONS = {
  "sgv":           {"label":"San Gabriel Valley","kicker":"The 626"},
  "greater-la":    {"label":"Greater Los Angeles","kicker":"LA"},
  "orange-county": {"label":"Orange County","kicker":"OC"},
  "san-diego":     {"label":"San Diego","kicker":"SD"},
  "inland-empire": {"label":"Inland Empire","kicker":"IE"},
}
def region_of(county, city):
    if county == "Orange": return "orange-county"
    if county == "San Diego": return "san-diego"
    if county in ("Riverside","San Bernardino"): return "inland-empire"
    if county == "Los Angeles":
        return "sgv" if city in SGV_CITIES else "greater-la"
    return "greater-la"

CLOSED_STATES = {"closed", "temporarily_closed"}

# ---- helpers ----------------------------------------------------------------
def slugify(s):
    s = (s or "").lower().strip()
    s = re.sub(r"['\".]", "", s); s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def esc(s): return html.escape(s if s is not None else "", quote=True)

def haversine(a_lat, a_lng, b_lat, b_lng):
    R = 3958.7613  # miles
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat); dl = math.radians(b_lng - a_lng)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(min(1, math.sqrt(x)))

def type_phrase(store_type):
    return {"chain":"bubble tea chain","specialty":"bubble tea house"}.get(
        (store_type or "").lower(), "bubble tea shop")

def type_chip(store_type):
    return {"chain":"Chain","specialty":"Specialty house"}.get(
        (store_type or "").lower(), "Tea shop")

# ---- motif rotation (deterministic per shop, so each page feels bespoke) -----
MOTIF_NAMES = ["pearl","jelly","grass-jelly","red-bean","taro",
               "egg-tart","foam","drizzle","matcha"]
MOTIF_LABEL = {
    "pearl":"Tapioca pearl","jelly":"Lychee jelly","grass-jelly":"Grass jelly",
    "red-bean":"Red bean","taro":"Taro swirl","egg-tart":"Egg tart",
    "foam":"Cheese foam","drizzle":"Brown sugar drizzle","matcha":"Matcha",
}
def motif_for(seed):
    h = 0
    for ch in (seed or "boba"):
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return MOTIF_NAMES[h % len(MOTIF_NAMES)]

def monogram(name):
    for ch in (name or ""):
        if ch.isalnum():
            return ch.upper()
    return "B"

def load_shops():
    with open(DATA, encoding="utf-8") as f:
        shops = json.load(f)
    for s in shops:
        s["region"]    = region_of(s.get("county",""), s.get("city",""))
        s["city_slug"] = slugify(s.get("city",""))
    return shops

# ---- nearby (haversine) -----------------------------------------------------
def nearby(shop, shops):
    """5 nearest non-closed shops with real distances; fallback same-city A-Z."""
    lat, lng = shop.get("latitude"), shop.get("longitude")
    out = []
    if lat is not None and lng is not None:
        cand = []
        for s in shops:
            if s["slug"] == shop["slug"]:                 continue
            if (s.get("status") or "") in CLOSED_STATES:  continue
            if s.get("latitude") is None or s.get("longitude") is None: continue
            d = haversine(lat, lng, s["latitude"], s["longitude"])
            cand.append((d, s))
        cand.sort(key=lambda t: t[0])
        for d, s in cand[:5]:
            out.append((s, f"{d:.1f} mi"))
    if not out:  # fallback: same city, non-closed, A-Z
        same = sorted(
            (s for s in shops
             if s["slug"] != shop["slug"]
             and s.get("city") == shop.get("city")
             and (s.get("status") or "") not in CLOSED_STATES),
            key=lambda s: s.get("name",""))
        out = [(s, None) for s in same[:5]]
    return out

# ---- directions / maps ------------------------------------------------------
def directions_href(shop):
    lat, lng = shop.get("latitude"), shop.get("longitude")
    if lat is not None and lng is not None:
        return f"https://www.google.com/maps/search/?api=1&query={lat}%2C{lng}"
    q = f"{shop.get('name','')} {shop.get('address','')} {shop.get('city','')} CA"
    return "https://www.google.com/maps/search/?api=1&query=" + re.sub(r"\s+","%20",q.strip())

def gsearch_hours(shop):
    q = f"{shop.get('name','')} {shop.get('city','')} CA hours"
    return "https://www.google.com/search?q=" + re.sub(r"\s+","+",q.strip())

# ---- inline obsidian stylesheet (self-contained; no shared-CSS coupling) ----
STYLE = """
:root{
  --obsidian:#0B0C0E;--smoked:#17191D;--smoked-2:#1F2228;
  --pearl:#F4EFE7;--porcelain:#FCF9F3;--muted:#8B8981;--muted-dk:#6f6d67;
  --champagne:#C5A46D;--gilt:#F4DDA2;--guava:#ff3f6f;--neon:#ff2f6d;
  --orchid:#b46bd6;--imperial:#5c2c86;--velvet:#2a0b12;--jade:#123F35;
  --line:rgba(244,239,231,.14);--line-2:rgba(244,239,231,.08);
  --serif:"Fraunces",Georgia,"Times New Roman",serif;
  --sans:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;
  --ease:cubic-bezier(.16,1,.3,1);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;color:var(--pearl);font-family:var(--sans);
  background:
    radial-gradient(1100px 520px at 84% -6%, rgba(255,47,109,.13), transparent 58%),
    radial-gradient(820px 640px at 2% 6%, rgba(92,44,134,.17), transparent 60%),
    radial-gradient(900px 900px at 50% 118%, rgba(18,63,53,.12), transparent 62%),
    var(--obsidian);
  background-attachment:fixed;
  font-size:16px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.035;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--champagne);outline-offset:3px;border-radius:2px}
::selection{background:var(--champagne);color:var(--obsidian)}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.08;letter-spacing:-.015em;margin:0}
p{margin:0 0 1rem}p:last-child{margin-bottom:0}
.wrap{max-width:1080px;margin:0 auto;padding:0 clamp(1.15rem,4vw,2.4rem);position:relative;z-index:2}
.skip{position:absolute;left:-999px;top:0;background:var(--pearl);color:var(--obsidian);padding:.7rem 1rem;z-index:200}
.skip:focus{left:12px;top:12px}
.eyebrow,.kicker{font-size:.7rem;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--champagne)}
.is-muted{color:var(--muted)}

/* header / footer */
.site-header{position:sticky;top:0;z-index:100;background:rgba(11,12,14,.86);
  backdrop-filter:saturate(140%) blur(10px);border-bottom:1px solid var(--line)}
.header-inner{max-width:1080px;margin:0 auto;padding:0 clamp(1.15rem,4vw,2.4rem);height:60px;
  display:flex;align-items:center;gap:1.4rem}
.brand{font-family:var(--serif);font-size:1.28rem;color:var(--porcelain);letter-spacing:-.01em}
.brand b{color:var(--guava);font-weight:500}
.head-nav{display:flex;gap:.2rem;margin-left:auto}
.head-nav a{font-size:.86rem;color:var(--pearl);opacity:.82;padding:.5rem .7rem;transition:opacity .18s var(--ease)}
.head-nav a:hover{opacity:1}
@media(max-width:640px){.head-nav{display:none}}
.site-footer{border-top:1px solid var(--line);margin-top:5rem;padding:3rem 0 2.4rem;background:var(--smoked)}
.footer-inner{max-width:1080px;margin:0 auto;padding:0 clamp(1.15rem,4vw,2.4rem);
  display:grid;gap:2rem;grid-template-columns:1.6fr 1fr 1fr 1fr}
@media(max-width:760px){.footer-inner{grid-template-columns:1fr 1fr}}
.footer-brand p{color:var(--muted);font-size:.88rem;max-width:32ch;margin-top:.6rem}
.footer-col h4{font-family:var(--sans);font-size:.68rem;font-weight:600;letter-spacing:.2em;
  text-transform:uppercase;color:var(--champagne);margin:0 0 .8rem}
.footer-col ul{list-style:none;padding:0;margin:0;display:grid;gap:.5rem}
.footer-col a{font-size:.88rem;color:var(--pearl);opacity:.8}.footer-col a:hover{opacity:1;color:var(--guava)}
.footer-bottom{max-width:1080px;margin:2.2rem auto 0;padding:1.4rem clamp(1.15rem,4vw,2.4rem) 0;
  border-top:1px solid var(--line-2);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;
  font-size:.78rem;color:var(--muted)}

/* breadcrumb */
.crumb{font-size:.78rem;color:var(--muted);margin:1.6rem 0 1.2rem;display:flex;flex-wrap:wrap;gap:.45rem;align-items:center}
.crumb a{color:var(--muted)}.crumb a:hover{color:var(--pearl)}
.crumb .sep{opacity:.4}.crumb [aria-current]{color:var(--pearl)}

/* hero */
.hero{padding:1.4rem 0 2.6rem;border-bottom:1px solid var(--line)}
.hero .kicker{display:block;margin-bottom:1rem}
.hero h1{font-size:clamp(2.7rem,7vw,4.5rem);font-weight:380;letter-spacing:-.022em}
.hero .dek{font-size:1.06rem;color:var(--pearl);opacity:.78;margin:.9rem 0 0;max-width:52ch}

/* hero medallion — a moon-gate monogram, the page's one neon spend */
.hero-top{display:flex;gap:clamp(1.2rem,4vw,2.3rem);align-items:center}
@media(max-width:560px){.hero-top{gap:1.25rem}}
.hero-head{min-width:0}
.medallion{position:relative;flex:none;width:clamp(94px,17vw,126px);height:clamp(94px,17vw,126px);
  border-radius:50%;display:grid;place-items:center;cursor:pointer;
  background:radial-gradient(circle at 50% 36%,var(--smoked-2),var(--obsidian) 74%);
  border:1px solid var(--champagne);
  box-shadow:inset 0 0 0 5px var(--obsidian),inset 0 0 0 6px rgba(197,164,109,.30)}
.medallion::after{content:"";position:absolute;inset:-7px;border-radius:50%;
  border:1px solid rgba(180,107,214,.30);
  box-shadow:0 0 28px 2px rgba(92,44,134,.34);pointer-events:none}
.med-mono{font-family:var(--serif);font-weight:400;line-height:1;letter-spacing:-.02em;
  font-size:clamp(2.3rem,6.5vw,3.2rem);color:var(--porcelain)}
.med-led{position:absolute;top:11%;right:11%;width:11px;height:11px;border-radius:50%;
  background:var(--guava);z-index:3;
  box-shadow:0 0 0 3px rgba(255,63,111,.16),0 0 12px 2px rgba(255,63,111,.75)}
.med-motif{position:absolute;bottom:-11px;left:50%;transform:translateX(-50%);z-index:3;
  --bm-size:26px;background:var(--obsidian);border:1px solid rgba(197,164,109,.42);
  border-radius:50%;padding:6px;box-sizing:content-box}

/* champagne flourish under the title block */
.hero .boba-divider{margin:1.5rem 0 1.25rem}

/* verification ledger — dated chips instead of stars */
.ledger{display:flex;flex-wrap:wrap;gap:.55rem;margin:1.5rem 0 0;list-style:none;padding:0}
.chip{display:inline-flex;align-items:center;gap:.5rem;border:1px solid var(--line);
  border-radius:2px;padding:.42rem .8rem;font-size:.78rem;letter-spacing:.01em;color:var(--pearl);
  background:var(--smoked)}
/* champagne (not neon) dot: the hero keeps a single neon spend — the medallion */
.chip .led{width:7px;height:7px;border-radius:50%;background:var(--champagne);flex:none}
.chip.tag{color:var(--muted);text-transform:uppercase;font-size:.66rem;letter-spacing:.16em}

/* action row */
.actions{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.6rem 0 0}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--sans);font-size:.86rem;font-weight:600;
  letter-spacing:.02em;padding:.7rem 1.2rem;border-radius:2px;border:1px solid var(--line);color:var(--pearl);
  background:transparent;cursor:pointer;transition:border-color .18s var(--ease),color .18s var(--ease);min-height:44px}
.btn:hover{border-color:var(--champagne)}
.btn-primary{background:var(--pearl);color:var(--obsidian);border-color:var(--pearl)}
.btn-primary:hover{background:#fff;border-color:#fff}

/* tonight strip — richer lacquer frame, the LED breathes only when open */
.tonight{position:relative;margin:1.9rem 0 0;border:1px solid var(--line);border-radius:2px;
  background:var(--smoked);padding:.95rem 1.15rem .95rem 1.25rem;display:flex;align-items:center;
  gap:.7rem;font-size:.94rem;overflow:hidden}
.tonight::before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;
  background:var(--champagne);opacity:.5}
.tonight.is-open{border-color:rgba(197,164,109,.34)}
.tonight.is-open::before{background:var(--guava);opacity:.85}
.tonight .led{position:relative;width:8px;height:8px;border-radius:50%;background:var(--muted);flex:none}
.tonight.is-open .led{background:var(--guava);box-shadow:0 0 0 3px rgba(255,63,111,.16),0 0 10px 1px rgba(255,63,111,.7)}
.tonight.is-open .led::after{content:"";position:absolute;inset:-5px;border-radius:50%;
  border:1px solid var(--guava);opacity:0}
.tonight .lbl{color:var(--pearl)}.tonight .sub{color:var(--muted)}
.tonight a{color:var(--champagne);border-bottom:1px solid var(--line)}

/* layout grid */
.grid{display:grid;gap:2.4rem;grid-template-columns:1fr;margin-top:2.6rem}
@media(min-width:880px){.grid{grid-template-columns:1fr 320px;gap:3rem}}
.sec{padding:1.9rem 0;border-top:1px solid var(--line-2)}
.sec:first-child{border-top:0;padding-top:.4rem}
.sec h2{font-size:1.5rem;font-weight:400;margin:0 0 1rem}
.sec .stamp{display:block;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--champagne);margin-top:.9rem}

/* hours accordion */
.hours{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.hours li{display:flex;justify-content:space-between;gap:1rem;padding:.6rem .95rem;font-size:.9rem;
  border-top:1px solid var(--line-2)}
.hours li:first-child{border-top:0}
.hours li.today{background:var(--smoked)}
.hours .d{color:var(--muted)}.hours .t{color:var(--pearl)}
.hours li.today .d,.hours li.today .t{color:var(--porcelain)}
details.acc{border:1px solid var(--line);border-radius:2px}
details.acc>summary{list-style:none;cursor:pointer;padding:.8rem .95rem;font-size:.9rem;color:var(--pearl);
  display:flex;justify-content:space-between;align-items:center}
details.acc>summary::-webkit-details-marker{display:none}
details.acc>summary .mk{color:var(--muted);font-size:.8rem}
details.acc[open]>summary .mk{color:var(--champagne)}
details.acc .hours{border:0;border-top:1px solid var(--line-2);border-radius:0}

/* map — champagne-hairline lacquer frame; the address is the default layer
   so a failed or coord-less map still reads as intentional, never a black box */
.map{border:1px solid rgba(197,164,109,.30);border-radius:2px;overflow:hidden;background:var(--smoked)}
#map-canvas{height:300px;background:var(--smoked);position:relative;z-index:1}
.map-cap{display:flex;justify-content:space-between;align-items:center;gap:.8rem 1rem;flex-wrap:wrap;
  padding:.8rem 1rem;border-top:1px solid var(--line-2);background:var(--smoked-2);
  font-size:.85rem;position:relative;z-index:2}
.map-cap .adr{color:var(--pearl)}.map-cap .adr b{color:var(--porcelain);font-weight:500}
.map-cap a{color:var(--champagne);border-bottom:1px solid var(--line);flex:none}
.map-empty{min-height:216px;display:grid;place-items:center;text-align:center;padding:1.6rem 1.2rem}
.map-empty .moongate{width:76px;height:76px;border-radius:50%;border:1px solid var(--champagne);
  display:grid;place-items:center;margin:0 auto .75rem;
  box-shadow:inset 0 0 0 4px var(--obsidian),inset 0 0 0 5px rgba(197,164,109,.26)}
.map-empty .moongate i{width:9px;height:9px;border-radius:50%;background:var(--champagne);display:block}
.map-empty strong{display:block;font-size:1.02rem;color:var(--porcelain)}
.map-empty span{color:var(--muted);font-size:.88rem}

/* nearby — a scroll-snap rail of motif-accented cards with a peeking next card */
.nearby-rail{display:flex;gap:.7rem;list-style:none;margin:0;padding:.15rem .15rem 1rem;
  overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
.nb-card{flex:0 0 clamp(156px,44%,196px);scroll-snap-align:start}
.nb-card a{display:flex;flex-direction:column;gap:.55rem;height:100%;
  border:1px solid var(--line);border-radius:2px;background:var(--smoked);padding:.9rem .95rem 1rem;
  transition:transform .18s var(--ease),border-color .18s var(--ease)}
.nb-card a:hover{transform:translateY(-3px);border-color:var(--champagne)}
.nb-card .boba-motif{--bm-size:30px;flex:none}
.nb-nm{font-size:.94rem;color:var(--pearl);line-height:1.28}
.nb-card a:hover .nb-nm{color:var(--guava)}
.nb-meta{margin-top:auto;font-size:.76rem;letter-spacing:.05em;color:var(--champagne)}
.nb-meta.ci{color:var(--muted);letter-spacing:0}

/* facts panel */
.facts{border:1px solid var(--line);border-radius:2px;background:var(--smoked);padding:1.3rem}
.facts .fc-title{font-family:var(--sans);font-size:.68rem;font-weight:600;letter-spacing:.2em;
  text-transform:uppercase;color:var(--champagne);margin:0 0 1rem}
.facts dl{margin:0;display:grid;gap:1rem}
.facts dt{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:.2rem}
.facts dd{margin:0;font-size:.92rem;color:var(--pearl)}
.facts dd a{color:var(--pearl);border-bottom:1px solid var(--line)}
.prov{display:block;font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--champagne);opacity:.85;margin-top:.25rem;font-variant:small-caps}

/* nearby rail */
.nearby{list-style:none;margin:0;padding:0;display:grid;gap:.1rem}
.nearby li{border-top:1px solid var(--line-2)}
.nearby li:first-child{border-top:0}
.nearby a{display:flex;justify-content:space-between;gap:1rem;padding:.7rem 0;align-items:baseline}
.nearby .nm{color:var(--pearl);font-size:.94rem}
.nearby a:hover .nm{color:var(--guava)}
.nearby .di{color:var(--champagne);font-size:.78rem;letter-spacing:.04em;flex:none}
.nearby .ci{color:var(--muted);font-size:.78rem;flex:none}

/* order / what-to-order states */
.order-empty{color:var(--muted);font-size:.94rem}
.order-list{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}
.order-list li{display:flex;gap:.7rem;align-items:baseline;font-size:.95rem}
.order-list .led{width:6px;height:6px;border-radius:50%;background:var(--guava);flex:none;margin-top:.5em}

/* claim band */
.claim{margin-top:3rem;border-top:1px solid var(--line);padding-top:2rem;
  display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:center}
.claim p{color:var(--muted);font-size:.9rem;margin:0;max-width:44ch}
.claim a{color:var(--champagne);border-bottom:1px solid var(--line);font-size:.9rem}

/* ---- CLOSED epitaph variant — elevated, but desaturated with no neon ---- */
body.closed{--guava:#6f6d67}
body.closed .wrap,body.closed .site-footer{filter:grayscale(1)}
body.closed .hero{opacity:.94}
body.closed .medallion{border-color:var(--muted-dk);box-shadow:inset 0 0 0 5px var(--obsidian),inset 0 0 0 6px rgba(139,137,129,.22)}
.epitaph{font-size:.86rem;color:var(--muted);margin-top:1.3rem;max-width:46ch}

/* ---- reveal motion (opt-in; static and full-opacity for reduced-motion) ---- */
@media (prefers-reduced-motion: no-preference){
  .ledger .chip{opacity:0;animation:bn-chip-in .5s var(--ease) forwards}
  .ledger .chip:nth-child(1){animation-delay:.04s}
  .ledger .chip:nth-child(2){animation-delay:.12s}
  .ledger .chip:nth-child(3){animation-delay:.20s}
  .ledger .chip:nth-child(4){animation-delay:.28s}
  .tonight.is-open .led::after{animation:bn-led-pulse 2.6s var(--ease) infinite}
}
@keyframes bn-chip-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes bn-led-pulse{0%{transform:scale(.5);opacity:.7}70%{transform:scale(1.9);opacity:0}100%{opacity:0}}

@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}
"""

# ---- head / chrome ----------------------------------------------------------
# The unified site nav, rendered once from build/nav_data.py and baked into
# every profile's <body>: skip link, sticky mega-nav, search overlay, mobile
# drawer, bottom bar. Interpolated as a value into head()'s f-string, so any
# braces inside it are inert.
NAV_HEADER = render_header().rstrip("\n")

def head(title, desc, canonical, robots):
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,380;9..144,400;9..144,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/nav-midnight.css">
<link rel="stylesheet" href="/css/motif.css">
<link rel="stylesheet" href="/css/sound.css">
<style>{STYLE}</style>
</head><body{{BODYCLASS}}>
{NAV_HEADER}
<main id="main" class="wrap">"""

FOOT = """</main>
<footer class="site-footer"><div class="footer-inner">
<div class="footer-brand"><a class="brand" href="/">Boba <b>Night</b></a>
<p>The Southern California boba directory. Real hours, honest rankings, new openings tracked.</p></div>
<div class="footer-col"><h4>By area</h4><ul>
<li><a href="/area/sgv/">The 626</a></li><li><a href="/area/orange-county/">Orange County</a></li>
<li><a href="/area/san-diego/">San Diego</a></li><li><a href="/area/greater-la/">Greater LA</a></li>
<li><a href="/area/inland-empire/">Inland Empire</a></li></ul></div>
<div class="footer-col"><h4>By vibe</h4><ul>
<li><a href="/best/date-night/">Date night</a></li><li><a href="/best/study/">Study-friendly</a></li>
<li><a href="/best/open-late/">Open late</a></li><li><a href="/best/brown-sugar/">Brown sugar</a></li></ul></div>
<div class="footer-col"><h4>About</h4><ul>
<li><a href="/how-we-rank/">How we rank</a></li><li><a href="/report/">Report a correction</a></li>
<li><a href="/about/">About Boba Night</a></li></ul></div>
</div><div class="footer-bottom">
<span>&copy; 2026 Boba Night</span><span class="note">We don't take payment for placement on our best-for lists.</span>
</div></footer>
<script src="/js/nav-midnight.js" defer></script>
<script src="/js/motif.js" defer></script>
<script src="/js/sound.js" defer></script>
</body></html>"""

# ---- weekday_text -> accordion rows ----------------------------------------
DAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
# python weekday(): Mon=0..Sun=6 ; used to mark "today"
def hours_rows(weekday_text, today_idx):
    rows = ""
    for i, line in enumerate(weekday_text):
        if ":" in line:
            d, t = line.split(":", 1)
        else:
            d, t = line, ""
        cls = " today" if i == today_idx else ""
        rows += (f'<li class="{cls.strip()}"><span class="d">{esc(d.strip())}</span>'
                 f'<span class="t">{esc(t.strip())}</span></li>')
    return rows

# ---- tonight strip client JS (bakes periods) --------------------------------
TONIGHT_JS = """
<script>
(function(){
  var P = %PERIODS%;
  var el = document.getElementById('tonight');
  if(!el) return;
  if(!P || !P.length){ return; }
  function laNow(){
    var s = new Date().toLocaleString('en-US',{timeZone:'America/Los_Angeles'});
    return new Date(s);
  }
  function fmt(hhmm){
    var h = parseInt(hhmm.slice(0,2),10), m = parseInt(hhmm.slice(2),10);
    var ap = h>=12?'PM':'AM'; var h12 = h%12; if(h12===0) h12=12;
    return h12 + ':' + (m<10?'0'+m:m) + ' ' + ap;
  }
  var WK = 7*1440;
  var d = laNow();
  var cur = d.getDay()*1440 + d.getHours()*60 + d.getMinutes();
  var openNow = null, nextOpen = null, nextOpenDelta = Infinity;
  for(var i=0;i<P.length;i++){
    var p = P[i]; if(!p.open || !p.close) continue;
    var o = p.open.day*1440 + parseInt(p.open.time.slice(0,2),10)*60 + parseInt(p.open.time.slice(2),10);
    var c = p.close.day*1440 + parseInt(p.close.time.slice(0,2),10)*60 + parseInt(p.close.time.slice(2),10);
    while(c <= o){ c += WK; }
    // test current instant and its previous-week image (for overnight wrap)
    var checks = [cur, cur + WK];
    for(var k=0;k<checks.length;k++){
      if(checks[k] >= o && checks[k] < c){ openNow = p.close.time; }
    }
    // soonest future opening
    var delta = ((o - cur) % WK + WK) % WK;
    if(delta < nextOpenDelta){ nextOpenDelta = delta; nextOpen = p.open.time; }
  }
  if(openNow){
    el.classList.add('is-open');
    el.querySelector('.lbl').textContent = 'Open now';
    el.querySelector('.sub').textContent = '\\u00b7 closes ' + fmt(openNow);
  }else{
    el.classList.remove('is-open');
    el.querySelector('.lbl').textContent = 'Closed now';
    el.querySelector('.sub').textContent = nextOpen ? ('\\u00b7 opens ' + fmt(nextOpen)) : '';
  }
})();
</script>
"""

# ---- lazy Leaflet map JS ----------------------------------------------------
MAP_JS = """
<script>
(function(){
  var host = document.getElementById('map-canvas');
  if(!host) return;
  var lat = %LAT%, lng = %LNG%;
  var loaded = false;
  function load(){
    if(loaded) return; loaded = true;
    var css = document.createElement('link'); css.rel='stylesheet';
    css.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
    document.head.appendChild(css);
    var js = document.createElement('script');
    js.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    js.onload=function(){
      var map = L.map(host,{scrollWheelZoom:false,attributionControl:true}).setView([lat,lng],16);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{
        attribution:'&copy; OpenStreetMap &copy; CARTO', subdomains:'abcd', maxZoom:20
      }).addTo(map);
      L.circleMarker([lat,lng],{radius:7,color:'#C5A46D',weight:2,fillColor:'#ff3f6f',fillOpacity:.9}).addTo(map);
    };
    document.body.appendChild(js);
  }
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(en){
      en.forEach(function(e){ if(e.isIntersecting){ load(); io.disconnect(); } });
    },{rootMargin:'200px'});
    io.observe(host);
  }else{ load(); }
})();
</script>
"""

# ---- render -----------------------------------------------------------------
def render(shop, shops):
    name    = shop.get("name","")
    city    = shop.get("city","")
    addr    = shop.get("address","")
    phone   = shop.get("phone")
    website = shop.get("website")
    lat     = shop.get("latitude")
    lng     = shop.get("longitude")
    place   = shop.get("google_place_id")
    wktext  = shop.get("weekday_text") or []
    periods = shop.get("periods") or []
    status  = (shop.get("status") or "").lower()
    reg     = REGIONS[shop["region"]]
    kicker  = reg["kicker"]
    is_closed = status in CLOSED_STATES
    has_hours = bool(wktext and periods)
    has_coords = lat is not None and lng is not None

    url = f"{SITE}/boba/ca/{shop['city_slug']}/{shop['slug']}/"
    dirn = directions_href(shop)
    today_idx = TODAY.weekday()  # Mon=0..Sun=6, matches weekday_text order above

    # -- indexing rule --
    if (not is_closed) and has_hours and has_coords and status == "open":
        robots = "index,follow"
    else:
        robots = "noindex,follow"

    # -- breadcrumb --
    crumb = f"""
<nav class="crumb" aria-label="Breadcrumb">
<a href="/">Home</a><span class="sep">/</span>
<a href="/area/{shop['region']}/">{esc(reg['label'])}</a><span class="sep">/</span>
<a href="/boba/ca/{shop['city_slug']}/">{esc(city)}</a><span class="sep">/</span>
<span aria-current="page">{esc(name)}</span>
</nav>"""

    # -- hero ledger + dek --
    if is_closed:
        dek = f"Was a {type_phrase(shop.get('store_type'))} in {esc(city)}, {esc(kicker)}. Marked closed."
        ledger = (
            '<ul class="ledger">'
            f'<li class="chip">Closed · marked closed {STAMP}</li>'
            f'<li class="chip tag">{esc(type_chip(shop.get("store_type")))}</li>'
            f'<li class="chip tag">{esc(kicker)}</li>'
            '</ul>')
        actions = ""
        tonight = ""
        epitaph = ('<p class="epitaph">This shop is marked closed in our records as of '
                   f'{STAMP}. We keep the page so an old link still lands somewhere honest '
                   'instead of a dead end.</p>')
    else:
        dek = f"{type_phrase(shop.get('store_type')).capitalize()} in {esc(city)}, {esc(kicker)}."
        verified_chip = (f'<li class="chip"><span class="led"></span>Verified open, checked {STAMP}</li>'
                         if has_hours else
                         f'<li class="chip">Listing confirmed, checked {STAMP}</li>')
        ledger = (
            '<ul class="ledger">'
            f'{verified_chip}'
            f'<li class="chip tag">{esc(type_chip(shop.get("store_type")))}</li>'
            f'<li class="chip tag">{esc(kicker)}</li>'
            '</ul>')
        # action row
        acts = [f'<a class="btn btn-primary" href="{dirn}" rel="nofollow noopener" target="_blank">Directions</a>']
        if phone:
            tel = re.sub(r"[^0-9+]", "", phone)
            acts.append(f'<a class="btn" href="tel:{tel}">Call</a>')
        if website:
            acts.append(f'<a class="btn" href="{esc(website)}" rel="nofollow noopener" target="_blank">Website</a>')
        actions = '<div class="actions">' + "".join(acts) + '</div>'
        # tonight strip
        if has_hours:
            tonight = ('<div class="tonight" id="tonight" role="status">'
                       '<span class="led"></span>'
                       '<span class="lbl">Checking hours…</span> <span class="sub"></span></div>')
        else:
            tonight = ('<div class="tonight" id="tonight-nohours" role="status">'
                       '<span class="led"></span>'
                       '<span class="lbl is-muted">Hours not verified yet.</span> '
                       f'<span class="sub"><a href="{gsearch_hours(shop)}" rel="nofollow noopener" target="_blank">Check Google</a></span></div>')
        epitaph = ""

    # -- hero medallion (moon-gate monogram + bespoke motif accent) --
    mtf   = motif_for(shop["slug"])
    mlbl  = MOTIF_LABEL.get(mtf, "boba")
    mono  = monogram(name)
    # the neon verification dot is spent only on a verified, open shop
    med_led = ('<span class="med-led" aria-hidden="true"></span>'
               if (not is_closed and has_hours) else "")
    medallion = (
        '<div class="medallion boba-surprise">'
        f'<span class="med-mono" aria-hidden="true">{esc(mono)}</span>'
        f'{med_led}'
        f'<span class="boba-motif med-motif" data-motif="{mtf}" aria-label="{esc(mlbl)} motif"></span>'
        '</div>')

    hero = f"""
<section class="hero">
<div class="hero-top">
{medallion}
<div class="hero-head">
<span class="kicker">{esc(city)} · {esc(kicker)}</span>
<h1>{esc(name)}</h1>
<p class="dek">{dek}</p>
</div>
</div>
<div class="boba-divider"></div>
{ledger}
{actions}
{tonight}
{epitaph}
</section>"""

    # -- tonight / hours accordion section --
    if has_hours:
        rows = hours_rows(wktext, today_idx)
        hours_sec = f"""
<section class="sec"><h2>Hours</h2>
<details class="acc" open><summary>This week's hours <span class="mk">expand</span></summary>
<ul class="hours">{rows}</ul></details>
<span class="stamp">Hours verified {STAMP}</span>
</section>"""
    else:
        hours_sec = ""

    # -- what to order (state machine) --
    sig = shop.get("signature_drinks")
    if sig:
        items = "".join(f'<li><span class="led"></span>{esc(x)}</li>' for x in sig)
        order = (f'<section class="sec"><h2>What to order</h2>'
                 f'<ul class="order-list">{items}</ul>'
                 f'<span class="stamp">From the shop’s own menu</span></section>')
    else:
        order = ('<section class="sec"><h2>What to order</h2>'
                 '<p class="order-empty">We list what we can verify. Menu link above, '
                 'nothing invented here.</p></section>')

    # -- map (champagne-hairline frame; address is the always-there default) --
    dir_label = "Open in Maps" if not has_coords else "Directions"
    map_cap = (f'<div class="map-cap"><span class="adr"><b>{esc(name)}</b> · {esc(addr)}, {esc(city)}, CA</span>'
               f'<a href="{dirn}" rel="nofollow noopener" target="_blank">{dir_label}</a></div>')
    if has_coords:
        map_body = f'<div id="map-canvas" aria-label="Map of {esc(name)}"></div>'
        map_js = MAP_JS.replace("%LAT%", repr(lat)).replace("%LNG%", repr(lng))
    else:
        map_body = ('<div class="map-empty"><div><span class="moongate"><i></i></span>'
                    f'<strong>{esc(addr)}</strong><span>{esc(city)}, CA</span></div></div>')
        map_js = ""
    map_sec = (f'<section class="sec"><h2>Find it</h2>'
               f'<div class="map">{map_body}{map_cap}</div></section>')

    # -- facts panel (provenance stamps) --
    facts = [f'<div><dt>Address</dt><dd>{esc(addr)}, {esc(city)}, CA<span class="prov">confirmed {STAMP}</span></dd></div>']
    if phone:
        facts.append(f'<div><dt>Phone</dt><dd>{esc(phone)}<span class="prov">confirmed {STAMP}</span></dd></div>')
    facts.append(f'<div><dt>Area</dt><dd><a href="/area/{shop["region"]}/">{esc(reg["label"])}</a>'
                 f'<span class="prov">confirmed {STAMP}</span></dd></div>')
    facts.append(f'<div><dt>Type</dt><dd>{esc(type_chip(shop.get("store_type")))}'
                 f'<span class="prov">confirmed {STAMP}</span></dd></div>')
    facts_panel = ('<aside class="g-aside"><div class="facts">'
                   f'<p class="fc-title">Find {esc(name)}</p><dl>' + "".join(facts) + '</dl></div></aside>')

    # -- nearby rail --
    nb = nearby(shop, shops)
    nb_items = ""
    for s, dist in nb:
        nmtf = motif_for(s["slug"])
        nlbl = MOTIF_LABEL.get(nmtf, "boba")
        meta = (f'<span class="nb-meta">{esc(dist)}</span>' if dist
                else f'<span class="nb-meta ci">{esc(s.get("city",""))}</span>')
        nb_items += (f'<li class="nb-card"><a href="/boba/ca/{s["city_slug"]}/{s["slug"]}/">'
                     f'<span class="boba-motif" data-motif="{nmtf}" aria-label="{esc(nlbl)} motif"></span>'
                     f'<span class="nb-nm">{esc(s.get("name",""))}</span>{meta}</a></li>')
    nb_title = "Still pouring nearby" if is_closed else "Nearby"
    nearby_sec = f'<section class="sec"><h2>{nb_title}</h2><ul class="nearby-rail">{nb_items}</ul></section>'

    # -- claim band --
    claim = ('<div class="claim">'
             '<p>Is this your shop? Correct the hours, add the menu, flag anything wrong.</p>'
             '<a href="/claim/">Claim this listing</a></div>')

    main = f"""{crumb}{hero}
<div class="grid"><div class="g-main">
{map_sec}
{hours_sec}
{order}
{nearby_sec}
</div>
{facts_panel}
</div>
{claim}"""

    # -- JSON-LD --
    shop_ld = {
        "@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":name,
        "@id":url + "#shop","url":url,"servesCuisine":"Bubble Tea",
        "address":{"@type":"PostalAddress","streetAddress":addr,"addressLocality":city,
                   "addressRegion":"CA","addressCountry":"US"},
    }
    if has_coords:
        shop_ld["geo"] = {"@type":"GeoCoordinates","latitude":lat,"longitude":lng}
    if phone:
        shop_ld["telephone"] = phone
    if website:
        shop_ld["sameAs"] = [website]
    if place:
        shop_ld["hasMap"] = f"https://www.google.com/maps/place/?q=place_id:{place}"
    if has_hours:
        specs = []
        DOW = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        for p in periods:
            if not p.get("open") or not p.get("close"): continue
            ot, ct = p["open"]["time"], p["close"]["time"]
            specs.append({"@type":"OpeningHoursSpecification",
                          "dayOfWeek":f"https://schema.org/{DOW[p['open']['day']]}",
                          "opens":f"{ot[:2]}:{ot[2:]}","closes":f"{ct[:2]}:{ct[2:]}"})
        if specs:
            shop_ld["openingHoursSpecification"] = specs
    if is_closed:
        # signal a closed listing to consumers of the schema
        shop_ld["additionalProperty"] = {"@type":"PropertyValue","name":"status","value":"permanentlyClosed"}

    breadcrumb_ld = {
        "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE}/"},
            {"@type":"ListItem","position":2,"name":reg["label"],"item":f"{SITE}/area/{shop['region']}/"},
            {"@type":"ListItem","position":3,"name":city,"item":f"{SITE}/boba/ca/{shop['city_slug']}/"},
            {"@type":"ListItem","position":4,"name":name,"item":url},
        ]}
    ld = (f'<script type="application/ld+json">{json.dumps(shop_ld, ensure_ascii=False)}</script>\n'
          f'<script type="application/ld+json">{json.dumps(breadcrumb_ld, ensure_ascii=False)}</script>')

    # -- client scripts --
    scripts = ""
    if not is_closed and has_hours:
        scripts += TONIGHT_JS.replace("%PERIODS%", json.dumps(periods, ensure_ascii=False))
    if not is_closed and has_coords:
        scripts += map_js  # closed pages keep the static-ish canvas but no guava; still fine to load
    elif has_coords and is_closed:
        scripts += map_js

    # -- title / desc --
    if is_closed:
        title = f"{name}, {city}: Closed (Boba) | Boba Night"
        desc  = f"{name} at {addr}, {city} is marked closed. Still-open boba nearby. Boba Night."
    else:
        title = f"{name}, {city}: Boba Hours, Menu & Map (2026) | Boba Night"
        desc  = f"{name} at {addr}, {city}. Hours, directions, and what to order. Boba Night."

    bodyclass = ' class="closed"' if is_closed else ""
    page = (head(title, desc, url, robots).replace("{BODYCLASS}", bodyclass)
            + main + ld + scripts + FOOT)
    return page, url


def out_path_for(shop):
    return os.path.join(ROOT, "boba", "ca", shop["city_slug"], shop["slug"], "index.html")

def main(argv):
    shops = load_shops()
    by_slug = {s["slug"]: s for s in shops}

    if "--all" in argv:
        # Hand-edited featured house — never regenerate it.
        SKIP = {"taro-yuan-city-of-industry"}
        wrote = idx = noidx = 0
        for shop in shops:
            if shop["slug"] in SKIP:
                continue
            page, _ = render(shop, shops)
            if 'name="robots" content="index,follow"' in page:
                idx += 1
            else:
                noidx += 1
            p = out_path_for(shop)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(page)
            wrote += 1
        print(f"wrote {wrote} profiles (skipped {len(SKIP)}): "
              f"{idx} index,follow / {noidx} noindex,follow")
        return 0

    if not argv:
        print("usage: gen_profiles.py <slug> [--out PATH] | --all", file=sys.stderr)
        return 2
    slug = argv[0]
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    shop = by_slug.get(slug)
    if not shop:
        print(f"unknown slug: {slug}", file=sys.stderr)
        return 1
    page, url = render(shop, shops)
    dest = out or out_path_for(shop)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(page)
    print(f"wrote {dest}  ({url})  status={shop.get('status')}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
