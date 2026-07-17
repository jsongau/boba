# Session 17 JUL 2026 — bobanight.com live, Boba Night rebrand, Supabase truth sync

## What changed and why

1. **Domain went live.** bobanight.com (Porkbun) now points at Vercel project
   `bobatime`: apex ALIAS + `www` CNAME → `cname.vercel-dns.com`. Vercel
   308-redirects apex → `www.bobanight.com`, so **www is the canonical host**.
   Porkbun URL forwarding to the parking page was the old interceptor; the two
   `uixie.porkbun.com` records were replaced. Email MX/SPF records untouched.
2. **Rebrand NiteBoba → Boba Night** (third name: CapyBoba → NiteBoba 11 JUL →
   Boba Night 17 JUL, now matching the real domain). 446 files: visible copy,
   titles, meta, OG, JSON-LD, llms.txt, robots.txt, README, gen_site.py,
   add_spots.py, templates, CLAUDE.md. Wordmark markup is now `Boba <b>Night</b>`.
   Canonical URLs: `https://niteboba.vercel.app` → `https://www.bobanight.com`
   (2,947 occurrences). Site emails → `hello@` / `corrections@bobanight.com`.
3. **Supabase truth sync (new: `build/sync_from_supabase.py`).** DB had drifted
   ahead of the site: 334 rows = 215 open / 99 closed / 8 paused / 12 seed,
   while the site listed 328 shops all implicitly open. An 8-shop random sample
   of the `closed` rows was web-verified by agents: **8/8 confirmed closed**
   (multi-source: Yelp + corroborators), so the status column is trusted.
   Applied: directory SHOPS entries carry `x`/`tc`/`vf` flags; cards show
   Closed (greyed, sorts last) / Paused / Verified open / Hours verifying;
   roulette + Surprise-me pools exclude closed & paused (221 spinnable).
   Input file: `data/stores-status.csv` (slug,status export of the table).

## Decisions made (and rejected)

- **Closed shops stay listed** (Jay's call) with honest CLOSED chips — rejected
  delisting/301. Rationale: keeps history + long-tail "is X closed" queries.
- **www canonical** (matches Vercel's apex→www 308 already configured) —
  rejected flipping to apex-primary mid-launch; flip later in Vercel if wanted.
- **Internal names keep `niteboba`**: GitHub repo, Supabase table, seed CSV,
  localStorage key `niteboba_saved_v1` (rename would wipe user saves).
- **Counts show 328 (listed), not 334 (DB)** until the 6 DB-only shops get
  pages: acai-joint-arcadia, acai-republic-fullerton, berry-brand-tustin,
  birdie-bowl-and-juicery-costa-mesa, paradise-bowls-irvine, ubatuba-acai-brea
  (all status=seed; run add_spots.py with full data to publish them).
- Runtime Supabase reads rejected again — static + sync pipe stays.

## Traps discovered

- Vercel MCP has NO attach-domain API; domain → project is dashboard-only.
- Cloud container can't `curl` the live site (Vercel 403s datacenter IPs) —
  verify redirects from a real browser or Vercel dashboard.
- Porkbun URL-forwarding created the parking ALIAS; removing the forward can
  remove the ALIAS with it — re-check DNS records after touching forwarding.
- The duplicate Vercel project `boba` still auto-deploys every push
  (harmless but wasteful) — disconnect pending, see CLAUDE.md.
- Cloud clone has no GitHub credentials: commits land locally; push happens
  from Jay's Mac (device bridge to `~/Claude/Projects/NiteBoba`) or by Jay.

## Exact next steps

1. Jay: Porkbun → Email Forwarding → create `hello@` + `corrections@`.
2. Jay: Vercel rename `bobatime`→`bobanight`; disconnect duplicate `boba`.
3. On "deploy": sync commits to Jay's Mac clone, push → auto-deploy, then
   verify live + Google Search Console: add property `bobanight.com`
   (domain-level), submit `https://www.bobanight.com/sitemap.xml`.
4. Phase C: night-intent SEO (open-late pages per area, FAQ schema).
5. Phase D: nav/mega-menu + breadcrumbs (+ BreadcrumbList schema) — research
   findings from this session's agents are in the workflow output.
6. Phase E: theme unification + roulette as sitewide modal (keep the page).
7. Closed-shop profile PAGES still look open — add closed banner + noindex
   via gen_site pass (directory now honest; profiles are not yet).

## Stack notes (for future sessions)

Static HTML + vanilla JS, no framework, no build step beyond python scripts.
Jay's preferred flow: preview files -vN → approval → commit → his "deploy" =
push to main = live. Evidence with every preview (screenshots/diffs).
