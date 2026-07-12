<div align="center">

# Atelier

**The craftsman's framework for AI-built software.**

*One install turns your coding agent into a principal engineer — with taste.*

[Requirements](docs/REQUIREMENTS.md) · [Architecture](docs/IMPLEMENTATION-PLAN.md) · [Contributing](CONTRIBUTING.md)

</div>

---

LLMs don't fail because they can't code. They fail because they don't know what
**done** means, what **good** looks like, and when to **stop**. Atelier fixes all
three:

- **Loop engineering with base cases** — every task runs against a written
  done-state contract and may not claim success until every criterion passes.
- **Design law, not vibes** — Apple-HIG editorial minimalism, enterprise motion
  choreography, named tokens, a component registry the agent picks from. The
  "AI-slop template look" is named and banned.
- **Clean-code law** — 250 words per file, enforced by a hook, not a hope. DRY,
  YAGNI, stdlib-first (ponytail built in).
- **Automatic model routing** — Opus plans like a principal engineer, Sonnet builds
  like a senior dev, Haiku summarizes. You never switch models manually.
- **Token-cheap memory** — rules and plans live in SQLite rows (served as TOON, not
  JSON), whole-repo awareness via code-review-graph, laws as progressive-disclosure
  skills.
- **Battle-tested auth law** — rotating refresh tokens, families, grace windows,
  silent refresh, and the exact anti-patterns that corrupt auth, shipped as a skill.
- **Self-learning** — drop a screenshot, a URL, or a repo; Atelier learns it into an
  overlay without ever touching its read-only core.

## Install

```
/plugin marketplace add <this-repo>
/plugin install atelier
/atelier:bootstrap
```

Bootstrap probes your environment, creates the workspace + SQLite store, installs
the curated companion skills/MCPs, and asks only for what it actually needs.

## Commands

| Command | Purpose |
|---------|---------|
| `/atelier:bootstrap` | One-shot setup of everything |
| `/atelier:plan` | Opus intake → architecture → done-state contract |
| `/atelier:clarify` | Understand first, then ask only the unknowns |
| `/atelier:build` | Sonnet executes the plan through the loop engine |
| `/atelier:review` | Ponytail + graph + lint + design + size gates |
| `/atelier:learn` | Teach it: images, URLs, code, new skills/MCPs |
| `/atelier:doctor` / `status` / `ship` / `update` | Health, progress, release, upgrades |

## Status

Phases 0–2 core landed: the five law skills (loop-engine, design-law,
clean-code-law, structure-law, auth-law) + deploy-advisor + gateway, model-pinned
agents (architect/Opus, builder/Sonnet, summarizer/Haiku), 8 commands, the
enforcement hooks (250-word gate, session-start plan resume), and the SQLite
store with seeded rules + component registry. Next: registry & asset-pipeline
MCPs (Phase 3), self-learning `/atelier:learn` (Phase 4) — see the
[implementation plan](docs/IMPLEMENTATION-PLAN.md).

## Contributing

New skills, component-registry MCPs, stack guides, and deployment recipes are the
main contribution surfaces. Read [CONTRIBUTING.md](CONTRIBUTING.md) — every
contribution passes the same gates Atelier enforces on generated code.

## License

[MIT](LICENSE)
