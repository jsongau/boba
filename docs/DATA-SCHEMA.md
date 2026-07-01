# DATA-SCHEMA — MODEL, ENRICHMENT PIPELINE, PROVENANCE
> The seed is a lead list. This is how it becomes verified, structured, citable data — and the rules that keep it honest.

---

## 1. PROVENANCE & HONESTY (read first)
- **The SCBD seed is a lead list, not ground truth.** Business names + addresses are factual data; building your own directory of real businesses is standard and fine. But (a) it's stale, (b) it's incomplete, and (c) for both quality and independence you must **re-verify every record against a primary source (Google Business Profile)** before publishing. Don't lift the source's editorial text or its arrangement — rebuild from primary data. Treat the seed as "here are leads to go verify," nothing more.
- **No field is publishable until it has a `verified_at` date and a `source`.** Especially hours and open/closed status. (Locked Rule #1.)
- **Third-party ratings are reference-only**, shown with attribution + date + link, never stored as first-party schema. (Locked Rule #2.)
- Anything unverified in a draft page is written as `{{VERIFY: ...}}` and blocked at the QA gate.

---

## 2. CANONICAL SHOP RECORD (the target schema)
This is what each shop becomes after enrichment. Mirror it as a Supabase table (`shops`) if reusing the CoverCapy stack.

```
id                  uuid
slug                text        # canonical, stable, never reused
name                text        # verified, NAP-canonical
brand_id            uuid|null   # FK -> brands (chains)
status              enum        # seed | unverified | open | temporarily_closed | closed
street              text
city                text
region_slug         text        # sgv | little-saigon | convoy | ...
state               text        # CA
postal_code         text
lat                 numeric
lng                 numeric
phone               text|null
website             text|null
gbp_url             text|null   # Google Business Profile (the verification anchor)
instagram           text|null
hours               jsonb       # per-day open/close; powers open-late + "open now"
price_band          enum|null   # $ | $$ | $$$
signature_drinks    text[]      # verified/observed, e.g. ["Black Sugar Boba Milk"]
# --- first-party ATTRIBUTES (the moat: structured answers that exist nowhere else) ---
attr_brown_sugar    bool|null   # cooks/serves notable brown sugar boba
attr_fruit_tea      bool|null   # strong fresh fruit tea program
attr_matcha         bool|null
attr_non_dairy      bool|null   # meaningful non-dairy options
attr_loose_leaf     bool|null   # brews from loose-leaf vs powder (credibility signal)
attr_seating        enum|null   # none | limited | ample
attr_wifi           bool|null
attr_outlets        bool|null
attr_drive_thru     bool|null
attr_food           bool|null   # popcorn chicken / Taiwanese eats
attr_late_close     time|null   # latest typical close (derived from hours)
# --- editorial FIT scores (0-3, our opinion, method documented) ---
fit_date_night      int|null
fit_first_date      int|null
fit_study           int|null
fit_group           int|null
fit_aesthetic       int|null
# --- provenance ---
source              text        # SCBD | google_business | yelp | instagram | field_visit
verified_at         date|null
hours_verified_at   date|null
created_at          timestamptz
updated_at          timestamptz
```

Supporting tables: `brands` (chain hub data), `landmarks` (name, lat/lng, slug, type — campuses, Disneyland, malls), `openings` (shop_id, opened_on, detected_on, source) for the freshness feeds, `closures` (shop_id, closed_on, detected_on, source).

---

## 3. ENRICHMENT PIPELINE (seed → publishable, per record)
Run as a repeatable job. Each step writes `source` + a date.

1. **Geocode.** street+city+state → lat/lng. (Reuse the CoverCapy geocoding approach — you already geocoded OC dentist records.)
2. **Entity match / dedupe.** Resolve against Google Places: confirm the shop exists at that address, capture `place_id`, `gbp_url`, canonical name, phone, website, status. Collapse seed dupes; attach `brand_id` for chains.
3. **Status check.** open / temporarily_closed / permanently_closed → set `status`, `verified_at`. **Closed shops are suppressed, not deleted** (archive profile with closure date).
4. **Hours.** Pull verified hours → `hours` jsonb → derive `attr_late_close`. Set `hours_verified_at`.
5. **Attributes.** Populate `attr_*` from primary signals (GBP attributes, official menu/site, observable facts). Anything you can't substantiate stays `null`, not guessed.
6. **Signature drinks.** From official menu / consistent first-party mentions. Observed, not invented.
7. **Fit scores.** Editorial 0–3 per fit dimension, applied by a documented rubric (below). These are opinions and labeled as such.
8. **QA gate.** Record is "publishable" only when: status ∈ {open, temporarily_closed}, lat/lng present, hours present + dated, no `{{VERIFY}}` left in derived copy.

### Fit-score rubric (document it; it's the "how we rank" honesty)
- **date_night (0–3):** seating quality + ambiance/noise + later hours + walkable to dinner/dessert. (Loud, tiny, take-out-only ⇒ low.)
- **first_date (0–3):** quieter/calmer than date_night; easy conversation; not a 2-hour line.
- **study (0–3):** seating + wifi + outlets + tolerant of long stays.
- **group (0–3):** capacity + food + tolerates noise/energy.
- **aesthetic (0–3):** photo-worthy interior (substantiated, not assumed).

---

## 4. NEW-OPENING DETECTION (feeds the freshness engine)
Weekly, per region: query Google ("new boba {city} 2026"), Yelp "Hot & New," IG/TikTok geotags → candidate list → run the enrichment pipeline → insert into `openings` + publish to `/new/{region}/` with `opened_on` (or "newly opened, opened date {{VERIFY}}") and link to the new profile. New openings also trigger re-render of the relevant city + qualifying intent pages.

> Honesty note: a TikTok claiming "just opened" is a *lead*. Verify existence + address via GBP before publishing, and only state an opening date if you can confirm it; otherwise "recently opened (date to confirm)."

---

## 5. EXPORT CONTRACT (data → templates)
Templates consume a flat per-page JSON derived from the tables. Example for an intent page:
```json
{
  "place":{"name":"Irvine","slug":"irvine","type":"city","region_slug":"oc"},
  "intent":{"slug":"date-night","label":"date night"},
  "verified_at":"2026-06-26",
  "picks":[
    {"name":"...","slug":"...","why":["...","..."],"order":"...",
     "fact":"open until 11 PM Fri–Sat","neighborhood":"Diamond Jamboree",
     "fit_date_night":3,"hours_verified_at":"2026-06-20","gbp_url":"..."}
  ],
  "faq":[{"q":"...","a":"..."}]
}
```
Templates render facts verbatim from this object; the model only writes the `why`/`faq` editorial within the constraints of the real attributes. No field in the rendered page may exist that isn't in this object or explicitly marked `{{VERIFY}}`.
