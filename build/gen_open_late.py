#!/usr/bin/env python3
"""
build/gen_open_late.py  —  the bespoke generator for /best/open-late/.

This page is OWNED here (like profiles are owned by gen_profiles.py). gen_site.py
must NOT write best/open-late/index.html or it would clobber this. gen_site skips
the 'open-late' slug in its INTENT loop.

Hybrid architecture:
  * Static shell (this generator): every internal link, the ranked late list, the
    city grid, landmark rows, learn cards, FAQ and all JSON-LD are baked to HTML —
    the SEO / GEO / AI-Overview surface, readable with JS off.
  * Live layer (js/open-late.js): refreshes the full late set from Supabase
    (niteboba_finder) and powers open-now, the time slider, the map, shuffle and
    the crawl builder. New DB rows appear with no rebuild.

Nothing renders without a verified field behind it (Rule 1).

Usage:
  python3 build/gen_open_late.py --preview /path/out.html   # self-contained preview
  python3 build/gen_open_late.py --build                    # write live page (linked assets)
"""
import json, os, sys, html, re, datetime

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE  = "https://www.bobanight.com"
TODAY = datetime.date.today().isoformat()
DATA  = os.path.join(ROOT, "build", "open-late-data.json")

# ---- region map (kept local so preview never depends on nav_data) ----
SGV_CITIES = {"Arcadia","Covina","Pasadena","Walnut","Rowland Heights","Monterey Park","City of Industry",
              "El Monte","Diamond Bar","Rosemead","San Gabriel","Baldwin Park","Temple City","Monrovia",
              "West Covina","South Pasadena","San Marino","Alhambra","Azusa","Glendora","San Dimas","La Verne",
              "Duarte","Claremont","La Cañada Flintridge"}
def region_of(county, city):
    if county == "Orange": return "orange-county"
    if county == "San Diego": return "san-diego"
    if county in ("Riverside","San Bernardino"): return "inland-empire"
    if county == "Ventura": return "ventura"
    if county == "Los Angeles": return "sgv" if city in SGV_CITIES else "greater-la"
    return "greater-la"
AREA = {
  "sgv": ("The 626","/area/sgv/"), "greater-la": ("Greater LA","/area/greater-la/"),
  "orange-county": ("Orange County","/area/orange-county/"), "san-diego": ("San Diego","/area/san-diego/"),
  "inland-empire": ("Inland Empire","/area/inland-empire/"), "ventura": ("Ventura County","/area/ventura/"),
}
DOW = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

def esc(s): return html.escape("" if s is None else str(s), quote=True)
def slugify(s):
    s = (s or "").lower().strip()
    s = re.sub(r"['\".]", "", s); s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")
def hrlabel(h):
    if h is None: return ""
    if h == 24: return "midnight"
    x = h % 24; ap = "AM" if x < 12 else "PM"; hh = x % 12 or 12
    return "%d %s" % (hh, ap)

# ---- data load + enrich ----
def load():
    d = json.load(open(DATA, encoding="utf-8"))
    for grp in ("seed","gems"):
        for sh in d[grp]:
            sh["cs"] = slugify(sh["ci"]); sh["rg"] = region_of(sh.get("co"), sh["ci"])
            prof = os.path.join(ROOT, "boba", "ca", sh["cs"], sh["s"], "index.html")
            sh["prof"] = os.path.exists(prof)
            sh["url"] = "/boba/ca/%s/%s/" % (sh["cs"], sh["s"]) if sh["prof"] else "/boba/ca/%s/" % sh["cs"]
    for c in d["cities"]:
        c["cs"] = slugify(c["city"]); c["rg"] = region_of(c.get("county"), c["city"])
    return d

