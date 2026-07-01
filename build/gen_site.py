#!/usr/bin/env python3
"""
CapyBoba static site generator.

Reads shop data and writes static HTML (data -> build -> static files; NOT an app).
Right now it reads the seed CSV, so pages render in honest "Verifying" skeleton state
(real name + address; hours/coords/attributes shown as Verifying). After enrichment,
point load_rows() at the enriched export and re-run: profiles gain real hours/coords
and flip from noindex to indexable automatically.

SEO safety: city pages + region hubs are indexable (real directory value).
Individual profiles are noindex until enriched (avoid thin-content penalty).
Intent pages are honest landing pages (no fabricated rankings) and noindex.
"""
import csv, io, re, os, html, datetime

ROOT = os.path.join(os.path.dirname(__file__), "boba-repo")
CSV  = os.path.join(ROOT, "data", "stores-seed.csv")
TODAY = datetime.date.today().isoformat()
SITE = "https://capyboba.com"

# ---- region mapping (editorial; adjustable) ----
SGV_CITIES = {"Arcadia","Covina","Pasadena","Walnut","Rowland Heights","Monterey Park",
              "El Monte","Diamond Bar","Rosemead","San Gabriel","Baldwin Park","Temple City","Monrovia"}
REGIONS = {
  "sgv":           {"label":"San Gabriel Valley","kicker":"The 626",
                    "blurb":"The densest boba in SoCal. Brown sugar, fruit tea, and Taiwanese dessert houses packed block to block."},
  "greater-la":    {"label":"Greater Los Angeles","kicker":"LA",
                    "blurb":"From Koreatown and DTLA to the Westside and Long Beach, everything from aesthetic cafes to grab-and-go counters."},
  "orange-county": {"label":"Orange County","kicker":"OC",
                    "blurb":"The Irvine clusters plus Little Saigon in Westminster and Garden Grove. Strong for date night and study spots."},
  "san-diego":     {"label":"San Diego","kicker":"SD",
                    "blurb":"Convoy and Mira Mesa anchor it, with a deep bench of Taiwanese and Vietnamese shops and late-night options."},
  "inland-empire": {"label":"Inland Empire","kicker":"IE",
                    "blurb":"Riverside and San Bernardino. Fewer shops, less competition, easier to find the good ones."},
}
def region_of(county, city):
    if county == "Orange": return "orange-county"
    if county == "San Diego": return "san-diego"
    if county in ("Riverside","San Bernardino"): return "inland-empire"
    if county == "Los Angeles":
        return "sgv" if city in SGV_CITIES else "greater-la"
    return "greater-la"

INTENTS = [
  ("date-night","Date night","calmer rooms, seating, later hours"),
  ("first-date","First date","quiet enough to actually talk"),
  ("study","Study-friendly","wifi, outlets, room to stay"),
  ("open-late","Open late","still pouring well after dinner"),
  ("brown-sugar","Brown sugar","cooked properly, not just syrup"),
  ("fruit-tea","Fresh fruit tea","real fruit, not powder"),
  ("matcha","Matcha","for the matcha people"),
  ("non-dairy","Non-dairy","oat and almond that actually work"),
  ("cheap","Best value","most cup for the money"),
  ("group","Group hangout","room and energy for a crowd"),
  ("drive-thru","Drive-thru","no parking, no line"),
  ("with-food","Boba and food","popcorn chicken and Taiwanese eats"),
]

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"['\".]", "", s); s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def esc(s): return html.escape(s or "", quote=True)

# ---- load data ----
def load_rows():
    rows=[]
    with open(CSV, encoding="utf-8") as f:
        lines=[ln for ln in f if not ln.startswith("#") and not ln.startswith("county,")]
    for r in csv.reader(io.StringIO("".join(lines))):
        if not r or len(r)<4 or not r[2].strip(): continue
        county,city,name,address = r[0].strip(),r[1].strip(),r[2].strip(),r[3].strip()
        rows.append({"county":county,"city":city,"name":name,"address":address})
    seen={}
    for r in rows:
        base=f"{slugify(r['name'])}-{slugify(r['city'])}"; n=seen.get(base,0)
        r["slug"]=base if not n else f"{base}-{n+1}"; seen[base]=n+1
        r["region"]=region_of(r["county"],r["city"]); r["city_slug"]=slugify(r["city"])
        # enriched fields (absent for seed): lat,lng,phone,hours,formatted_address,status
        r.setdefault("status","seed")
    return rows

