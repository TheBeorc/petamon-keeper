# PET-A-MON keeper — sync log

Newest first. One entry per review or port: date, trigger, per-app result, commits.

## 2026-11-23 — iPhone: no second code after Add to Home Screen (user request)
- Problem: on iPhone the Home Screen app has its own storage; since iOS 17.2 only cookies are copied
  from Safari, and the Supabase session lives in localStorage → second OTP email.
- Fix: while the install guide is open, Safari keeps a one-time Supabase token (admin generateLink,
  no email; approved players only) in a 30-min SameSite=Strict Secure cookie. The Home Screen app,
  first launch without a session, exchanges it via verifyOtp({token_hash}) for its own session,
  deletes the cookie and inherits the accepted data notice. Fallback: normal code login.
  Android unchanged (installed PWA shares Chrome storage).
- Cattamonio `2807eed` (built here), Doggos `43d8518`, Birds `41f7dbd` (same patch, no theme tokens).
  Unit 161 / 161 / 180 ✓; e2e 38 / 38 / 39 ✓ incl. 3 new iPhone scenarios.
- Birds `7c5840a`: pre-existing stale e2e assertion ("Eyes up, Milan" → "Tel chì el piccion!")
  and lost exec bit on `scripts/sql-apply.sh` fixed.
- Not verifiable here: real iPhone (cookie copy at Add to Home Screen) and real Lovable Cloud
  generateLink. To test on a phone after Publish.

## 2026-11-23 — backlog cleanup (user decisions)
- Cattamonio `7639b7b`: `emailSender.test.ts` ported from Doggos (152 tests ✓; verified it fails on a wrong sender).
- Declined: `home_name` port. Dropped: email preview domain alignment.

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