# ---- shop card (static; JS repaints live open/closed) ----
def scard(sh, gem=False):
    dirurl = "https://www.google.com/maps/dir/?api=1&destination=%s,%s" % (sh["la"], sh["lo"])
    rat = ('<span class="rat">★ %.1f</span> <span>%s on Google</span>' % (round(sh["r"],1), sh.get("rv") or 0)) if sh.get("r") else ""
    pill = '<span class="ol-pill soon"><span class="led"></span>Until %s</span>' % hrlabel(sh["lc"])
    cls = "ol-card ol-card--gem" if gem else "ol-card"
    star = ('<button class="ol-star" data-save="%s" aria-label="Save %s" title="Save to your black book">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-9.2-8.4A5 5 0 0 1 12 6a5 5 0 0 1 9.2 5.6C19 15.6 12 20 12 20z"/></svg></button>'
            ) % (esc(sh["s"]), esc(sh["nm"]))
    return ('<article class="%s" data-slug="%s"><div class="ol-card-top"><a class="nm" href="%s">%s</a>%s</div>'
            '<div class="meta"><a href="/boba/ca/%s/">%s</a>%s</div>%s'
            '<div class="ol-actions"><a class="ol-mini pri" href="%s" target="_blank" rel="nofollow noopener">Directions</a>'
            '<button class="ol-mini" data-crawl="%s">+ Add to crawl</button></div></article>') % (
        cls, esc(sh["s"]), sh["url"], esc(sh["nm"]), star, sh["cs"], esc(sh["ci"]),
        (" <span>·</span> " + rat) if rat else "", pill, dirurl, esc(sh["s"]))

# ---- landmarks that already have a crawlable /near/ page ----
LANDMARKS = [
    ("disneyland","Disneyland & Downtown Disney","Anaheim"),
    ("south-coast-plaza","South Coast Plaza","Costa Mesa"),
    ("uc-irvine","UC Irvine","Irvine"),
    ("cal-state-fullerton","Cal State Fullerton","Fullerton"),
    ("the-americana","The Americana at Brand","Glendale"),
    ("convoy-district","The Convoy District","San Diego"),
    ("ucla","UCLA & Westwood","Los Angeles"),
    ("uc-san-diego","UC San Diego","La Jolla"),
]
DRINKS = [
    ("Brown sugar","/guide/brown-sugar-vs-tiger-sugar/"),
    ("Fresh fruit tea","/best/fruit-tea/"),
    ("Matcha","/best/matcha/"),
    ("Cheese foam","/guide/what-is-cheese-foam/"),
    ("Crystal boba","/guide/crystal-boba-vs-tapioca/"),
    ("Non-dairy","/guide/order-non-dairy-boba/"),
    ("The whole pantry","/pantry/"),
]
COLLECTIONS = [
    ("Date night","/best/date-night/"),("Study-friendly","/best/study/"),
    ("Best matcha","/best/matcha/"),("Best brown sugar","/best/brown-sugar/"),
    ("Fresh fruit tea","/best/fruit-tea/"),("Non-dairy","/best/non-dairy/"),
    ("Groups","/best/group/"),("Drive-thru","/best/drive-thru/"),
    ("Best value","/best/cheap/"),("Boba & food","/best/with-food/"),
    ("First date","/best/first-date/"),("Boba near me","/near-me/"),
]

