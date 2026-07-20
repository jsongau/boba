# Boba Night — REPO & DEPLOY (READ THIS FIRST)

_Last verified: 2026-07-20. If anything here conflicts with what you observe, trust the live repo and update this doc._

## The one repo (do not cross projects)
- **GitHub:** `https://github.com/jsongau/niteboba.git` — owner **jsongau**, branch **main**.
- **Local path (device `kyts-macbook-pro`):** `/Users/kytlegacy/Claude/Projects/NiteBoba`
- **Live site:** `https://www.bobanight.com` (Vercel auto-deploys on every push to `main`; `vercel.json` holds redirects). Brand "Boba Night"; repo/folder named "niteboba" — same thing.
- This IS the right repo: the local folder's git remote is jsongau/niteboba, and pushes to it go live at bobanight.com.

### Look-alikes to NOT use for Boba Night
- `jsongau/covercapycodex` — different repo (CoverCapy/dental).
- The `covercapy` GitHub account — see push auth.
- Supabase "BOBA" project — empty; shop data lives in the "CoverCapy" project (below).

## Push auth gotcha (the #1 deploy blocker)
- Repo is owned by **jsongau**; pushes need the **jsongau** credential.
- The Mac is often logged into GitHub as **covercapy**, which is DENIED push access
  (`remote: Permission to jsongau/niteboba.git denied to covercapy`).
- Fix: push as jsongau — username `jsongau`, password = a jsongau classic PAT with `repo` scope. Keychain remembers it after.
- The cloud sandbox and the device VM have NO network to GitHub (`git push` there = `403 from proxy after CONNECT`). Generate + commit for the user, then hand off the push.

## WHY a fresh session "can't find the local repo"
- Every Cowork session starts in a fresh, EMPTY cloud sandbox. The code is NOT in the cloud — only on the Mac at the path above.
- Files are reachable only via the device bridge (`mcp__remote-devices__*`), and only when the desktop app is connected AND the NiteBoba folder is attached to the session.
- Started from web/mobile, or folder not attached → the session sees project docs but not the repo files.
- The cloud workspace is ephemeral; only the git repo + the claude.ai Project docs persist between sessions.
- First move in a new session: `get_device_info` → confirm `/Users/kytlegacy/Claude/Projects/NiteBoba` is a connected folder; if missing, ask the user to connect it. Work under `/sessions/<id>/mnt/NiteBoba`.

## Data source of truth
- Supabase project **CoverCapy** (`hfvbeqlefwwjlrbyxpbj`), table `public.niteboba` (742 rows; 622 open+enriched). Ignore the "BOBA" Supabase project for shop data.

## Generators (being unified on Supabase)
- Profiles: `gen_profiles_v4.py` (v4 template). All 622 open stores on v4 as of 2026-07-20.
- Scaffold (city pages, region hubs, sitemap): `build/gen_site.py`, fed from Supabase via `build/run_sb_scaffold.py`.
- `build/gen_profiles.py` is retired-in-practice — do not use (caused template drift).
- Nav still stale: `build/nav_data.py` derives the mega-nav from `directory/index.html`'s `var SHOPS`. Repoint at Supabase next.

## Deploy flow
1. Generate in the sandbox.
2. Sync into the repo (tar → SendUserFile → device_commit_files → extract) or edit the mounted repo directly.
3. `git add <paths>` (never `-A` — stray bundles/pngs must not be committed), `git commit`.
4. User pushes: `cd /Users/kytlegacy/Claude/Projects/NiteBoba` then `git push origin main`.
5. Vercel rebuilds; verify at bobanight.com.

## Open cleanup (2026-07-20)
- Repoint nav_data/directory SHOPS at Supabase + re-stamp nav.
- Noindex/remove the 119 closed/seed profile pages.
- Retire `build/gen_profiles.py` and `data/stores-seed.csv`.
