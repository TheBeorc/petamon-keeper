# PET-A-MON — what is shared and what is not

Baseline measured on 2026-11-23 (cattamonio `3d053c6`, doggos `baa29f3`, birdsofmilan `3d05fcf`):
of ~290 files, **160 are byte-identical** in all three apps; most of the rest differ only in theme.
Re-measure any time with `python3 scripts/keeper.py drift`.

## Stack (identical in all three)
TanStack Start (React 19, SSR on Cloudflare Worker), Tailwind 4, TanStack Query, Lovable Cloud
(Supabase: Postgres + Auth + Storage). Server functions in `src/fn/` → logic in `src/server/`.
Vision judge: Anthropic direct (`claude-haiku-5-5`) by default, Lovable gateway optional, mock for
tests. SQL lives in `doc/sql/` and is applied by Lovable verbatim (`doc/LOVABLE_STEPS.md`).
Full description: each app's `doc/ARCHITECTURE.md` (Cattamonio's is the reference).

## Layers

| Layer | Paths | Rule when porting |
| --- | --- | --- |
| **Core** (same logic everywhere) | `src/app/` (camera, store, data, api), `src/fn/`, `src/server/core/`, `src/server/lib/` (except `prompts.ts`), `src/game/{scoring,time,otp,invites}.ts`, `src/components/k/*` (Auth/OTP login, Hunt, Invite, Frame, Onboarding, PlayerAvatar, AvatarUploader), `src/routes/*` (except themed pages), `scripts/` | Port as-is after `translate`; tests must pass |
| **Themed** (same structure, different words/colours) | `src/i18n/{it,en}.ts`, `src/styles/catamon.css`, `src/server/lib/prompts.ts`, `src/game/vision-schema.ts` (subject enum), `src/lib/email-templates/*`, `src/routes/{privacy,regole}.tsx`, `doc/`, tests | Port logic/keys; rewrite copy and colours per app |
| **App-specific** (identity) | `src/game/catalog.ts` (+ seed SQL), `src/components/cat/{art,fantasy}.ts`, `public/` icons, community route `/colonia` `/branco` `/stormo`, claims, palette values, `src/game/milano.ts` (Birds only) | Never copy |
| **Lovable-managed** | `supabase/migrations/`, `drizzle/`, `src/integrations/supabase/*`, `src/routeTree.gen.ts`, `.lovable/`, `.env`, email domain setup, secrets | Never by hand → Lovable `send_message` |

## Theme per app

| | Cattamonio | Doggos | Birds of Milan |
| --- | --- | --- | --- |
| Claim | A caccia di mici | Mi Fido di te / In Dog We Trust | Tel chì el piccion! |
| Animal (it) | il gatto / i gatti | il cane / i cani | l'uccello / gli uccelli |
| Action in UI | cattura | cattura | avvistamento |
| Community page | `/colonia` | `/branco` | `/stormo` |
| Temp nickname | `micio-xxxxx` | `fido-xxxxx` | `pulcino-xxxxx` |
| Email domain | cattamonio.com | doggos.cattamonio.com | birdsofmilan.cattamonio.com |
| Palette | rosa / lavanda | arancio / marrone | grigio nebbia / blu Navigli |
| Catalog | 23 species (mantelli/razze + volpe bonus) | 20 razze + taglie dei meticci | 25 uccelli del Comune di Milano + fenicottero bonus |

## Known divergences in core code (baseline)

- **Birds only**: digital zoom on the camera (`src/app/camera.ts` `centerCrop`/`digitalZoomMax`,
  zoom slider in `Hunt.tsx`, CSS `.cam-zoom`), mandatory location inside Comune di Milano
  (`src/game/milano.ts`, `released` result in `capture.ts` / `types/app.ts`), second photo for birds,
  short home-screen name via i18n key `home_name` (`store.tsx`, `Onboarding.tsx`).
- **Doggos + Birds, not Cattamonio**: `src/test/emailSender.test.ts`.
- **Cosmetic**: `src/routes/lovable/email/auth/preview.ts` ROOT_DOMAIN uses the custom domain in
  Cattamonio/Birds but `doggos.lovable.app` in Doggos; canonical/og URLs: Cattamonio/Doggos use
  `*.lovable.app`, Birds uses its custom domain.

These are tracked as decisions in `BACKLOG.md`.