def build_body(d):
    b = d["buckets"]; seed = d["seed"]; gems = d["gems"]; cities = d["cities"]
    p9,p10,p11,p12,p1 = b["p9"],b["p10"],b["p11"],b["p12"],b["p1"]
    latest = max((s["lc"] for s in seed), default=24)
    latest_shop = next((s for s in seed if s["lc"] == latest), seed[0])

    # breadcrumb + hero (page-head preserved)
    crumb = ('<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a>'
             '<span class="boba-motif crumb-sep" data-motif="pearl" aria-hidden="true"></span>'
             '<a href="/best/">By vibe</a><span class="boba-motif crumb-sep" data-motif="pearl" aria-hidden="true"></span>'
             '<span aria-current="page">Open late</span></nav>')
    hero = ('<div class="page-head"><p class="eyebrow">Open late · Southern California</p>'
            '<h1>Late-night boba and dessert, still open across SoCal</h1>'
            '<p class="lede">Right now <b>%d</b> boba and dessert shops in Southern California are open past 9 PM, and <b>%d</b> are still pouring past midnight. '
            'This is a live map of what\'s actually open tonight, sorted by how late, drawn from verified hours, and refreshed every night. '
            'Pick a time, a mood, or your city.</p></div>') % (p9, p12)

    # answer strip (GEO quotable)
    stats = ''.join('<div class="ol-stat%s"><span class="n">%d</span><span class="l">%s</span></div>' % (c, n, l)
                    for n, l, c in [(p9,"open past 9 PM",""),(p10,"open past 10 PM",""),(p11,"open past 11 PM",""),
                                    (p12,"open past midnight"," is-hot"),(p1,"open past 1 AM"," is-hot")])
    answer = ('<section class="ol-sec" id="tonight"><div class="ol-head"><p class="eyebrow">Tonight at a glance</p>'
              '<h2>What\'s open late in Southern California right now</h2>'
              '<p class="ol-answer" data-speakable>As of %s, <b>%d</b> boba and dessert shops in Southern California stay open past 9 PM, <b>%d</b> past 11 PM and <b>%d</b> past midnight. '
              'The latest, %s in %s, pours until %s on weekends.</p></div>'
              '<div class="ol-stats">%s</div>'
              '<div class="ol-sticky"><div class="ol-sticky-in"><span class="lab">Live</span>'
              '<span class="val" id="ol-sticky-val"><b>—</b> open now</span>'
              '<a href="#map">Jump to the map</a></div></div></section>') % (
        TODAY, p9, p11, p12, esc(latest_shop["nm"]), esc(latest_shop["ci"]), hrlabel(latest), stats)

    # open now
    seed_sorted = sorted(seed, key=lambda s: (-s["lc"], -(s.get("r") or 0)))
    opennow = ('<section class="ol-sec" id="open-now"><div class="ol-head"><p class="eyebrow">Open right now</p>'
               '<h2>Open right now, and how late they go</h2>'
               '<p class="ol-answer">Tap a window to see the shops. Open-now is computed live in Pacific time from each shop\'s verified hours, '
               'so it changes as the night goes on. <span id="ol-live-note" class="ol-sub">Loading the full set live…</span></p></div>'
               '<div class="ol-live" id="ol-live"></div>'
               '<div id="ol-live-list">%s</div></section>') % (
        '<p class="ol-count">%d late shops tonight</p><div class="ol-grid">%s</div>' % (len(seed), ''.join(scard(s) for s in seed_sorted[:24])))

    # time slider
    slider = ('<section class="ol-sec" id="by-time"><div class="ol-head"><p class="eyebrow">Choose your time</p>'
              '<h2>Drag to the hour you\'ll actually go out</h2>'
              '<p class="ol-answer">Slide from 8 PM to 2 AM and the whole set filters to what\'s still open then.</p></div>'
              '<div class="ol-time"><div class="ol-time-read" id="ol-slider-read"></div>'
              '<input class="ol-range" id="ol-slider" type="range" min="1200" max="1560" step="30" value="1320" '
              'aria-label="Choose a time between 8 PM and 2 AM">'
              '<div class="ol-ticks" id="ol-slider-ticks"></div></div>'
              '<div id="ol-slider-list" style="margin-top:1.2rem"></div></section>')

    # mood
    mood = ('<section class="ol-sec" id="tonights-plan"><div class="ol-head"><p class="eyebrow">What are you doing tonight?</p>'
            '<h2>Pick the night, we\'ll narrow it down</h2>'
            '<p class="ol-answer">These filter the live set by how late they run. Looking for a vibe instead? '
            '<a href="/best/date-night/">Date night</a>, <a href="/best/study/">study spots</a> and <a href="/best/group/">groups</a> have their own rooms.</p></div>'
            '<div class="ol-chips" id="ol-mood-chips"></div><div id="ol-mood-list"></div></section>')

    # map
    mapsec = ('<section class="ol-sec" id="map"><div class="ol-head"><p class="eyebrow">Late-night hotspots</p>'
              '<h2>The map of everywhere still open</h2>'
              '<p class="ol-answer">Green pins are open right now; gold pins are late tonight. Tap a pin for hours and directions.</p></div>'
              '<div class="ol-map" id="ol-map"><div class="ol-map-fallback">Loading the night map…</div></div></section>')

    # hidden gems
    gemsec = ('<section class="ol-sec" id="hidden-gems"><div class="ol-head"><p class="eyebrow">Hidden gems open late</p>'
              '<h2>High ratings, smaller crowds, still open</h2>'
              '<p class="ol-answer">Shops rated 4.5★ or better with fewer than 300 Google reviews that stay open late. The ones the algorithms haven\'t flooded yet.</p></div>'
              '<div id="ol-gems"><div class="ol-grid">%s</div></div></section>') % ''.join(scard(g, gem=True) for g in gems)

    # crawl
    crawl = ('<section class="ol-sec" id="crawl"><div class="ol-head"><p class="eyebrow">Build a late-night crawl</p>'
             '<h2>Chain two or three stops into one run</h2>'
             '<p class="ol-answer">Add stops from any shop above, then open the whole route in Maps or send it to whoever\'s driving.</p></div>'
             '<div class="ol-crawl"><div id="ol-crawl-list"></div>'
             '<div class="ol-crawl-foot" id="ol-crawl-foot" style="display:none">'
             '<span class="tot" id="ol-crawl-tot"></span>'
             '<button class="ol-mini pri" id="ol-crawl-open">Open in Maps</button>'
             '<button class="ol-mini" id="ol-crawl-share">Share crawl</button>'
             '<button class="ol-mini" id="ol-crawl-clear">Clear</button></div></div></section>')

    # shuffle
    shuffle = ('<section class="ol-sec" id="surprise"><div class="ol-head"><p class="eyebrow">Feeling adventurous</p>'
               '<h2>Can\'t decide? Let the night pick.</h2></div>'
               '<div class="ol-shuffle"><div class="prompt"><p>We\'ll pull one spot that\'s open late tonight, with directions and a slot for your crawl.</p>'
               '<button class="ol-dice" id="ol-shuffle-btn">🎲 Pick for me</button></div>'
               '<div class="ol-shuffle-out" id="ol-shuffle-out"></div></div></section>')

    # explore by city
    top_cities = [c for c in cities if c["n_late"] >= 1][:40]
    citycards = ''.join(('<a class="ol-row" href="/boba/ca/%s/"><span class="rl">%s</span>'
                         '<span class="rr"><b>%d</b> open late<br>to %s</span></a>') % (
                        c["cs"], esc(c["city"]), c["n_late"], hrlabel(c["latest"])) for c in top_cities)
    citysec = ('<section class="ol-sec" id="by-city"><div class="ol-head"><p class="eyebrow">Explore by city</p>'
               '<h2>Late-night boba by city</h2>'
               '<p class="ol-answer">%d SoCal cities have at least one shop open past 9 PM. Rowland Heights leads with %d, then San Diego and Los Angeles.</p></div>'
               '<div class="ol-rows">%s</div>'
               '<p class="ol-more"><a href="/directory/">See every SoCal boba shop in the directory</a></p></section>') % (
        len(cities), cities[0]["n_late"], citycards)

    # perfect after (landmarks)
    lmrows = ''.join(('<a class="ol-row" href="/near/%s/"><span class="rl">%s</span>'
                      '<span class="rr">late boba near<br><b>%s</b></span></a>') % (sl, esc(nm), esc(area))
                     for sl, nm, area in LANDMARKS)
    perfect = ('<section class="ol-sec" id="perfect-after"><div class="ol-head"><p class="eyebrow">Perfect after…</p>'
               '<h2>Dessert after the main event</h2>'
               '<p class="ol-answer">The late boba nearest the places SoCal actually goes at night. Coming after Korean BBQ or hot pot? '
               'Those neighborhood guides are next on the list.</p></div>'
               '<div class="ol-rows">%s</div></section>') % lmrows

    # popular drinks (educational, links only — no fabricated per-shop menus)
    dchips = ''.join('<a class="ol-chip" href="%s">%s</a>' % (u, esc(n)) for n, u in DRINKS)
    drinks = ('<section class="ol-sec" id="drinks"><div class="ol-head"><p class="eyebrow">Popular late-night drinks</p>'
              '<h2>What to order when it\'s late</h2>'
              '<p class="ol-answer">Tap a drink to learn what it is and who does it well. Per-shop menus (“who\'s serving brown sugar tonight”) are the next thing we\'re wiring in.</p></div>'
              '<div class="ol-chips">%s</div></section>') % dchips

    # learn
    LEARN = [
        ("Why do some boba shops stay open so late?",
         "The latest spots cluster where night traffic already exists: the San Gabriel Valley tea corridor, Little Saigon, and college and nightlife pockets. Weekend hours usually run one to two hours later than weekdays."),
        ("Best caffeine-free drinks for a late night?",
         "Fruit teas, taro, and milk blends can be made with an herbal base or no tea at all. Ask for a caffeine-free base; most shops keep one. See the <a href=\"/pantry/\">Pantry</a> for what goes in each."),
        ("Milk tea or fruit tea after dinner?",
         "After a heavy meal, a lighter <a href=\"/best/fruit-tea/\">fresh fruit tea</a> or a milk tea at 25 to 50 percent sweetness sits better than a full-sugar brown sugar. Cheese foam adds richness without more sugar in the tea."),
        ("What does 50% sweet actually mean?",
         "It is roughly half the shop default syrup, not half the flavor. Late at night many people drop to 25 to 50 percent. <a href=\"/guide/what-50-percent-sweet-means/\">Read what 50% sweet means</a>."),
        ("What is cheese foam?",
         "A lightly salted cap of whipped cream and cream cheese over tea, savory and sweet, best sipped through the foam rather than stirred. <a href=\"/guide/what-is-cheese-foam/\">Read about cheese foam</a>."),
        ("Brown sugar vs tiger sugar?",
         "Same idea: pearls cooked in brown sugar syrup, with tiger sugar naming the striped look on the cup. What matters is whether the pearls are cooked to order. <a href=\"/guide/brown-sugar-vs-tiger-sugar/\">Compare brown sugar and tiger sugar</a>."),
    ]
    learn = ('<section class="ol-sec" id="learn"><div class="ol-head"><p class="eyebrow">Learn</p>'
             '<h2>Good to know for a late run</h2></div><div class="ol-learn">%s</div></section>') % ''.join(
        '<details%s><summary>%s</summary><p class="ans">%s</p></details>' % (" open" if i==0 else "", esc(q), a)
        for i,(q,a) in enumerate(LEARN))

    # related collections
    rel = ''.join('<a class="ol-chip" href="%s">%s</a>' % (u, esc(n)) for n, u in COLLECTIONS)
    related = ('<section class="ol-sec" id="related"><div class="ol-head"><p class="eyebrow">Keep exploring</p>'
               '<h2>Related collections</h2></div><div class="ol-chips">%s</div></section>') % rel

    # FAQ (mirrors FAQPage schema)
    mid_names = ", ".join(esc(s["nm"]) for s in sorted([s for s in seed if s["lc"]>=24], key=lambda s:-s["lc"])[:3])
    FAQ = [
        ("What boba is open right now near me in SoCal?",
         "About %d SoCal boba shops stay open past 9 PM. The map and “open now” list at the top of this page compute what\'s open this minute from verified hours in Pacific time." % p9),
        ("Where can I get boba after midnight in Southern California?",
         "Roughly %d shops stay open past midnight, including %s. Use the “open past midnight” card above for tonight\'s live list." % (p12, mid_names)),
        ("What boba shop is open the latest in SoCal?",
         "%s in %s runs the latest we have verified. It pours until %s on weekends, and a handful of others hold until 1 to 2 AM." % (esc(latest_shop["nm"]), esc(latest_shop["ci"]), hrlabel(latest))),
        ("Where is late-night boba in Rowland Heights?",
         "Rowland Heights has the most late boba in SoCal. %d shops stay open past 9 PM, several until midnight or 1 AM. See the <a href=\"/boba/ca/rowland-heights/\">Rowland Heights list</a>." % cities[0]["n_late"]),
        ("Is any boba open 24 hours?",
         "Not truly 24 hours. SoCal boba tops out around 2 AM on weekends, and 4 AM at one Alhambra spot. For the latest options, use the time slider above."),
    ]
    faq = ('<section class="ol-sec faq" id="faq"><div class="ol-head"><p class="eyebrow">Questions</p>'
           '<h2>Late-night boba, answered</h2></div>%s</section>') % ''.join(
        '<h3>%s</h3><p>%s</p>' % (esc(q), a) for q, a in FAQ)

    body = crumb + hero + answer + opennow + slider + mood + mapsec + gemsec + crawl + shuffle + citysec + perfect + drinks + learn + related + faq

    # ---- injected data + schema ----
    def slim(sh):
        return {k: sh[k] for k in ("s","nm","ci","cs","la","lo","r","rv","pl","per","lc","url") if k in sh}
    injected = json.dumps({"seed":[slim(s) for s in seed], "gems":[slim(g) for g in gems], "generated": TODAY}, separators=(",",":"))

    def ohs(per):
        out=[]
        for p in per:
            if not p.get("o") or p.get("c") is None: continue
            o,c = p["o"], p["c"]
            out.append({"@type":"OpeningHoursSpecification","dayOfWeek":"https://schema.org/"+DOW[p["d"]],
                        "opens":o[:2]+":"+o[2:], "closes":c[:2]+":"+c[2:]})
        return out
    items=[]
    for i, s in enumerate(seed_sorted[:20]):
        biz={"@type":"CafeOrCoffeeShop","name":s["nm"],"servesCuisine":"Bubble Tea",
             "address":{"@type":"PostalAddress","addressLocality":s["ci"],"addressRegion":"CA","addressCountry":"US"},
             "geo":{"@type":"GeoCoordinates","latitude":s["la"],"longitude":s["lo"]},
             "url":SITE+s["url"],"openingHoursSpecification":ohs(s["per"])}
        if s.get("r"): biz["aggregateRating"]={"@type":"AggregateRating","ratingValue":round(s["r"],1),"reviewCount":s.get("rv") or 0,"@id":SITE+s["url"]+"#gr"}
        items.append({"@type":"ListItem","position":i+1,"item":biz})
    url = SITE + "/best/open-late/"
    schema_blocks = [
        {"@context":"https://schema.org","@type":"CollectionPage","@id":url+"#page","url":url,
         "name":"Late-Night Boba & Dessert Open Now in Southern California",
         "description":"Live directory of SoCal boba and dessert shops open late, sorted by how late, from verified hours.",
         "isPartOf":{"@type":"WebSite","name":"Boba Night","url":SITE+"/"},
         "dateModified":TODAY,
         "speakable":{"@type":"SpeakableSpecification","cssSelector":["h1","[data-speakable]"]},
         "mainEntity":{"@type":"ItemList","name":"Boba open late in Southern California","numberOfItems":len(items),"itemListElement":items}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
            {"@type":"ListItem","position":2,"name":"By vibe","item":SITE+"/best/"},
            {"@type":"ListItem","position":3,"name":"Open late","item":url}]},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r"<[^>]+>","",a)}} for q,a in FAQ]},
    ]
    schema = "".join('<script type="application/ld+json">%s</script>' % json.dumps(bl, separators=(",",":")) for bl in schema_blocks)
    return body, injected, schema