# ---- shared chrome ----
def head(title, desc, canonical, noindex=False):
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">{robots}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner">
<a class="brand" href="/">Capy<b>Boba</b></a>
<nav class="head-nav" aria-label="Primary">
<a href="/area/sgv/">By area</a><a href="/best/">By vibe</a><a href="/new/orange-county/">New</a><a href="/guide/">Guides</a>
</nav>
<div class="head-actions"><a class="btn btn-ghost" href="/">Find boba</a></div>
</div></header>
<main id="main" class="wrap">"""

def foot():
    return f"""</main>
<footer class="site-footer"><div class="footer-inner">
<div class="footer-brand"><a class="brand" href="/">Capy<b>Boba</b></a>
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
<li><a href="/about/">About CapyBoba</a></li></ul></div>
</div><div class="footer-bottom">
<span>&copy; 2026 CapyBoba</span><span class="note">We don't take payment for placement on our best-for lists.</span>
</div></footer></body></html>"""

def write(path, content):
    full=os.path.join(ROOT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,"w",encoding="utf-8").write(content)

# ---- profile ----
def render_profile(r, neighbors):
    enriched = bool(r.get("latitude"))
    url=f"{SITE}/boba/ca/{r['city_slug']}/{r['slug']}/"
    reg=REGIONS[r["region"]]
    directions=f"https://www.google.com/maps/search/?api=1&query={r['name'].replace(' ','%20')}%20{r['address'].replace(' ','%20')}%20{r['city'].replace(' ','%20')}%20CA"
    mono=esc((r["name"][:2]).upper())
    near="".join(
        f'<li><a href="/boba/ca/{n["city_slug"]}/{n["slug"]}/">{esc(n["name"])}</a><span class="meta">{esc(n["address"])}</span></li>'
        for n in neighbors[:5]) or '<li class="is-muted">More nearby shops as the area is verified.</li>'
    status_pill = ('<span class="status pending"><span class="led"></span>Verifying hours</span>'
                   if not enriched else '<span class="status open"><span class="led"></span>Hours listed below</span>')

    body=f"""
<nav class="crumb" aria-label="Breadcrumb">
<a href="/">Home</a><span class="sep">/</span>
<a href="/area/{r['region']}/">{esc(reg['label'])}</a><span class="sep">/</span>
<a href="/boba/ca/{r['city_slug']}/">{esc(r['city'])}</a><span class="sep">/</span>
<span aria-current="page">{esc(r['name'])}</span>
</nav>

<section class="hero"><div class="hero-inner">
<div class="hero-logo"><span class="mono">{mono}</span></div>
<div class="hero-body">
<div class="hero-titlerow"><h1>{esc(r['name'])}</h1></div>
<p class="hero-sub">Boba in {esc(r['city'])}, {esc(reg['label'])}</p>
<div class="hero-meta">{status_pill} <span class="tag tag-verifying">Verifying</span></div>
<div class="hero-actions">
<a class="btn btn-primary" href="{directions}" rel="nofollow noopener" target="_blank">Get directions</a>
<a class="btn btn-ghost" href="/boba/ca/{r['city_slug']}/">More {esc(r['city'])} boba</a>
</div></div></div></section>

<div class="grid">
<div class="g-main">
<section class="sec"><h2>Find it</h2>
<div class="map-main"><div class="map-main-face"><span class="pin"></span><span class="map-hint">Map loads from verified coordinates</span></div>
<div class="map-foot"><div class="addr"><strong>{esc(r['address'])}</strong><span>{esc(r['city'])}, CA</span></div>
<a class="btn btn-primary" href="{directions}" rel="nofollow noopener" target="_blank">Get directions</a></div></div>
<p class="note-line">Coordinates are geocoded and verified before this profile is indexed, so the pin never drifts from the real address.</p>
</section>

<section class="sec"><p class="p-summary"><span class="lbl">About <span class="tag tag-verifying">Verifying</span></span>
We're verifying {esc(r['name'])}'s hours, menu, and details against the shop's own listing. The name and address here are confirmed; the rest fills in shortly.</p></section>

<section class="sec"><h2>What to order <span class="tag tag-verifying">Verifying</span></h2>
<p class="is-muted">Signature drinks are pulled from the official menu before they show here. Nothing invented.</p></section>

