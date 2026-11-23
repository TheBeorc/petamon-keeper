---
name: petamon-port
description: Implement or port a change across the three PET-A-MON apps (Cattamonio, Doggos, Birds of Milan). Use when the user asks for a change to shared behaviour (camera, zoom, login/OTP, invites, admin, scoring plumbing, PWA, emails, tests) or when petamon-review decided a change in one app should reach the others.
---

# Port a change across PET-A-MON

## 1. Frame it
- Name the change in one line and the **source** (user request, or `<app>@<sha>`).
- `python3 scripts/keeper.py sync` so every clone is at `origin/main`.
- List touched paths and `python3 scripts/keeper.py classify <paths>`:
  - `core` → port as-is (after translation of theme tokens);
  - `themed` → port the logic, rewrite copy/colours per app;
  - `app-specific` → do not copy; write the per-app equivalent only if the user wants it;
  - `lovable-managed` → never by hand: SQL goes in `doc/sql/NN_*.sql` + a Lovable `send_message`.
- If it touches game rules or identity (see CLAUDE.md), ask the user first.

## 2. Build it once
- For a new feature, implement it in the app the user named, or in **Cattamonio** by default
  (the original; Doggos is closest to it, Birds diverges most — see `docs/COMMON.md`).
- Add/adjust tests next to the existing ones (`src/test/`, `tests/e2e/`).
- `bun run typecheck && bunx vitest run` in that app.

## 3. Carry it to the siblings
For each other app:
```
git -C ../<src> diff <base>..<head> -- <paths> > /tmp/…/change.patch   # or `git format-patch`
python3 scripts/keeper.py translate <src> <dst> < change.patch > dst.patch
git -C ../<dst> apply --3way dst.patch     # resolve conflicts by hand
```
- `drift <paths>` before and after: the normalised diff of the ported files should shrink or stay
  at the known themed differences, never grow with unrelated lines.
- Review every hunk for theme leaks (wrong animal, domain, colour, nickname prefix, route
  `/colonia` `/branco` `/stormo`) and Italian grammar.
- i18n: add the same keys to `it.ts` and `en.ts` in every app (types enforce parity per app).
- `bun install --frozen-lockfile` if needed, then `bun run typecheck && bunx vitest run`.

## 4. Land it
- Per app: one commit `keeper: <cosa> (da <origine>)`, push to `main`
  (`git -c push.negotiate=true push origin main`). If the push is rejected because main moved,
  `git pull --rebase` (only your own unpushed commit), re-test, push again.
- Database part, if any: one `mcp__Lovable__send_message` per project with the exact SQL file to
  apply verbatim (as `doc/LOVABLE_STEPS.md` does), then `get_message` until done and
  `npm run sql:compare` if the app has it.
- `python3 scripts/keeper.py mark <app>` for every app now aligned; entry in `SYNC_LOG.md`;
  remove/close the item in `BACKLOG.md`; commit + push the keeper repo.
- Tell the user: what landed where (commit links), what was adapted, what still needs Publish
  in Lovable (pushing to main updates the editor/preview, **not** the published site).
