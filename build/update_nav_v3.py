#!/usr/bin/env python3
"""Nav V3 'Neon Cup' markup update, applied in place to every page that carries
the finder header (plus templates/nav.html and build/nav-finder-partial.html).

Idempotent. DRY-RUN by default; pass --apply to write.

Per file:
  1. remove the New tab (data-item="new"), keep a 'New openings' link in the Shops rail
  2. rename the 'Ratings & meetups' trigger label to 'Society'
  3. wrap #meterChip in a .rad-anchor and move #meter into a #radPop popover
     with minus/plus steppers (the cup gauge itself is injected by js/finder.js)
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APPLY = "--apply" in sys.argv

SKIP_DIRS = {".git", "node_modules", "_to_delete", "design-library", "docs", "examples"}
EXTRA = [os.path.join(ROOT, "templates", "nav.html"),
         os.path.join(ROOT, "build", "nav-finder-partial.html")]
SKIP_PATHS = {"nearby/index.html", "account/index.html"}

POP_TPL = '''<span class="rad-anchor" id="radAnchor">{chip}<div class="rad-pop" id="radPop" hidden>
  <p class="rad-title">Set your range</p>
  <div class="rad-row">
    <button class="rad-btn" id="radMinus" type="button" aria-label="One mile closer">&minus;</button>
    <div class="rad-mid">{meter}<p class="rad-read"><b id="radVal">5</b> miles around you</p></div>
    <button class="rad-btn" id="radPlus" type="button" aria-label="One mile farther">+</button>
  </div>
</div></span>'''

def transform(s):
    changed = False
    # 1) drop the New tab
    i = s.find('<div class="bn-item" data-item="new">')
    if i >= 0:
        j = s.find('<div class="bn-item" data-item="pick-for-me">', i)
        if j > i:
            s = s[:i] + s[j:]; changed = True
    old_rail = '<a class="bn-rail-b bn-rail-link" href="/near/">Near a landmark</a>'
    if old_rail in s and 'href="/new/">New openings<' not in s:
        s = s.replace(old_rail, old_rail + '<a class="bn-rail-b bn-rail-link" href="/new/">New openings</a>')
        changed = True
    # 2) rename to Society
    if 'aria-controls="bnpanel-ratings-meetups">Ratings &amp; meetups<span class="bn-caret"' in s:
        s = s.replace('aria-controls="bnpanel-ratings-meetups">Ratings &amp; meetups<span class="bn-caret"',
                      'aria-controls="bnpanel-ratings-meetups">Society<span class="bn-caret"')
        changed = True
    else:
        # trigger may carry an injected svg icon between attrs and label
        k = s.find('aria-controls="bnpanel-ratings-meetups"')
        if k >= 0:
            seg = s[k:k+700]
            seg2 = seg.replace('Ratings &amp; meetups<span class="bn-caret"', 'Society<span class="bn-caret"', 1)
            if seg2 != seg:
                s = s[:k] + seg2 + s[k+700:]; changed = True
    # 3) popover shell (skip if already applied)
    if 'id="radPop"' not in s:
        mchip = re.search(r'<button class="meter-chip"[^>]*id="meterChip"[^>]*>.*?</button>', s, re.S)
        mmeter = re.search(r'<div class="meter"[^>]*id="meter"[^>]*>.*?</div>', s, re.S)
        if mchip and mmeter:
            meter_html = mmeter.group(0)
            s = s.replace(mchip.group(0), POP_TPL.format(chip=mchip.group(0), meter=meter_html), 1)
            occ = [m.start() for m in re.finditer(re.escape(meter_html), s)]
            if len(occ) > 1:
                x = occ[-1]; s = s[:x] + s[x+len(meter_html):]
            changed = True
    return s, changed

def files():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and d != "templates"]
        for fn in fns:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn)
    for p in EXTRA:
        if os.path.exists(p):
            yield p

n_changed = n_skipped = 0
for path in files():
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel in SKIP_PATHS:
        continue
    s = open(path, encoding="utf-8").read()
    if 'id="meterChip"' not in s and 'bnpanel-ratings-meetups' not in s:
        n_skipped += 1; continue
    new, changed = transform(s)
    if changed:
        n_changed += 1
        if APPLY:
            open(path, "w", encoding="utf-8").write(new)
print(("APPLIED" if APPLY else "DRY-RUN"), "| changed:", n_changed, "| no-nav skipped:", n_skipped)
