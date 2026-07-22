#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boba Night - surgical order-rail patcher.

Replaces ONLY the order-rail block (between <!-- TPL:order-rail --> and
<!-- /TPL:order-rail -->) in every profile page under boba/**/index.html, and
appends the matching rail styles to css/profile-v4.css (idempotent). Does NOT
regenerate whole pages, touch nav counts, or create new pages.

New rail: name + Google rating + review count + full address on the left;
three equal buttons on the right - Uber Eats (location deep-link), DoorDash,
Toast - plus Directions. Toast renders full-color/clickable only where
build/toast_links.json marks the shop verified; otherwise greyed + disabled.

Run on the Mac (needs Supabase network), from the repo root:
    python3 build/patch_order_rail.py --dry-run
    python3 build/patch_order_rail.py --slug share-tea-san-gabriel
    python3 build/patch_order_rail.py
Cloud test: NBSAMPLE=<rows.json> --root <tmp repo>
"""
import base64, json, os, re, sys, urllib.parse, urllib.request

SB  = "https://hfvbeqlefwwjlrbyxpbj.supabase.co"
KEY = "sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf"
COLS = ("slug,name,city,address,zip,latitude,longitude,"
        "google_rating,google_review_count,price_level")

def q(s):  return urllib.parse.quote("" if s is None else str(s), safe="")
def a(u):  return u.replace("&", "&amp;")

def fetch_rows():
    s = os.environ.get("NBSAMPLE")
    if s: return json.load(open(s, encoding="utf-8"))
    rows, page = [], 0
    while True:
        url = (SB + "/rest/v1/niteboba?select=" + COLS +
               "&status=eq.open&limit=1000&offset=%d" % (page*1000))
        req = urllib.request.Request(url, headers={
            "apikey": KEY, "Authorization": "Bearer " + KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            batch = json.load(r)
        rows.extend(batch)
        if len(batch) < 1000: break
        page += 1
    return rows

def fnum(v):
    try: return float(v)
    except (TypeError, ValueError): return None

# ---- SVG art (matches approved v6 preview) ----
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

def esc_html(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
             .replace('"',"&quot;"))

def build_rail(row, toast):
    name = row["name"]; E = esc_html(name)
    street = ((row.get("address") or "").split(",")[0]).strip()
    city = row.get("city") or ""
    zipc = (row.get("zip") or "").strip() if row.get("zip") else ""
    lat = fnum(row.get("latitude")); lng = fnum(row.get("longitude"))
    full = street + (", " + city if city else "") + ", CA" + (" " + zipc if zipc else "")
    # Uber Eats location deep-link
    if lat is not None and lng is not None:
        pl = {"address": full, "latitude": lat, "longitude": lng,
              "reference": "", "referenceType": "google_places"}
        enc = base64.b64encode(urllib.parse.quote(
            json.dumps(pl, separators=(',', ':'))).encode()).decode()
        ue = "https://www.ubereats.com/search?diningMode=DELIVERY&q=" + q(name) + "&pl=" + enc
    else:
        ue = "https://www.ubereats.com/search?q=" + q(name)
    dd = "https://www.doordash.com/search/store/" + q(name) + "/"
    dirn = ("https://www.google.com/maps/search/?api=1&query=" +
            q(name + " " + street + " " + city + " CA"))
    # rating + reviews meta
    rating = row.get("google_rating"); reviews = row.get("google_review_count")
    bits = []
    if rating not in (None, "", "0"):
        bits.append('<span class="od-rail-star">&#9733; %s</span>' % esc_html(str(rating)))
    if reviews not in (None, "", 0, "0"):
        bits.append('<span class="od-rail-rev">%s reviews</span>' % ("{:,}".format(int(reviews))))
    if full:
        bits.append('<span class="od-rail-dot">&middot;</span>%s' % esc_html(full))
    meta = "".join(bits)
    # Toast: verified -> active <a>, else greyed <span>
    tinfo = toast.get(row["slug"]) if toast else None
    if tinfo and tinfo.get("toast_url") and tinfo.get("confidence") in ("high", "review"):
        toast_btn = ('<a class="od-svc od-svc--to" href="%s" target="_blank" rel="nofollow sponsored noopener">%s<span class="od-n">Toast</span></a>'
                     % (a(tinfo["toast_url"]), TO_ART))
    else:
        toast_btn = ('<span class="od-svc od-svc--to is-off" aria-disabled="true" title="Not available on Toast">%s<span class="od-n">Toast</span></span>'
                     % TO_ART)
    return ('<!-- TPL:order-rail -->\n'
     '<nav class="od-rail" aria-label="Order %s to go">\n'
     '  <span class="od-rail-lead">%s'
     '<span class="od-rail-info"><b class="od-rail-name">%s</b>'
     '<span class="od-rail-meta">%s</span></span></span>\n'
     '  <div class="od-rail-acts">\n'
     '    <a class="od-svc od-svc--ue" href="%s" target="_blank" rel="nofollow sponsored noopener">%s<span class="od-n">Uber&nbsp;Eats</span></a>\n'
     '    <a class="od-svc od-svc--dd" href="%s" target="_blank" rel="nofollow sponsored noopener">%s<span class="od-n">DoorDash</span></a>\n'
     '    %s\n'
     '    <a class="od-dir" href="%s" rel="nofollow noopener" target="_blank">%s<span>Directions</span></a>\n'
     '  </div>\n</nav>\n'
     '<p class="od-rail-note">Delivery and pickup by Uber Eats, DoorDash, or Toast. Menus and prices set by the service.</p>\n'
     '<!-- /TPL:order-rail -->'
     % (E, LEAD_CUP, E, meta, a(ue), UE_ART, a(dd), DD_ART, toast_btn, a(dirn), DIR_ART))

RAIL_CSS = """
/* ===== order-rail v3: info block + 3 equal services (patch_order_rail.py) ===== */
.od-rail{gap:.9rem}
.od-rail-lead{flex:1 1 auto;min-width:0;align-items:center}
.od-rail-info{display:flex;flex-direction:column;min-width:0;line-height:1.28}
.od-rail-name{color:var(--porcelain,#F4EFE7);font:600 1rem "Inter Tight",sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.od-rail-meta{color:var(--muted,#a89f92);font-size:.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:.4rem;flex-wrap:wrap}
.od-rail-star{color:var(--champagne,#C5A46D);font-weight:600}
.od-rail-rev{color:var(--muted,#a89f92)}
.od-rail-rev::before{content:"\\00b7";margin-right:.4rem;opacity:.6}
.od-rail-dot{opacity:.6}
.od-svc--to:hover{border-color:rgba(255,74,0,.6);background:rgba(255,74,0,.09);transform:translateY(-1px)}
.od-svc.is-off{opacity:.4;filter:grayscale(1);cursor:not-allowed;pointer-events:none;transform:none}
@media(max-width:820px){
  .od-rail{flex-direction:column;align-items:stretch;gap:.6rem}
  .od-rail-lead{display:flex !important}
  .od-rail-meta{white-space:normal}
  .od-rail-acts{display:flex;flex:1;gap:.42rem}
  .od-rail .od-svc{flex:1;justify-content:center;padding:.68rem .3rem;gap:.35rem}
  .od-rail .od-n{font-size:.82rem}
  .od-rail .od-art{width:22px;height:22px}
  .od-dir{padding:.68rem .55rem;border:1px solid var(--line,rgba(244,239,231,.14))}
  .od-dir span{display:none}
}
"""
CSS_MARKER = "order-rail v3: info block + 3 equal services"

def patch_css(root, dry):
    path = os.path.join(root, "css", "profile-v4.css")
    css = open(path, encoding="utf-8").read()
    if CSS_MARKER in css:
        return "css already patched"
    if not dry:
        open(path, "w", encoding="utf-8").write(css.rstrip("\n") + "\n" + RAIL_CSS)
    return "css patched"

SLUG_RE = re.compile(r'bn-shop-data"[^>]*>\s*(\{.*?\})\s*</script>', re.S)
RAIL_RE = re.compile(r'<!-- TPL:order-rail -->.*?<!-- /TPL:order-rail -->', re.S)

def slug_of(html_text, path):
    m = SLUG_RE.search(html_text)
    if m:
        try: return json.loads(m.group(1)).get("slug")
        except Exception: pass
    return os.path.basename(os.path.dirname(path))

def main(argv):
    dry = "--dry-run" in argv
    only = argv[argv.index("--slug")+1] if "--slug" in argv else None
    root = argv[argv.index("--root")+1] if "--root" in argv else \
           os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows = {r["slug"]: r for r in fetch_rows()}
    tpath = os.path.join(root, "build", "toast_links.json")
    toast = json.load(open(tpath, encoding="utf-8")) if os.path.exists(tpath) else {}
    print("shops: %d, toast-verified entries: %d" %
          (len(rows), sum(1 for v in toast.values() if v.get("confidence") in ("high","review"))))
    print(patch_css(root, dry))
    boba = os.path.join(root, "boba")
    patched = skipped = missing = norail = 0
    for dp, _, files in os.walk(boba):
        if "index.html" not in files: continue
        fp = os.path.join(dp, "index.html")
        html_text = open(fp, encoding="utf-8").read()
        if "<!-- TPL:order-rail -->" not in html_text:
            norail += 1; continue
        slug = slug_of(html_text, fp)
        if only and slug != only: continue
        row = rows.get(slug)
        if not row:
            missing += 1; continue
        new = build_rail(row, toast)
        out = RAIL_RE.sub(lambda _: new, html_text, count=1)
        # fix the "To go" quickfact Uber link too
        old_ue = "https://www.ubereats.com/search?q=" + q(row["name"])
        m = re.search(r'href="' + re.escape(old_ue) + r'"', out)
        if m:
            newm = re.search(r'href="(https://www\.ubereats\.com/search\?diningMode=DELIVERY[^"]*)"', new)
            if newm:
                out = out.replace('href="' + old_ue + '"', 'href="' + newm.group(1) + '"')
        if out != html_text:
            if not dry:
                open(fp, "w", encoding="utf-8").write(out)
            patched += 1
        else:
            skipped += 1
    print("patched=%d skipped=%d missing-in-db=%d non-profile=%d%s" %
          (patched, skipped, missing, norail, "  [DRY-RUN, nothing written]" if dry else ""))

if __name__ == "__main__":
    main(sys.argv[1:])
