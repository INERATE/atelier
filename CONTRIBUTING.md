# Contributing to Atelier

Thanks for helping build the craftsman's framework. Atelier holds contributions to
the same standard it enforces on generated code — that's the whole point.

## What to contribute

| Surface | What it looks like |
|---------|--------------------|
| **Skills** | A new law or stack guide (`skills/<name>/SKILL.md`): frontmatter description ≤ 2 sentences, body teaches the *decision rules*, not tutorials. |
| **Registry MCPs** | Turn a component/asset site (e.g. a UI library) into registry rows or an MCP under `mcp/registry/` — see `skills/mcp-maker/`. |
| **Stack guides** | `skills/stack-guides/<stack>.md`: when to use it, canonical file structure, the 5 mistakes agents make with it. |
| **Deployment recipes** | Additions to `deploy-advisor`: platform, setup steps, real cost table. |
| **Hooks / tools** | Deterministic enforcement or asset tooling — must ship with a one-file self-check. |
| **Seed data** | Component metadata, design rules, command help in `db/seed/`. |

## Ground rules (the laws apply to you)

1. **Ponytail:** shortest working change. No speculative abstraction, no new
   dependency for what a few lines do, stdlib first.
2. **250-word law:** code files stay ≤ 250 words (350 hard cap). Docs are exempt.
3. **Design law:** anything user-facing (README sections, generated UI examples)
   follows `skills/design-law/` — no AI-slop.
4. **DRY:** check the graph/repo before writing; if it exists, import it.
5. **No polling, ever** — in framework code or examples.
6. **Core is read-only at runtime:** features that modify behavior go through
   workspace overlays + SQLite pointers, never by mutating core files.

## Workflow

1. Open an issue describing the change (template provided) — for small fixes, a PR
   directly is fine.
2. Fork, branch (`feat/<slug>` or `fix/<slug>`), make the change.
3. Run the self-checks: hook tests (`python hooks/<hook>.py --test`), schema check,
   markdown lint.
4. PR with: what it does, why it's the minimal version, and (for skills) one example
   of the agent behaving better with it.
5. One maintainer review + green CI merges it.

## Commit style

Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`). Keep subjects ≤ 72 chars.

## Questions

Open a discussion or an issue. Be kind — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
