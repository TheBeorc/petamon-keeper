# PET-A-MON keeper — sync log

Newest first. One entry per review or port: date, trigger, per-app result, commits.

## 2026-11-23 — camera zoom + pinch everywhere (user request)
- Pinch-to-zoom added to the shared camera hook (`usePinch` in `src/app/camera.ts`, Pointer Events,
  `gesturestart` blocked for iOS Safari, `touch-action: none` on `.cam`); slider kept.
- Birds of Milan `d380bfd`: pinch added to its existing zoom. 171 tests ✓.
- Cattamonio `0fca83b`, Doggos `4e86bfa`: full zoom ported from Birds (+ pinch, `zoom` i18n key, CSS,
  4K stream request). 151 / 152 tests ✓, typecheck + eslint ✓.
- Not ported (Birds-specific, user decision): location rule / "released" phase.
- Not verified on a real phone: e2e uses Chromium's fake camera; test pinch on iPhone + Android.

## 2026-11-23 — keeper set up (baseline)
- Baseline marked as reviewed: cattamonio `3d053c6`, doggos `baa29f3`, birdsofmilan `3d05fcf`.
- Drift measured (see `docs/COMMON.md`); open items recorded in `BACKLOG.md`.
- Tests at baseline: cattamonio typecheck + vitest 148/148 ✓.