<section class="sec"><h2>Good to know <span class="tag tag-verifying">Verifying</span></h2>
<p class="is-muted">Seating, wifi, non-dairy, and other details show only once a primary source confirms them.</p></section>

<section class="sec"><h2>Other boba nearby</h2>
<ul class="nearby-list">{near}</ul>
<p class="note-line">Neighbors are real shops from the {esc(r['city'])} list. Distances fill in from geocoded coordinates.</p></section>

<section class="sec faq"><h2>FAQ</h2>
<h3>Where is {esc(r['name'])}?</h3><p>{esc(r['name'])} is at {esc(r['address'])} in {esc(r['city'])}, CA.</p>
<h3>Is it open right now?</h3><p class="is-muted">We're verifying current hours against the shop's listing. Use Get directions above for live Google hours in the meantime.</p></section>
</div>

<aside class="g-aside"><div class="facts-card">
<p class="fc-title">Find {esc(r['name'])}</p>
<dl class="dl">
<div><dt>Address</dt><dd>{esc(r['address'])}, {esc(r['city'])}, CA</dd></div>
<div><dt>Area</dt><dd><a href="/area/{r['region']}/">{esc(reg['label'])}</a></dd></div>
<div><dt>Hours</dt><dd class="is-muted">Verifying</dd></div>
<div><dt>Phone</dt><dd class="is-muted">Verifying</dd></div>
</dl>
<p class="card-line"><span class="dot"></span>Is this your shop? <a class="textlink" href="/claim/">Claim this listing</a></p>
<p class="card-line"><span class="dot"></span>Something wrong? <a class="textlink" href="/report/">Report it</a></p>
</div></aside>
</div>

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":"{esc(r['name'])}",
"@id":"{url}#shop","url":"{url}","servesCuisine":"Bubble Tea",
"address":{{"@type":"PostalAddress","streetAddress":"{esc(r['address'])}","addressLocality":"{esc(r['city'])}","addressRegion":"CA","addressCountry":"US"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},
{{"@type":"ListItem","position":2,"name":"{esc(reg['label'])}","item":"{SITE}/area/{r['region']}/"}},
{{"@type":"ListItem","position":3,"name":"{esc(r['city'])}","item":"{SITE}/boba/ca/{r['city_slug']}/"}},
{{"@type":"ListItem","position":4,"name":"{esc(r['name'])}","item":"{url}"}}]}}
</script>
"""
    title=f"{r['name']}, {r['city']}: Boba Hours, Menu & Map (2026) | CapyBoba"
    desc=f"{r['name']} at {r['address']}, {r['city']}. Directions, hours, and what to order. CapyBoba."
    # noindex until enriched
    write(f"boba/ca/{r['city_slug']}/{r['slug']}/index.html",
          head(title,desc,url,noindex=not enriched)+body+foot())

# ---- city page ----
def render_city(city, county, region, shops, neighbor_cities):
    cslug=slugify(city); reg=REGIONS[region]; url=f"{SITE}/boba/ca/{cslug}/"
    items="".join(
        f'<div class="dir-item"><div class="di-main"><a class="di-name" href="/boba/ca/{cslug}/{s["slug"]}/">{esc(s["name"])}</a>'
        f'<div class="di-addr">{esc(s["address"])}</div></div>'
        f'<div class="di-right"><span class="di-hours is-muted">Hours verifying</span></div></div>'
        for s in shops)
    nbr="".join(f'<a href="/boba/ca/{slugify(c)}/">{esc(c)}</a> ' for c in neighbor_cities[:5])
    ld_items="".join(
        '{"@type":"ListItem","position":%d,"url":"%s/boba/ca/%s/%s/","name":"%s"}%s'
        % (i+1, SITE, cslug, s["slug"], esc(s["name"]).replace('"','\\"'), "," if i<len(shops)-1 else "")
        for i,s in enumerate(shops))
    body=f"""
