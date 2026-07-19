# Session — Sign-in portal + accounts (2026-07-19 pm)

## What changed and why
The /nearby/ pink CTA went Mystery Roll -> Sign in (user cut the roll). "Sign in" links to a new
static portal at /account/. Goal: turn the device-local Black Book (saved shops in localStorage) into
real accounts whose saved spots sync across devices — the retention lever for a directory.

## Architecture (backend-first)
- Auth: Supabase Auth, **email one-time codes** (signInWithOtp + verifyOtp, type:"email"). Chosen over
  magic links because codes need no redirect-URL/dashboard config and work on a static site immediately.
  Google OAuth deferred (needs client id/secret from Jay).
- DB: the shared "BOBA" Supabase project `uqefyfqwwkkvydkgepgf` (free tier caps at 2 projects; Jay chose
  shared-with-RLS over paying for a dedicated one). Tables namespaced boba_*:
  - boba_profiles (id uuid -> auth.users, handle, created_at)
  - boba_favorites (id, user_id -> auth.users, shop_slug, shop_name, shop_where, shop_url, created_at, unique(user_id,shop_slug))
  - RLS: owner-only select/insert/update(/delete). Profile created lazily client-side on sign-in (no
    trigger on the shared auth.users, so other apps' signups don't create boba rows).
- Frontend /account/index.html: loads supabase-js from jsdelivr CDN (npm + CDN both blocked in the cloud
  sandbox, so it's verified via a stubbed client; real email round-trip must be tested on the live site).
  Guarded init + 3.5s boot fallback so a slow/blocked lib never leaves a dead "Loading…" screen.
- Black Book migration: on first sign-in, localStorage niteboba_blackbook_v1 -> boba_favorites (upsert,
  ignoreDuplicates), then set niteboba_bb_migrated_v1 so it runs once.

## Security fix (do not skip)
Advisor flagged 6 CoverCapy reference tables with RLS OFF in the shared project = anon key could read AND
write every row. Fixed: enabled RLS + a `for select using (true)` policy on each, which keeps public reads
working but blocks anon writes. Service role bypasses RLS so admin/service writes are unaffected. Reads
can be tightened later once CoverCapy's access model is confirmed.

## Keys (public, safe in client)
- URL https://uqefyfqwwkkvydkgepgf.supabase.co
- publishable key sb_publishable_0Y-o-QD73luyTYUcjWRWzQ_7b9ogFLs  (RLS is the guard, not key secrecy)

## Also
Taro Yuan floater on /nearby/ rebuilt to lead with search (magnifier + "Search Boba Night" + prompt),
featured house demoted to a small footer link, brief attention pulse (3x). DATA md5 bc29f344d082 unchanged.

## Exact next steps
1. Live-test the email code round-trip at bobanight.com/account/ (sandbox couldn't send/receive email).
2. Configure custom SMTP in Supabase Auth (default email is rate-limited ~a few/hour) before real traffic.
3. Add a "Save this spot" control on shop profile pages that inserts into boba_favorites when signed in.
4. Optional: Google OAuth (needs client id/secret).
5. Still pending: sitewide finder-header rollout via shared assets (approved, not yet run).
6. Consider .gitignore for *.bundle and card-*.png (untracked junk in repo root).
