# Build

`gen_site.py` reads the shop data and writes static HTML (data -> build -> static files; not an app).

## Run
```
python3 build/gen_site.py
```
Writes: region hubs (/area/*), city pages (/boba/ca/*), shop profiles (/boba/ca/*/*),
by-vibe pages (/best/*), guides (/guide/*), landmark pages (/near/*), new-openings
(/new/*), cities index (/cities/), legal + trust pages (/about, /how-we-rank,
/how-we-make-money, /report, /claim, /privacy, /terms), sitemap.xml, robots.txt, llms.txt.

## SEO gating (automatic)
- City pages + region hubs: indexable (real directory value).
- Shop profiles: `noindex,follow` until enriched (real hours/coords). They flip to
  indexable automatically once load_rows() returns latitude for a shop.
- By-vibe pages: honest landing pages, no fabricated rankings, noindex.
- sitemap.xml lists only indexable pages.

## Enrich later
Currently reads data/stores-seed.csv (seed = Verifying state). After the boba-enrich
Edge Function fills coords/hours/phone, export the enriched rows and point load_rows()
at them, then re-run. No template changes needed.
