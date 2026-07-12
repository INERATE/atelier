---
name: gateway
description: The design-truth gateway — resolves which design files are authoritative right now (core law + self-learning overlays). Run at the START of any UI/design task, before reading the design law.
---

# Gateway

The core design law is read-only; learned taste lives in overlay files pointed
to by the store. This skill tells you what to read, in order.

## Protocol

1. Query the pointers:
   `python <plugin>/db/store.py sql "SELECT path, kind FROM design_guide_versions WHERE promoted=0 ORDER BY id"`
   (no db / no rows → core law only).
2. Read in order: `skills/design-law/SKILL.md` first, then each overlay —
   later overlays override earlier ones; every overlay overrides core **except**
   the anti-style list and the token-centralization rule, which are inviolable.
3. Also load active overlay rules:
   `python <plugin>/db/store.py rules design` (rows with `source=overlay:*`).

## Rules

- Never edit core law files at runtime. New taste = new overlay file in
  `workspace/overlays/` + a `design_guide_versions` row (the learner agent's
  job, via `/atelier:learn`).
- Conflicting overlays: newest wins; note the conflict to the user.
- Promotion to core is a deliberate human act (a future
  `/atelier:promote`), never automatic.
