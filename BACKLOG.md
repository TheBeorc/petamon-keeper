# PET-A-MON keeper — backlog

## Needs decision (user)

1. **SEO from Cattamonio (Lovable, 2026-11-25) → Doggos + Birds?** Cattamonio now allows Google
   indexing (removed `noindex`), has a `/sitemap.xml` (`src/lib/sitemap.ts`, `staticData.sitemap`
   on every route), main headings on public pages, page-specific share text, canonical/og:url on
   `cattamonio.com`, and a Google Search Console verification tag. The siblings are still `noindex`.
   *Recommendation: port the generic part (sitemap mechanism, headings, share text) only if you want
   Doggos/Birds findable on Google; the verification tag and domains are per app and need your own
   Search Console setup per domain.* Counter-argument: these are friends-only invite games; being
   indexed brings strangers to a login wall and no benefit.

## Ready to port (no decision needed)

_(none)_

## Declined by the user (do not propose again)
- **`home_name` short home-screen name** (Birds) → Cattamonio/Doggos: no visible effect there, their brand is already short. Declined 2026-11-23.
- **Email preview domain** (`src/routes/lovable/email/auth/preview.ts`): Lovable-generated scaffold, preview only. Dropped 2026-11-23.

## Done
- 2026-11-23 — **iPhone: Home Screen app already signed in** (no second code), all three apps. Needs a real-iPhone check after Publish.
- 2026-11-23 — **Email sender test → Cattamonio** (`src/test/emailSender.test.ts`, from Doggos). Now in all three apps.
- 2026-11-23 — **Camera zoom + pinch in all three apps** (user request). Birds `d380bfd` (pinch added),
  Cattamonio `0fca83b`, Doggos `4e86bfa` (zoom + slider + pinch ported).
- 2026-11-23 — **Location rule: Birds of Milan only** (user decision). Never port. Second photo for
  birds also stays Birds-only.
