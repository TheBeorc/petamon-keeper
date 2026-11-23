# petamon-keeper

Keeper for the PET-A-MON section — Cattamonio, Doggos, Birds of Milan (Lovable apps sharing one
codebase). Open a Claude Code session with this repo plus the three app repos; `CLAUDE.md` tells
Claude how to keep them aligned.

- `CLAUDE.md` — the keeper's role and rules
- `apps.json` — app registry and theme tokens
- `docs/COMMON.md` — shared vs. themed vs. app-specific map
- `BACKLOG.md`, `SYNC_LOG.md` — open decisions and history
- `state/sync-state.json` — last reviewed commit per app
- `scripts/keeper.py` — sync / status / news / drift / classify / translate / mark
- `.claude/skills/` — `petamon-port`, `petamon-review`
