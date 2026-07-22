#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boba Night - Toast presence checker.

For every OPEN shop in Supabase, queries Toast Local search
(https://toast.app/pickup/search) with the shop name at the shop's coordinates and
records a match when a returned restaurant's name and city line up with ours.
Output: build/toast_links.json  {slug: {toast_url, toast_name, toast_city, confidence}}
Resumable: already-checked slugs are skipped on re-run.

NETWORK REQUIRED - run on the Mac:
    python3 /Users/kytlegacy/Claude/Projects/NiteBoba/build/check_toast.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request

SB  = "https://hfvbeqlefwwjlrbyxpbj.supabase.co"
KEY = "sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toast_links.json")
UA  = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
REC = re.compile(r'"city":"([^"]*)","state":"[A-Z]{2}"\},"name":"([^"]*)","shortUrl":"([^"]*)"')

def ns(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def fetch_shops():
    rows, page = [], 0
    while True:
        q = ("/rest/v1/niteboba?select=slug,name,city,latitude,longitude"
             "&status=eq.open&latitude=not.is.null&longitude=not.is.null"
             "&order=name.asc&limit=1000&offset=%d" % (page * 1000))
        req = urllib.request.Request(SB + q, headers={
            "apikey": KEY, "Authorization": "Bearer " + KEY, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            batch = json.load(r)
        rows.extend(batch)
        if len(batch) < 1000: break
        page += 1
    return rows

def toast_search(name, city, lat, lng):
    qs = urllib.parse.urlencode({
        "q": name, "lat": "%.6f" % lat, "long": "%.6f" % lng,
        "placeType": "region", "place": "%s, CA" % city})
    req = urllib.request.Request("https://toast.app/pickup/search?" + qs,
                                 headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace").replace('\\"', '"')

def match(shop, html_text):
    a = ns(shop["name"])
    best = None
    for city, rname, short in REC.findall(html_text):
        b = ns(rname)
        if len(a) < 4 or len(b) < 4: continue
        name_ok = b.startswith(a) or a.startswith(b) or a in b
        if not name_ok: continue
        same_city = ns(city) == ns(shop["city"])
        cand = {"toast_url": "https://toast.app/r/%s/order" % short,
                "toast_name": rname, "toast_city": city,
                "confidence": "high" if same_city else "review"}
        if same_city: return cand
        best = best or cand
    return best

def main():
    done = {}
    if os.path.exists(OUT):
        done = json.load(open(OUT, encoding="utf-8"))
    shops = fetch_shops()
    todo = [s for s in shops if s["slug"] not in done]
    print("shops: %d total, %d already checked, %d to go" % (len(shops), len(done), len(todo)))
    for i, s in enumerate(todo):
        try:
            page = toast_search(s["name"], s["city"], float(s["latitude"]), float(s["longitude"]))
            m = match({"name": s["name"], "city": s["city"]}, page)
            done[s["slug"]] = m or {"confidence": "none"}
            if m: print("  + %s -> %s (%s)" % (s["slug"], m["toast_name"], m["confidence"]))
        except Exception as e:
            print("  ! %s: %s" % (s["slug"], e))
            done[s["slug"]] = {"confidence": "error", "error": str(e)[:120]}
        if (i + 1) % 10 == 0 or i == len(todo) - 1:
            json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print("  %d/%d checked" % (i + 1, len(todo)))
        time.sleep(1.0)
    json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    hi = sum(1 for v in done.values() if v.get("confidence") == "high")
    rv = sum(1 for v in done.values() if v.get("confidence") == "review")
    er = sum(1 for v in done.values() if v.get("confidence") == "error")
    print("DONE. on-toast(high): %d, needs-review: %d, errors: %d, not-on-toast: %d"
          % (hi, rv, er, len(done) - hi - rv - er))

if __name__ == "__main__":
    main()
