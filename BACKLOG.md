# PET-A-MON keeper — backlog

## Needs decision (user)

_(none)_

## Ready to port (no decision needed)

4. **`home_name` i18n key** (Birds): short home-screen/installed-app name read from i18n instead of
   the brand constant. Small, generic. Port to Cattamonio + Doggos with each app's short name.
5. **`src/test/emailSender.test.ts`** (Doggos, Birds) → Cattamonio. Test only.
6. **Email preview ROOT_DOMAIN** in Doggos uses `doggos.lovable.app` while the sender is
   `doggos.cattamonio.com`. Cosmetic (preview page only); align when next touching email code.

## Done
- 2026-11-23 — **Camera zoom + pinch in all three apps** (user request). Birds `d380bfd` (pinch added),
  Cattamonio `0fca83b`, Doggos `4e86bfa` (zoom + slider + pinch ported).
- 2026-11-23 — **Location rule: Birds of Milan only** (user decision). Never port. Second photo for
  birds also stays Birds-only.