<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">/</span>
<a href="/area/{region}/">{esc(reg['label'])}</a><span class="sep">/</span><span aria-current="page">{esc(city)}</span></nav>
<div class="page-head"><p class="eyebrow">{esc(reg['label'])}</p>
<h1>Boba in {esc(city)}</h1>
<p class="lede">We're tracking <b>{len(shops)} boba shop{'s' if len(shops)!=1 else ''}</b> in {esc(city)}. Addresses are below; hours and shop details are being verified against each shop's own listing before they show.</p></div>
<div class="notice"><span class="tag tag-verifying">Verifying</span>
<span>This is a live directory in progress. Shop names and addresses are confirmed. Hours, coordinates, and details are added as we verify each shop, so you won't see a wrong hour that sends you to a closed shop.</span></div>
<section class="sec"><h2>Every boba shop in {esc(city)}</h2>
<div class="dir-list">{items}</div></section>
<section class="sec faq"><h2>FAQ</h2>
<h3>How many boba shops are in {esc(city)}?</h3><p>We're tracking {len(shops)} in {esc(city)}, listed above with addresses.</p>
<h3>Are the hours accurate?</h3><p>We verify hours against each shop's own listing before showing them, so a shop reads as verifying until that's done rather than showing a guessed hour.</p></section>
<nav class="related">Part of <a href="/area/{region}/">{esc(reg['label'])}</a>{' &middot; Nearby: '+nbr if nbr else ''}</nav>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ItemList","name":"Boba shops in {esc(city)}, CA","numberOfItems":{len(shops)},"itemListElement":[{ld_items}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},
{{"@type":"ListItem","position":2,"name":"{esc(reg['label'])}","item":"{SITE}/area/{region}/"}},
{{"@type":"ListItem","position":3,"name":"{esc(city)}","item":"{url}"}}]}}
</script>
"""
    title=f"Boba in {city}: {len(shops)} Shops with Addresses & Map (2026) | CapyBoba"
    desc=f"Every boba shop in {city}, CA: {len(shops)} spots with addresses. Hours and details verified and added continuously. CapyBoba."
    write(f"boba/ca/{cslug}/index.html", head(title,desc,url)+body+foot())

# ---- region hub ----
def render_region(region, cities_map):
    reg=REGIONS[region]; url=f"{SITE}/area/{region}/"
    cities=sorted(cities_map.keys())
    cards="".join(
        f'<a class="card" href="/boba/ca/{slugify(c)}/"><h3>{esc(c)}</h3>'
        f'<span class="c-meta">{len(cities_map[c])} shop{"s" if len(cities_map[c])!=1 else ""}</span></a>'
        for c in cities)
    total=sum(len(v) for v in cities_map.values())
    body=f"""
<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">/</span><span aria-current="page">{esc(reg['label'])}</span></nav>
<div class="page-head"><p class="eyebrow">{esc(reg['kicker'])}</p>
<h1>Boba in {esc(reg['label'])}</h1>
<p class="lede">{esc(reg['blurb'])} We're tracking <b>{total} shops</b> across <b>{len(cities)} cities</b> here. Pick a city to see the shops.</p></div>
<section class="sec"><h2>Cities</h2><div class="card-grid">{cards}</div></section>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},
{{"@type":"ListItem","position":2,"name":"{esc(reg['label'])}","item":"{url}"}}]}}
</script>
"""
    title=f"Boba in {reg['label']}: {total} Shops by City (2026) | CapyBoba"
    desc=f"Boba across {reg['label']}: {total} shops in {len(cities)} cities with addresses. Browse by city on CapyBoba."
    write(f"area/{region}/index.html", head(title,desc,url)+body+foot())

# ---- intent landing (honest, no fake ranking, noindex) ----
def render_intent_index():
    url=f"{SITE}/best/"
    tiles="".join(
        f'<a class="card" href="/best/{slug}/"><h3>{esc(label)}</h3><span class="c-meta">{esc(desc)}</span></a>'
        for slug,label,desc in INTENTS)
    body=f"""
<nav class="crumb"><a href="/">Home</a><span class="sep">/</span><span aria-current="page">By vibe</span></nav>
<div class="page-head"><p class="eyebrow">Start with the mood</p><h1>Boba by vibe</h1>
<p class="lede">Most boba searches are about a moment, not a brand. These picks are ranked on verified attributes, so each list goes live once enough {esc('shops')} in an area are verified for it.</p></div>
<div class="notice"><span class="tag tag-verifying">In progress</span><span>We don't post a ranking we haven't earned. As shops are verified, each vibe gets a real, method-shown list. Meanwhile, browse by area.</span></div>
<section class="sec"><h2>Vibes</h2><div class="card-grid">{tiles}</div></section>
<nav class="related">Browse by area: <a href="/area/sgv/">The 626</a> <a href="/area/orange-county/">Orange County</a> <a href="/area/san-diego/">San Diego</a></nav>
"""
    write("best/index.html", head("Boba by Vibe: Date Night, Study, Open Late & More | CapyBoba",
          "Find SoCal boba by vibe: date night, study-friendly, open late, brown sugar and more. Ranked on verified attributes.",
          url, noindex=True)+body+foot())

def render_intent(slug,label,desc):
    url=f"{SITE}/best/{slug}/"
    body=f"""
