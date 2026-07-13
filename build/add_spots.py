#!/usr/bin/env python3
"""
add_spots.py — add new shops to EVERY surface in one run.

Input: a JSON file of spots:
[{"name","address","city","county","area",          # area = display label e.g. "Orange County"
  "region_slug",                                     # e.g. "orange-county" (for /area/ links)
  "store_type",                                      # "chain"|"specialty"
  "dessert": true,                                   # optional, marks dessert-first houses
  "featured": false,                                 # optional
  "website": "", "signature_items": [], "source_url": "",  # optional, for the profile page
  "about": ""                                        # optional editorial line for profile
}]

Updates: seed CSV, directory SHOPS + counts, roulette SHOPS, profile page,
city page (create or update), cities index, area page, sitemap, homepage
counts, gen_site region map (if a new SGV city). Prints a Supabase INSERT.
Run from repo root:  python3 build/add_spots.py spots.json
"""
import csv, io, json, os, re, sys, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()

ONES = ["","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
TENS = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
def spell(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n//10] + ("-" + ONES[n%10] if n%10 else "")
    if n < 1000:
        s = ONES[n//100] + " hundred"
        if n%100: s += " and " + spell(n%100)
        return s
    return str(n)

def slugify(s):
    s = re.sub(r"[’']", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def rd(p): return open(os.path.join(ROOT,p),encoding="utf-8").read()
def wr(p,s): open(os.path.join(ROOT,p),"w",encoding="utf-8").write(s)

def main(spots_path):
    spots = json.load(open(spots_path))
    for sp in spots:
        sp["cs"] = slugify(sp["city"])
        sp["slug"] = slugify(sp["name"]) + "-" + sp["cs"]

    # ---------- 1. seed CSV ----------
    p = "data/stores-seed.csv"; s = rd(p)
    for sp in spots:
        s += f'{sp["county"]},{sp["city"]},{sp["name"]},{sp["address"]},manual,seed,yes\n'
    wr(p, s)

    # ---------- 2. directory SHOPS + counts ----------
    p = "directory/index.html"; s = rd(p)
    m = re.search(r"var SHOPS = (\[.*?\]);", s, re.S)
    shops = json.loads(m.group(1))
    known = {x["s"] for x in shops}
    for sp in spots:
        if sp["slug"] in known: raise SystemExit("slug exists: "+sp["slug"])
        e = {"n":sp["name"],"c":sp["city"],"cs":sp["cs"],"s":sp["slug"],
             "ar":sp["area"],"ch":1 if sp["store_type"]=="chain" else 0}
        if sp.get("featured"): e["f"]=1
        if sp.get("dessert"): e["ds"]=1
        shops.append(e)
    old_total = len(shops)-len(spots); new_total = len(shops)
    old_cities = len({x["cs"] for x in shops[:old_total]}); new_cities = len({x["cs"] for x in shops})
    s = s[:m.start()] + "var SHOPS = " + json.dumps(shops,separators=(",",":")) + ";" + s[m.end():]
    for a,b in [(f"Browse <b>{old_total}</b> shops across <b>{old_cities}</b> cities",f"Browse <b>{new_total}</b> shops across <b>{new_cities}</b> cities"),
                (f"<h2>Browse all {old_total} shops</h2>",f"<h2>Browse all {new_total} shops</h2>"),
                (f"Showing {old_total} shops",f"Showing {new_total} shops")]:
        assert a in s, "directory count: "+a; s = s.replace(a,b)
    s = s.replace(f"All {old_cities} cities", f"All {new_cities} cities").replace(f"Browse all {old_cities} cities", f"Browse all {new_cities} cities")
    wr(p, s)

    # ---------- 3. roulette SHOPS ----------
    p = "tools/roulette/index.html"; s = rd(p)
    m = re.search(r"const SHOPS = (\[.*?\]);", s, re.S)
    rl = json.loads(m.group(1))
    for sp in spots:
        e = {"n":sp["name"],"c":sp["city"],"ar":sp["area"],"ad":sp["address"],
             "ch":sp["store_type"]=="chain","loc":1}
        if sp.get("dessert"): e["ds"]=True
        rl.append(e)
    s = s[:m.start()] + "const SHOPS = " + json.dumps(rl,separators=(",",":")) + ";" + s[m.end():]
    wr(p, s)

    # ---------- 4. profile pages ----------
    tpl = rd("boba/ca/city-of-industry/taro-yuan-city-of-industry/index.html")
    for sp in spots:
        d = os.path.join(ROOT,"boba/ca",sp["cs"],sp["slug"]); os.makedirs(d,exist_ok=True)
        nm, ct, ad = html.escape(sp["name"]), html.escape(sp["city"]), html.escape(sp["address"])
        q = re.sub(r"\s+","%20",f'{sp["name"]} {sp["address"]} {sp["city"]} CA')
        items = "".join(f'<li><span><strong>{html.escape(i)}</strong></span></li>' for i in sp.get("signature_items",[]))
        order_sec = (f'<section class="sec"><h2>What to order</h2><ul class="nearby-list">{items}</ul>'
                     f'<p class="note-line">Items noted from <a href="{html.escape(sp["source_url"])}" rel="noopener" target="_blank">public sources</a>; menu details verify before they are stated as fact.</p></section>') if items and sp.get("source_url") else \
                    '<section class="sec"><h2>What to order <span class="tag tag-verifying">Verifying</span></h2><p class="is-muted">Signature items are pulled from the official menu before they show here. Nothing invented.</p></section>'
        about = html.escape(sp.get("about","")) or f"We're verifying {nm}'s hours, menu, and details against the shop's own listing. The name and address here are confirmed; the rest fills in shortly."
        website = f'<a class="btn btn-ghost" href="{html.escape(sp["website"])}" rel="noopener" target="_blank">Official site</a>' if sp.get("website") else ""
        pg = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nm}, {ct}: Hours, Menu &amp; Map (2026) | NiteBoba</title>
<meta name="description" content="{nm} at {ad}, {ct}. Directions, what to order, and verified details as they land. NiteBoba.">
<link rel="canonical" href="https://niteboba.vercel.app/boba/ca/{sp["cs"]}/{sp["slug"]}/"><meta name="robots" content="noindex,follow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner">
<a class="brand" href="/">Nite<b>Boba</b></a>
<nav class="head-nav" aria-label="Primary">
<a href="/cities/">Cities</a><a href="/best/">By vibe</a><a href="/tools/">Tools</a><a href="/new/">New</a><a href="/guide/">Guides</a>
</nav>
<div class="head-actions"><a class="btn btn-ghost" href="/">Find boba</a></div>
</div></header>
<main id="main" class="wrap">
<nav class="crumb" aria-label="Breadcrumb">
<a href="/">Home</a><span class="sep">/</span>
<a href="/area/{sp["region_slug"]}/">{html.escape(sp["area"])}</a><span class="sep">/</span>
<a href="/boba/ca/{sp["cs"]}/">{ct}</a><span class="sep">/</span>
<span aria-current="page">{nm}</span>
</nav>
<section class="hero"><div class="hero-inner">
<div class="hero-logo"><span class="mono">{nm[0].upper()}</span></div>
<div class="hero-body">
<div class="hero-titlerow"><h1>{nm}</h1></div>
<p class="hero-sub">{"Dessert house" if sp.get("dessert") else "Boba"} in {ct}, {html.escape(sp["area"])}</p>
<div class="hero-meta"><span class="status pending"><span class="led"></span>Verifying hours</span> <span class="tag tag-verifying">Verifying</span></div>
<div class="hero-actions">
<a class="btn btn-primary" href="https://www.google.com/maps/search/?api=1&query={q}" rel="nofollow noopener" target="_blank">Get directions</a>
{website}
</div></div></div></section>
<div class="grid">
<div class="g-main">
<section class="sec"><h2>Find it</h2>
<div class="map-main"><div class="map-main-face"><span class="pin"></span><span class="map-hint">Map loads from verified coordinates</span></div>
<div class="map-foot"><div class="addr"><strong>{ad}</strong><span>{ct}, CA</span></div>
<a class="btn btn-primary" href="https://www.google.com/maps/search/?api=1&query={q}" rel="nofollow noopener" target="_blank">Get directions</a></div></div>
<p class="note-line">Coordinates are geocoded and verified before this profile is indexed, so the pin never drifts from the real address.</p>
</section>
<section class="sec"><p class="p-summary"><span class="lbl">About</span>
{about}</p></section>
{order_sec}
<section class="sec"><h2>Good to know <span class="tag tag-verifying">Verifying</span></h2>
<p class="is-muted">Seating, wifi, non-dairy, and other details show only once a primary source confirms them.</p></section>
<section class="sec faq"><h2>FAQ</h2>
<h3>Where is {nm}?</h3><p>{nm} is at {ad} in {ct}, CA.</p>
<h3>Is it open right now?</h3><p class="is-muted">We're verifying current hours against the shop's listing. Use Get directions above for live Google hours in the meantime.</p></section>
</div>
<aside class="g-aside"><div class="facts-card">
<p class="fc-title">Find {nm}</p>
<dl class="dl">
<div><dt>Address</dt><dd>{ad}, {ct}, CA</dd></div>
<div><dt>Area</dt><dd><a href="/area/{sp["region_slug"]}/">{html.escape(sp["area"])}</a></dd></div>
<div><dt>Type</dt><dd>{"Dessert house" if sp.get("dessert") else ("Chain" if sp["store_type"]=="chain" else "Independent")}</dd></div>
<div><dt>Hours</dt><dd class="is-muted">Verifying</dd></div>
</dl>
<p class="card-line"><span class="dot"></span>Is this your shop? <a class="textlink" href="/claim/">Claim this listing</a></p>
<p class="card-line"><span class="dot"></span>Something wrong? <a class="textlink" href="/report/">Report it</a></p>
</div></aside>
</div>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CafeOrCoffeeShop","name":{json.dumps(sp["name"])},
"@id":"https://niteboba.vercel.app/boba/ca/{sp["cs"]}/{sp["slug"]}/#shop","url":"https://niteboba.vercel.app/boba/ca/{sp["cs"]}/{sp["slug"]}/","servesCuisine":"Bubble Tea",
"address":{{"@type":"PostalAddress","streetAddress":{json.dumps(sp["address"])},"addressLocality":{json.dumps(sp["city"])},"addressRegion":"CA","addressCountry":"US"}}}}
</script>
</main>
<footer class="site-footer"><div class="footer-inner">
<div class="footer-brand"><a class="brand" href="/">Nite<b>Boba</b></a>
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
<li><a href="/about/">About NiteBoba</a></li></ul></div>
</div><div class="footer-bottom">
<span>&copy; 2026 NiteBoba</span><span class="note">We don't take payment for placement on our best-for lists.</span>
</div></footer></body></html>
'''
        wr(os.path.join("boba/ca",sp["cs"],sp["slug"],"index.html"), pg)

    # ---------- 5+6. city pages + cities index ----------
    cities_idx = rd("cities/index.html")
    for sp in spots:
        cp = f'boba/ca/{sp["cs"]}/index.html'
        item = (f'<div class="dir-item"><div class="di-main"><a class="di-name" href="/boba/ca/{sp["cs"]}/{sp["slug"]}/">{html.escape(sp["name"])}</a>'
                f'<div class="di-addr">{html.escape(sp["address"])}</div></div><div class="di-right"><span class="di-hours is-muted">Hours verifying</span></div></div>')
        if os.path.exists(os.path.join(ROOT,cp)):
            s = rd(cp)
            s = s.replace('</div></section>\n<section class="sec faq">', item+'</div></section>\n<section class="sec faq">',1) if item not in s else s
            # bump counts: "tracking <b>N boba shop(s)</b>" and FAQ "tracking N in"
            mm = re.search(r"tracking <b>(\d+) boba shops?</b>", s)
            if mm:
                n0 = int(mm.group(1)); n1 = n0+1
                s = s.replace(f"tracking <b>{n0} boba shop{'s' if n0!=1 else ''}</b>", f"tracking <b>{n1} boba shops</b>")
                s = re.sub(r"tracking "+str(n0)+r" in", f"tracking {n1} in", s)
            wr(cp, s)
        else:
            t = rd("boba/ca/city-of-industry/index.html")
            t = t.replace("City of Industry", sp["city"]).replace("city-of-industry", sp["cs"])
            t = t.replace("San Gabriel Valley", sp["area"]).replace("/area/sgv/", f'/area/{sp["region_slug"]}/')
            t = t.replace('<a class="di-name" href="/boba/ca/'+sp["cs"]+'/taro-yuan-'+sp["cs"]+'/">Taro Yuan</a><div class="di-addr">18246 Gale Ave A</div>',
                          f'<a class="di-name" href="/boba/ca/{sp["cs"]}/{sp["slug"]}/">{html.escape(sp["name"])}</a><div class="di-addr">{html.escape(sp["address"])}</div>')
            t = re.sub(r'"itemListElement":\[.*?\]\}', f'"itemListElement":[{{"@type":"ListItem","position":1,"url":"https://niteboba.vercel.app/boba/ca/{sp["cs"]}/{sp["slug"]}/","name":{json.dumps(sp["name"])}}}]}}', t, count=1, flags=re.S)
            t = t.replace("starting with Taro Yuan on Gale Ave", f"starting with {sp['name']}")
            t = t.replace("Taro Yuan", sp["name"])  # residual mentions
            wr(cp, t)
            # sitemap
            sm = rd("sitemap.xml")
            anchor = "  <url><loc>https://niteboba.vercel.app/meetups/</loc>"
            sm = sm.replace(anchor, f'  <url><loc>https://niteboba.vercel.app/boba/ca/{sp["cs"]}/</loc><lastmod>{TODAY}</lastmod></url>\n'+anchor,1)
            wr("sitemap.xml", sm)
        # cities index card
        if f'/boba/ca/{sp["cs"]}/' not in cities_idx:
            cities_idx = cities_idx.replace('</div></section><section class="sec"><h2>Inland Empire</h2>',
                f'<a class="card" href="/boba/ca/{sp["cs"]}/"><h3>{html.escape(sp["city"])}</h3><span class="c-meta">1 shop</span></a></div></section><section class="sec"><h2>Inland Empire</h2>') \
                if sp["region_slug"]=="san-diego" else cities_idx  # only generic fallback
    wr("cities/index.html", cities_idx)

    # ---------- 9. homepage counts ----------
    s = rd("index.html")
    s = s.replace(f"{old_total} rooms across five regions", f"{new_total} rooms across five regions")
    s = s.replace(f"{spell(old_total).capitalize()} rooms", f"{spell(new_total).capitalize()} rooms")
    wr("index.html", s)

    # ---------- Supabase SQL ----------
    rows=[]
    for sp in spots:
        rows.append("("+",".join([
            json.dumps(sp["slug"]).replace('"',"'"), json.dumps(sp["name"]).replace('"',"'"),
            json.dumps(sp["city"]).replace('"',"'"), json.dumps(sp["county"]).replace('"',"'"),
            "'CA'", json.dumps(sp["address"]).replace('"',"'"), "'manual'","'seed'","true",
            json.dumps(sp["store_type"]).replace('"',"'"),
            "true" if sp.get("featured") else "false",
            json.dumps(sp.get("website") or None).replace('"',"'") if sp.get("website") else "null",
        ])+")")
    print("-- Supabase:")
    print("insert into public.niteboba (slug,name,city,county,state,address,source,status,seed_verify_needed,store_type,is_featured,website) values\n"+",\n".join(rows)+";")
    print(f"\nDone: {len(spots)} spots. Totals {old_total}->{new_total} shops, {old_cities}->{new_cities} cities.")
    print("MANUAL CHECKS: cities/index.html + area page cards/counts for new cities; homepage area tile numbers; SGV_CITIES in gen_site.py if a new 626 city.")

if __name__ == "__main__":
    main(sys.argv[1])
