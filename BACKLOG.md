# PET-A-MON keeper — backlog

## Needs decision (user)

_(none)_

## Ready to port (no decision needed)

_(none)_

## Declined by the user (do not propose again)
- **`home_name` short home-screen name** (Birds) → Cattamonio/Doggos: no visible effect there, their brand is already short. Declined 2026-11-23.
- **Email preview domain** (`src/routes/lovable/email/auth/preview.ts`): Lovable-generated scaffold, preview only. Dropped 2026-11-23.

## Done
- 2026-11-23 — **Email sender test → Cattamonio** (`src/test/emailSender.test.ts`, from Doggos). Now in all three apps.
- 2026-11-23 — **Camera zoom + pinch in all three apps** (user request). Birds `d380bfd` (pinch added),
  Cattamonio `0fca83b`, Doggos `4e86bfa` (zoom + slider + pinch ported).
- 2026-11-23 — **Location rule: Birds of Milan only** (user decision). Never port. Second photo for
  birds also stays Birds-only.