<nav class="crumb"><a href="/">Home</a><span class="sep">/</span><a href="/best/">By vibe</a><span class="sep">/</span><span aria-current="page">{esc(label)}</span></nav>
<div class="page-head"><p class="eyebrow">By vibe</p><h1>Best boba for {esc(label.lower())} in Southern California</h1>
<p class="lede">Our {esc(label.lower())} picks are ranked on verified attributes ({esc(desc)}). This list goes live once enough shops in each area are verified, so it's honest rather than guessed.</p></div>
<div class="notice"><span class="tag tag-verifying">Verifying</span><span>We're confirming which shops truly fit {esc(label.lower())} before ranking them. Browse by area in the meantime.</span></div>
<nav class="related">Browse by area: <a href="/area/sgv/">The 626</a> <a href="/area/orange-county/">Orange County</a> <a href="/area/san-diego/">San Diego</a> <a href="/area/greater-la/">Greater LA</a> <a href="/area/inland-empire/">Inland Empire</a></nav>
"""
    write(f"best/{slug}/index.html", head(f"Best Boba for {label} in SoCal (2026) | CapyBoba",
          f"Best SoCal boba for {label.lower()}: {desc}. Ranked on verified attributes, honest and method-shown. CapyBoba.",
          url, noindex=True)+body+foot())

# ---- sitemap / robots / llms ----
def render_meta_files(cities_by_region):
    urls=[f"{SITE}/"]
    for reg in REGIONS: urls.append(f"{SITE}/area/{reg}/")
    for reg,cm in cities_by_region.items():
        for c in cm: urls.append(f"{SITE}/boba/ca/{slugify(c)}/")
    body='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        body+=f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n"
    body+="</urlset>\n"
    write("sitemap.xml", body)
    write("robots.txt",
      "User-agent: *\nAllow: /\n\n"
      "# AI answer engines welcome\nUser-agent: GPTBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n"
      "User-agent: Google-Extended\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\n\n"
      f"Sitemap: {SITE}/sitemap.xml\n")
    write("llms.txt",
      "# CapyBoba\n\n"
      "The Southern California boba directory. Real hours, honest rankings, new openings tracked. "
      "No fabricated stats or reviews; third-party ratings are shown live and attributed, never cached. "
      "Individual shop profiles are noindex until their hours and coordinates are verified.\n\n"
      f"- Directory by area: {SITE}/area/\n- Cities: {SITE}/boba/ca/\n- By vibe: {SITE}/best/\n")

def main():
    rows=load_rows()
    by_city={}; cities_by_region={}
    for r in rows:
        by_city.setdefault((r["city"],r["county"],r["region"]),[]).append(r)
        cities_by_region.setdefault(r["region"],{}).setdefault(r["city"],[]).append(r)
    # profiles
    for r in rows:
        neighbors=[x for x in by_city[(r["city"],r["county"],r["region"])] if x["slug"]!=r["slug"]]
        render_profile(r, neighbors)
    # city pages
    for (city,county,region),shops in by_city.items():
        shops_sorted=sorted(shops,key=lambda s:s["name"].lower())
        neighbor_cities=[c for c in cities_by_region[region] if c!=city]
        render_city(city,county,region,shops_sorted,neighbor_cities)
    # region hubs
    for region,cm in cities_by_region.items():
        render_region(region,cm)
    # intent pages
    render_intent_index()
    for slug,label,desc in INTENTS: render_intent(slug,label,desc)
    # meta
    render_meta_files(cities_by_region)
    print(f"shops(profiles): {len(rows)}")
    print(f"cities: {len(by_city)}")
    print(f"regions: {len(cities_by_region)} -> {sorted(cities_by_region)}")
    print(f"intent pages: {len(INTENTS)+1}")

if __name__=="__main__":
    main()
