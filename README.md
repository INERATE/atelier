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
  choreography, centralized theme tokens (dark/light/any theme = one file, zero
  page edits), a component registry the agent picks from. The "AI-slop template
  look" is named and banned.
- **Clean-code law** — 250 words per file, enforced by a hook, not a hope.
- **Automatic model routing** — Opus plans, Sonnet builds, Haiku summarizes,
  a parallel design-scout studies premium component source while you build,
  and a learner ingests your references. You never switch models manually.
- **Token-cheap memory + framework graph** — rules, plans, and registries live
  in SQLite rows served as lean pipe-rows, and `store.py map <topic>` resolves
  which skill/tool to load in one ~30-token query instead of directory scans.
- **Battle-tested auth law** — rotating refresh tokens, families, grace windows,
  silent refresh, and the exact anti-patterns that corrupt auth.
- **Native asset pipeline** — image→webp, video→webp frames→scroll-scrubbed
  scrollytelling, and AI video generation (Gemini Omni Flash / Veo 3.1) with a
  graceful paste-prompt fallback when there's no API key.
- **Self-learning** — drop a screenshot or URL; Atelier learns it into an
  overlay without ever touching its read-only core.

## Install (Claude Code)

```
/plugin marketplace add INERATE/atelier
/plugin install atelier
```

Requirements: Python 3.10+ on PATH. Optional: ffmpeg (video frames),
Pillow (image compression), a Google AI key (media generation).

## Start (in your project folder)

```
/atelier:bootstrap    # once — probes your machine, creates workspace/atelier.db,
                      # checks companions, asks (optionally) for a Google AI key
/atelier:plan <what you want to build>
```

`plan` runs intake (paste a project doc or answer one batch of questions —
stack, layout, auth mode, hosting with real costs, your ONE brand accent),
then the Opus architect writes the architecture and a **done-state contract**
into the store. Then:

```
/atelier:build        # Sonnet executes task-by-task; refuses to "finish" with unmet criteria
/atelier:review       # ponytail + graph + lint + design + size gates, evidence recorded
/atelier:ship         # final gate: every criterion re-verified, ship report with deploy costs
```

## The flow

```
/atelier:plan ──► Understand → Clarify(one batch) → Architecture + Done-State ──► SQLite
                                                                                    │
/atelier:build ─► builder(Sonnet) task loop ─► hooks enforce laws ─► criteria pass ─┘
                     │ architectural hole? → back to architect(Opus)
/atelier:review ─► gates update evidence        /atelier:ship ─► all green → shipped
```

Sessions are disposable; state isn't — plans and criteria live in
`workspace/atelier.db`, and a session-start hook resumes the active plan after
any compaction or restart.

## All commands

| Command | Purpose |
|---------|---------|
| `/atelier:bootstrap` | One-shot setup: store, doctor, companions, credentials |
| `/atelier:plan` | Intake → architecture → done-state contract (Opus) |
| `/atelier:clarify` | Understand first, then ask only the unknowns |
| `/atelier:build` | Execute the plan through the loop engine (Sonnet) |
| `/atelier:review` | All quality gates, evidence into the contract |
| `/atelier:learn` | Teach it: screenshots, URLs, code, new skills/MCPs → overlays |
| `/atelier:promote` | Make a learned overlay permanent, git-tracked law |
| `/atelier:ship` | Final release gate + deploy plan with costs |
| `/atelier:status` / `doctor` | Progress · health checks |

## Self-learning in 30 seconds

Paste a screenshot in chat (or drop files in `workspace/references/`) →
`/atelier:learn` → the learner writes `workspace/overlays/NNN-<slug>.md` + a
pointer row. Every UI task reads core law + your overlays via the gateway.
Love it forever? `/atelier:promote` moves it into `docs/design/` (git-tracked).
Core framework files are never edited at runtime — a `git pull` can't clobber
your taste, and your taste can't corrupt the core.

## Status

Phases 0–5 landed: 13 skills (laws + principal-mind + mcp-maker + 5 stack
guides), 5 model-pinned agents (architect, builder, summarizer, learner,
design-scout), 11 commands, enforcement hooks, CI, the SQLite store with a
27-node framework map, the asset pipeline, and self-learning overlays.
Open items: the media-generation daemon (gRPC) and broader cross-runtime
adapters — see the [implementation plan](docs/IMPLEMENTATION-PLAN.md).

## Contributing

New skills, component-registry MCPs, stack guides, and deployment recipes are
the main contribution surfaces. Read [CONTRIBUTING.md](CONTRIBUTING.md) — every
contribution passes the same gates Atelier enforces on generated code.

## Maintainer

Created and maintained by **[Piyush Sharma (@ScienHAC)](https://github.com/ScienHAC)** —
built from the hard-won production patterns of [GrowthCharters](https://growthcharters.com).

## License

[MIT](LICENSE) © Piyush Sharma (ScienHAC) and Atelier contributors