# ---- shells ----
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">'
LEAFLET_JS  = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>'
TITLE = "Late-Night Boba & Dessert Open Now in Southern California (2026) | Boba Night"
DESC  = "Live map of SoCal boba and dessert shops open late: open now, past 10, 11, midnight and 1 AM. Verified hours, by city and landmark. Boba Night."

def build_page():
    d = load(); body, injected, schema = build_body(d)
    sys.path.insert(0, os.path.join(ROOT, "build"))
    from gen_site import head, foot
    top = head(TITLE, DESC, SITE + "/best/open-late/", noindex=False)
    top = top.replace("</head>", '  ' + LEAFLET_CSS + '\n  <link rel="stylesheet" href="/css/open-late.css">\n</head>')
    scripts = (LEAFLET_JS + '<script>window.__OL__=' + injected + ';</script>'
               + '<script src="/js/open-late.js" defer></script>')
    bottom = foot().replace("</body>", scripts + "\n</body>")
    out = top + body + schema + bottom
    dest = os.path.join(ROOT, "best", "open-late", "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(out)
    print("BUILD wrote", dest, "(%d bytes)" % len(out))

def read(p):
    try: return open(os.path.join(ROOT, p), encoding="utf-8").read()
    except Exception: return ""

def build_preview(dest):
    d = load(); body, injected, schema = build_body(d)
    cur = read("best/open-late/index.html")
    # Preview uses a minimal top bar; PRODUCTION (--build) keeps the real, untouched
    # site nav via gen_site.head(). (The full mega-nav's overlay/drawer are stateful
    # and only look right served in-site, so we don't replicate them in the preview.)
    nav = ('<div class="ol-prevbadge">Preview · v2 — content below the hero</div>'
           '<header class="bn-header"><div class="bn-bar">'
           '<a class="bn-word" href="#">Boba <b>Night</b></a>'
           '<nav class="bn-nav-lite" aria-label="Primary"><a href="#by-city">By city</a>'
           '<a href="#map">Map</a><a href="#hidden-gems">Hidden gems</a><a href="#crawl">Build a crawl</a></nav>'
           '<a class="bn-cta" href="#tonight">Tonight</a></div></header>')
    foot_html = cur[cur.index("</main>")+7 : cur.index("</body>")] if "</main>" in cur and "</body>" in cur else ""
    foot_html = re.sub(r'<script src="/js/[^"]+"[^>]*></script>\s*', "", foot_html)  # we inline JS below
    prevcss = (".ol-prevbadge{position:fixed;top:10px;right:10px;z-index:500;background:var(--neon);color:#fff;"
               "font:600 .66rem/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;padding:.45rem .7rem;border-radius:2px}"
               ".bn-nav-lite{display:flex;gap:1.4rem;margin-left:2rem}.bn-nav-lite a{color:var(--silver);font-size:.9rem;font-weight:500}"
               ".bn-nav-lite a:hover{color:var(--pearl)}@media(max-width:760px){.bn-nav-lite{display:none}}")
    css = "\n".join(read("css/"+f) for f in ("site.css","nav-midnight.css","motif.css","open-late.css")) + "\n" + prevcss
    js  = read("js/open-late.js")
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')
    doc = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
           "<title>PREVIEW · " + esc(TITLE) + "</title><meta name=\"robots\" content=\"noindex\">"
           "<meta name=\"theme-color\" content=\"#0B0C0E\">" + fonts + LEAFLET_CSS +
           "<style>" + css + "</style></head><body>" + nav +
           '<main id="main" class="wrap">' + body + schema + "</main>" + foot_html +
           LEAFLET_JS + "<script>window.__OL__=" + injected + ";</script>" +
           "<script>" + js + "</script></body></html>")
    open(dest, "w", encoding="utf-8").write(doc)
    print("PREVIEW wrote", dest, "(%d bytes)" % len(doc))

if __name__ == "__main__":
    if "--build" in sys.argv:
        build_page()
    elif "--preview" in sys.argv:
        i = sys.argv.index("--preview"); dest = sys.argv[i+1] if len(sys.argv) > i+1 else "/tmp/open-late-preview.html"
        build_preview(dest)
    else:
        print("usage: gen_open_late.py --preview <path> | --build")
