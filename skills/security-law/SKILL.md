---
name: security-law
description: The Atelier Security Law — OWASP-grade defense for every request path (injection, XSS, CSRF, tenant isolation, rate limiting, transport). Load before writing ANY endpoint, form, or data-processing code — not just auth. Auth token/session mechanics live in [[auth-law]]; this is everything else.
---

# Security Law

Assume every request is hostile until proven otherwise. Client-sent data is
never trusted, including things that "should" be safe (an org id, a role, a
price) — trust only what the server derives from the verified session.

## 1. Injection

- **SQL/NoSQL: parameterized queries / ORM only.** Never string-concat or
  f-string a query. No exceptions for "internal" or "admin" endpoints.
- Shell/command execution: never pass user input to a shell; use argument
  arrays, never `shell=True` / string-built commands.

## 2. XSS

- Never `dangerouslySetInnerHTML` (or equivalent) on untrusted content —
  user text, imported files (Excel/CSV), rendered markdown. Sanitize
  server-side (allowlist tags/attrs) before it's ever stored or rendered.
- Set a CSP header; no inline `<script>` from user data.
- React/Vue/etc. auto-escaping is the default path — don't opt out of it to
  "fix" a rendering quirk.

## 3. CSRF & cookie theft

- Session cookies: `HttpOnly` + `Secure` + `SameSite=Lax/Strict` (see
  [[auth-law]] for the token model itself).
- **No state change on GET.** Mutations only via POST/PUT/PATCH/DELETE with
  the session cookie + (for cookie-authed browser clients) a CSRF token or
  origin check.

## 4. Transport & replay

- HTTPS + HSTS everywhere; no mixed content.
- Short-lived access tokens, single-use rotating refresh (already specified
  in [[auth-law]]) — this is what makes a captured token worthless within
  minutes even without CSRF.

## 5. Tenant isolation (the worst bug class)

- `organization_id` / `tenant_id` used in ANY query comes from the verified
  JWT/session server-side — **never from the request body, query string, or
  a client-supplied header.** A user editing a JSON payload must not be able
  to touch another tenant's row.
- Every list/detail/mutation endpoint filters by the session's tenant AND
  checks resource ownership — "authenticated" is not "authorized."
- Test this class explicitly: user A's token against user B's resource ID
  must 403/404, never 200.

## 6. Abuse & brute force

- Rate-limit login, 2FA verify, password reset, and any public form (Redis
  `SETNX`+expiry, see [[stack-guides/redis-celery]]). Lock/backoff after N
  failures per account AND per IP.
- Turnstile/CAPTCHA on public unauthenticated forms (signup, contact, reset).
- Generic errors outward ("invalid credentials"), detailed errors only in
  server logs — never leak which field was wrong, or stack traces, to the
  client.

## 7. Validation at trust boundaries

- Validate/normalize on the server regardless of client-side validation —
  Zod on the frontend is UX, not security; the backend schema (Pydantic/etc.)
  is the actual gate.
- File uploads: validate type/size server-side by content, not extension;
  store outside the webroot; serve through a handler, not direct static path.

## Shipping checklist

- [ ] No string-built queries anywhere in the diff
- [ ] No `dangerouslySetInnerHTML`/raw-HTML render on user-sourced content
- [ ] Every mutating endpoint requires non-GET + authz check on the resource
- [ ] Every tenant-scoped query derives `organization_id` from the session, never the payload
- [ ] Public forms rate-limited + Turnstile; login/2FA rate-limited per account+IP
- [ ] Server-side validation exists independent of client-side validation
