# PET-A-MON keeper — backlog

## Needs decision (user)

1. **Digital camera zoom → Cattamonio + Doggos.** Built in Birds of Milan (`67a562a`): centre-crop
   zoom up to 5×, stops when the crop drops below 720 px, slider in the hunt screen.
   *Recommendation: port* — pure camera plumbing, no rule change, and the user named zoom as a
   shared concern. *Counter-argument:* cats and dogs are usually photographed up close, so the
   slider adds UI for little gain and digital zoom lowers the photo resolution the judge sees.
2. **Location requirement (geofence) → others?** Birds requires a GPS fix inside Comune di Milano,
   otherwise the bird is "released" with no points. *Recommendation: do not port* — it is
   Birds' identity (Milan). If wanted elsewhere, generalise `milano.ts` into a per-app optional
   area rather than copying.
3. **Second photo for birds** (Birds only). *Recommendation: leave Birds-only* unless the judge's
   anti-cheat in the other apps proves weak.

## Ready to port (no decision needed)

4. **`home_name` i18n key** (Birds): short home-screen/installed-app name read from i18n instead of
   the brand constant. Small, generic. Port to Cattamonio + Doggos with each app's short name.
5. **`src/test/emailSender.test.ts`** (Doggos, Birds) → Cattamonio. Test only.
6. **Email preview ROOT_DOMAIN** in Doggos uses `doggos.lovable.app` while the sender is
   `doggos.cattamonio.com`. Cosmetic (preview page only); align when next touching email code.

## Done
_(nothing yet)_
