---
name: petamon-review
description: Review new commits in the PET-A-MON apps (Cattamonio, Doggos, Birds of Milan) and decide what to port to the siblings. Use on the scheduled keeper check, when the user says one app was updated, or when another session reports a change.
---

# Review PET-A-MON updates

1. `python3 scripts/keeper.py sync` then `python3 scripts/keeper.py news`.
   Nothing new anywhere → mark nothing, reply in one line ("nessuna novità"), stop.
2. For each new commit, read the diff (`git -C ../<app> show <sha>`) and sort it:
   - **Port** — bug fixes and improvements in `core` code, shared UX (camera, zoom, login,
     invites, admin, archive, PWA, email plumbing), tests for those, dependency bumps.
   - **Port the idea, not the code** — `themed` changes whose logic is generic but whose copy
     or colours are per app.
   - **Ask the user** — rule/identity changes, or a feature that could be deliberately exclusive.
   - **Skip** — catalog, species, art, palette, claims, icons, domain, Lovable plan files,
     anything `app-specific`; Lovable-generated churn (formatting of generated files, `.lovable/`).
   Use `python3 scripts/keeper.py drift <paths>` to see whether the siblings already have it.
3. Do the **Port** items with skill `petamon-port` (direct push to main, tests gate).
   Put **Ask** items in `BACKLOG.md` under "Needs decision" with a one-line recommendation.
4. `python3 scripts/keeper.py mark <app>` for each app reviewed, add a dated `SYNC_LOG.md`
   entry (commit → decision → result), commit + push the keeper repo.
5. Report to the user: ported (with links), waiting for their decision, skipped (one line each).
   On a scheduled run with nothing to report, keep the reply to a single line.
