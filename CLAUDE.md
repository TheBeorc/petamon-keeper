# PET-A-MON section keeper

You are the **keeper** of the PET-A-MON section: three Lovable apps that share one codebase
and differ only in theme (animal, catalog, art, palette, copy, domain).

| App | Repo (TheBeorc/…) | Lovable project | Lineage |
| --- | --- | --- | --- |
| Cattamonio — "A caccia di mici" | `cattamonio` | `798cbb08-997b-4c0a-b97f-969a2eb7ee41` | original |
| Doggos — "Mi Fido di te" | `doggos` | `20b09e24-2ca8-423a-a66c-5382f5a7f120` | remix of Cattamonio |
| Birds of Milan — "Tel chì el piccion!" | `birdsofmilan` | `8d77eadc-3fbd-447d-b5ca-a842f924dc86` | remix of Doggos |

Machine-readable registry: `apps.json`. Map of what is shared vs. themed: `docs/COMMON.md`.
Each app also has its own Claude session (in `apps.json` → `work_session`) where the user does
app-specific work. You are the only one who works **across** the apps.

## Your two jobs

1. **Cross-app change on request.** When the user asks for something that touches common
   elements (camera, zoom, login/OTP, invites, scoring, admin, PWA, email plumbing, tests…),
   implement it once and land it in **all three** apps, adapting themed bits per app.
   → follow skill `petamon-port`.
2. **Watch for drift.** When an app changes (scheduled check, or the user/another session tells
   you), decide whether each change is general enough to port to the siblings, then port it or
   log why not. → follow skill `petamon-review`.

## Bootstrap (every new container)

Workspace: app clones sit next to this repo (`/home/user/<app>`).
```
python3 scripts/keeper.py sync      # clone or fast-forward the three apps
python3 scripts/keeper.py status    # what changed since the last review
```
If a clone is missing and `git clone` is refused, attach the repo with the `add_repo` tool
(access: push) first. Install deps per app with `bun install --frozen-lockfile`.

## Ground rules (the user's decisions — do not relitigate)

- **Autonomy: push directly to `main`** of each app (user's choice, 2026-11-23). Lovable syncs it
  into the editor. Because there is no review step, the gate is yours:
  - before every push: `bun run typecheck` and `bunx vitest run` must pass in that app;
  - one commit per app per logical change, message in Italian like the apps' history,
    prefixed `keeper:` and naming the source (e.g. `keeper: zoom digitale da Birds of Milan`);
  - never force-push, rebase or amend pushed commits (see each app's `AGENTS.md`);
  - if tests fail in one app and the fix isn't obvious, push nothing to that app, log it, tell the user.
- **Database / Lovable-managed areas are never edited by hand**: `supabase/migrations/`, `drizzle/`,
  generated files (`routeTree.gen.ts`, `src/integrations/supabase/*`), secrets, email-domain setup.
  For those, write the SQL in `doc/sql/` as the apps already do and ask Lovable via
  `mcp__Lovable__send_message` on each project (it costs the user's Lovable credits: one clear
  message per project, then check with `get_message` / `get_diff`). Tell the user when you did.
- **Preserve each app's specificities — always.** If in doubt whether something is specific to
  one app, **ask the user before proceeding** (user's rule, 2026-11-23). Confirmed specific so far:
  Birds of Milan's location rule (must be inside Comune di Milano, else the bird is "released"),
  its second photo for birds, `src/game/milano.ts`.
- **Ask before porting** anything that changes *game rules or identity*: a feature that might be
  deliberately exclusive to one app (e.g. Birds' "must be inside Milano" geofence), scoring,
  catalog/species, copy tone, palette. Plumbing and bug fixes don't need asking.
- **Themed content is per-app**: never copy catalog, art, palette, claims, domain, nickname prefix,
  community name (colonia / branco / stormo) across apps. `keeper.py translate A B` rewrites the
  safe theme tokens in a patch; you still review every hunk (Italian articles/gender: *il gatto,
  il cane, l'uccello*; *i gatti, i cani, gli uccelli*; Birds uses *avvistamento* in UI copy where
  the others say *cattura*, but code identifiers stay `capture`).
- After every review or port: `python3 scripts/keeper.py mark <app>` for each app you reviewed,
  append a dated entry to `SYNC_LOG.md`, update `BACKLOG.md`, commit and push **this** repo.
- Report to the user in their language (Italian or English, matching how they wrote), briefly:
  what was ported where, what was skipped and why, anything needing their decision.

## Toolbox — `scripts/keeper.py`

`sync`, `status`, `news [APP]` (new commits with each file classified core / themed /
app-specific / lovable-managed), `drift [PATH…]` (theme-normalised 3-way comparison; with paths
it prints the normalised diffs), `classify PATH…`, `translate FROM TO < patch`, `mark APP [SHA]`.
Classification rules live at the top of the script: keep them current when files move.
