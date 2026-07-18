# Session — After Dark palette + deploy fix (18 JUL 2026)

## What changed and why
- **Root cause of "pages look like crap":** the obsidian redesign (commit `cb7d3cd`)
  and everything after it was built and committed but never pushed. Live site
  was serving `7869cee` (unified dark nav on the OLD cream body). Nothing was
  wrong with the design; it was a deploy gap. Jay's Mac clone was stuck at
  `7869cee` and never received the newer commits, so there was nothing to push.
- **After Dark palette, rolled to ALL pages.** Retuned the shared design tokens
  in `css/site.css`, `css/luxury-homepage.css`, `css/nav-midnight.css`,
  `css/motif.css`, and the baked `:root` in `build/gen_profiles.py`. Every body
  now carries a fixed radial glow: neon-pink (top-right) + royal purple
  (top-left) + faint jade (foot) over the obsidian base. Regenerated 333
  profiles + 46 city + 5 region + 13 intent pages.
- **Purple came back as a ROYAL accent, not the old lavender wash.** New tokens
  `--orchid #b46bd6`, `--imperial #5c2c86`, `--velvet #2a0b12`, `--gilt #F4DDA2`.
  Purple shows as the background glow and as a halo ring on the profile
  medallion. Neon action colour nudged `#ff3f6f -> #ff2f6d`.

## Decisions made
- **Aesthetic direction = "After Dark."** Everyday wording (date night, find a
  spot, good places to try) with a luxe/neon LOOK doing the flirting. Jay
  rejected the safe reframe and picked the explicit-luxe visual register;
  build boundary held: no copy that literally advertises sugar-dating (protects
  AI-citation SEO + shop partnerships + future payments), full visual heat is
  fine. Direction previews `after-hours-preview-v2/v3.html` were delivered as
  disposable previews and kept OUT of the repo.
- **Gifting money path = gift-card aggregator (Tremendous/Tango), not delivery
  logistics.** Toast gift cards are per-restaurant only, so they can't be the
  cross-shop path. DoorDash Drive / Uber Direct (white-label logistics) are a
  much heavier later option.

## Decisions rejected
- Literal sugar-daddy/mistress COPY (brand + SEO + payments risk).
- Deploying straight to Vercel via MCP (would bypass GitHub git history; Jay's
  model is git = source of truth, "commit = saved, push = live").
- Making purple the dominant theme colour (kept as accent; the `Featured` paid
  pill needs to move off purple to gilt-gold so the paid signal survives — NOT
  yet done, flagged).

## Traps discovered
- Cloud container has NO GitHub push credentials; `device_bash` on the Mac has
  NO network. So exactly one `git push` must run in Jay's real Terminal. Transport
  for commits cloud -> Mac is a **git bundle** (`git bundle create b34b8c0..main`).
- A stale `.git/index.lock` sat in the Mac repo; `device_bash` cannot `rm`
  mounted files ("Operation not permitted") — work around with `mv`, or Jay
  removes it in Terminal.
- Theme tokens are duplicated across 5 CSS files + generators (no single source).
  Any palette change must touch every `:root`.

## Gifting backend — the plan (NOT built; awaiting Stripe/Tremendous setup)
- Supabase (existing `CoverCapy` project): `standing_orders` (recipient + drink
  + mods + optional preferred shop), `gifts` (sender, recipient, amount,
  provider, status, message), lightweight `accounts` (reach a recipient by
  phone/email; no heavy auth for v1).
- 3 Vercel serverless functions: set standing order · view by shareable link ·
  `POST /api/gift` (server-side only; calls Tremendous with the SECRET key,
  never in the browser). Webhook flips gift -> redeemed.
- **Concept to remember: server-side secret.** Anything that spends money runs
  on a server holding a key the browser never sees, or the Tremendous float
  gets drained. This is what turns a static directory into a transacting product.
- Jay must create + fund Stripe + Tremendous business accounts (Claude cannot
  create accounts or enter payment credentials). Claude wires the code with a
  swappable, mockable provider adapter so the whole flow is clickable first.

## Dice-roll — the spec (NOT built)
- Two-stage: roll for a spot, then roll for a drink. Both resolve to a REAL shop
  open right now (reuse `js/near-index.json` + `window.CBS` drink data). Working
  demo lives in `after-hours-preview-v3.html`.

## Exact next steps
1. Jay pushes (one line) -> Vercel `bobatime` -> bobanight.com goes After Dark.
2. Screenshot the LIVE pages to confirm (not local).
3. Build interior-page intensity pass IF Jay wants profiles closer to v3 heat.
4. Backend: stand up the 3 Supabase tables + `/api/gift` skeleton with mock
   provider. This is the named next backend task.

## Stack / approach note (for future sessions)
Static multi-page HTML + vanilla JS, Vercel auto-deploy on push to
`jsongau/niteboba` main, Supabase warehouse synced by hand/scripts. Deploy from
cloud = git bundle -> Mac -> push. Theme = obsidian + After Dark glow (neon-pink,
royal purple, jade, champagne gold). Anti-AI copy standard enforced by
`build/copy_audit.py`.
