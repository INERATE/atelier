---
name: auth-law
description: The Atelier Auth Law — production-hardened session architecture (rotating refresh tokens, families, grace window, silent refresh, sliding window) plus the anti-patterns that corrupt auth. Load before designing or touching ANY authentication code.
---

# Auth Law

Distilled from a production system that was broken repeatedly by well-meaning
"improvements" and then hardened. If you are about to "improve" auth, your
improvement is probably in the anti-pattern list. A genuinely logged-in user
must NEVER be bounced to login by normal use.

## The six guarantees

1. No unexpected bounce to login — ever, on any click or cross-app navigation.
2. Token expiry is invisible: new access tokens issue **silently**.
3. **No polling.** One-shot self-rescheduling timer + on-demand refresh only.
4. Auth-layer-first: silent refresh → session check → only then redirect.
5. Long sessions survive: multi-hour live streams / videos never drop.
6. Sliding window: any visit within 30 days extends 30 days; only true
   inactivity forces re-login.

## Token model

| Thing | Lifetime | Storage |
|-------|----------|---------|
| Access JWT | 15 min | JS-readable cookie; `Authorization: Bearer` |
| Refresh token | 30 days, **single-use, rotates** | HttpOnly cookie + SHA-256 hash in DB |
| Session | 30 days | DB row (truth) + cache |
| expires_at / user cookies | 30 days | JS-readable (schedule timer / routing); not credentials |

Cookie domain `.yourdomain.com` when multiple subdomains share one session
(central "accounts.\*" auth, Google-style) — chosen at intake vs per-app auth.

## Rotation, families, grace

Every refresh consumes the token and issues a new one. All tokens from one
login share a `token_family_id`. A rotated-away token presented **outside** the
**60-second grace window** = assumed theft → revoke the family. Inside the
window → return the already-issued successor (absorbs tab races). The grace
window is load-bearing; the single-flight mutex is the real fix.

**Golden rule: ONE refresh in flight per app.** Every trigger (one-shot timer
~2min before expiry, 401 recovery, tab focus, layout mount) funnels through a
single module-level in-flight promise/mutex.

## Login flows (all end in the SAME token issuance)

Password (+ optional TOTP 2FA before tokens) · OAuth via state-cookie + JSON
callback into `user_identities` · Passkeys/WebAuthn in `user_passkeys` ·
Turnstile/captcha on public forms. Never a parallel session mechanism.
Every login/refresh writes an activity log (device, IP) — Google-style
auditable sessions; owner console can list + revoke sessions per user.

## Anti-patterns (each one has actually corrupted production auth)

1. ❌ Interval-based refresh polling.
2. ❌ A second refresh caller outside the mutex.
3. ❌ Two AuthProviders mounted on one route (nested layouts = passthroughs).
4. ❌ Zustand/Redux/etc. for auth state — cookies + one AuthContext per app.
5. ❌ Redirect to /login on missing access token before silent refresh + session check.
6. ❌ Skipping refresh because JS cookies are gone (HttpOnly may still be valid).
7. ❌ Family revocation broadened to "revoke all".
8. ❌ Shrinking the grace window to "harden" security.
9. ❌ Casually changing token lifetimes.

## Shipping checklist

- [ ] No polling; no unmutexed refresh; one provider per app
- [ ] Redirect is the LAST branch; typecheck all affected apps
- [ ] OAuth/passkey/2FA terminate in the same issuance
- [ ] All four sliding-window scenarios verified
- [ ] Sessions auditable + revocable from the console
