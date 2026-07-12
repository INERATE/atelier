# Atelier — Requirements Specification

> **Atelier** (n.) — a workshop or studio of a master craftsman.
>
> This document is the clean, complete, structured version of the founder's original
> statement of need (`Statement/need.md`). It states **what Atelier is, why it exists,
> what it must do, and what "done" means for it** — written so that any contributor,
> with no prior context, can understand the whole vision.

---

## 1. The Problem

Modern LLMs (Claude, Gemini, GPT) can write any code — they were trained on it. They do
not fail because they *can't* code. They fail because:

1. **They don't know what "done" means.** Without an explicit, checkable done-state,
   agents drift, over-build, under-build, or loop forever.
2. **They don't know what "good" looks like.** Left alone, they produce the
   "AI-slop" look: rainbow gradients, purple-pink blobs, bouncy animations, generic
   template layouts — and code spread across bloated thousand-line files with no
   structure a human can navigate.
3. **They waste tokens.** Re-reading giant markdown files every turn, re-deriving
   plans, using the most expensive model for trivial edits.
4. **They ask questions at the wrong time.** Either they interrogate the user before
   reading anything, or they never ask and guess wrong.
5. **They forget.** Design decisions, project rules, and learned references evaporate
   between sessions unless something persists them.

The senior engineers at Google/Microsoft/Apple who used to provide judgment — taste,
architecture, stopping conditions — are exactly what the LLM is missing. **Atelier is
that senior engineer, packaged as an installable framework.**

## 2. What Atelier Is

Atelier is an **open-source, installable engineering framework for AI coding agents**
(Claude Code first; portable to Cursor, Gemini CLI, Codex, Aider later).

It is **not** a single skill, not a single MCP server, and not a prompt pack. It is a
**plugin** — the distribution container that bundles:

| Layer | Role in Atelier |
|-------|-----------------|
| **Skills** | Procedural knowledge, model-invoked: design law, clean-code law, file-structure law, auth law, stack guides. Cheap descriptions always in context; full body loaded only when relevant. |
| **Hooks** | Deterministic enforcement, runs regardless of what the model "decides": file-size gate, design-token lint, asset auto-compression, graph re-index. |
| **MCP servers** | External tools/data: component registries (shadcn, Aceternity, ReactBits, Motion.dev, MagicUI), code-review-graph, asset pipeline, the Atelier SQLite store. |
| **Subagents** | Isolated workers pinned to a model tier — the auto model router (see §6). |
| **Commands** | The user surface: `/atelier:bootstrap`, `/atelier:plan`, `/atelier:build`, `/atelier:learn`, … (see §13). |
| **SQLite store** | Fast, token-cheap structured memory: rules, registries, plans, done-states, learning events (see §7). |

**Hybrid model:** Atelier ships its own laws (design, clean code, structure, auth) AND
installs curated third-party power-ups (ponytail, code-review-graph, ui-ux-pro-max,
stitch, shadcn MCP, aceternity MCP, react-bits MCP, …) so one install gives the agent
the complete toolkit.

## 3. Who It's For

- **Non-expert builders** — most users won't know deep coding. Atelier assumes this:
  the agent must carry the engineering judgment so the user never has to.
- **Serious builders / founders** — people shipping real products (the founder's own
  GrowthCharters is the reference customer) who need industrial-grade output, not demos.
- **Contributors** — Atelier is open source; anyone can add skills, MCPs, registries,
  and stack guides through a documented contribution path.

## 4. Core Principle: Loop Engineering with Base Cases

Every task runs a strict loop with a **mathematical stopping condition** — like
recursion (`if (done) return;`):

```
Understand → Clarify → Plan → Execute → Review → Compare vs Done-State
     ▲                                                    │
     └────────────── still missing? loop ─────────────────┘
                              done? STOP
```

- **Understand first, ask second.** The agent reads the repo, docs, CLAUDE.md, the
  Atelier store, and the web (if needed) BEFORE asking anything. It generates
  assumptions and unknowns, then asks **only the unknowns** — batched, once,
  high-impact. Clarification is precious; it is never the first move and never skipped
  when a project-defining ambiguity exists.
- **Done-state contracts.** Planning produces an explicit checklist written to the
  store (e.g., "hero exists ✓, responsive ✓, a11y ✓, perf > 95 ✓, design law
  followed ✓, tests pass ✓"). The loop terminates **only** when every criterion
  passes. "When the user said these done" is a valid criterion.
- **Review is a gate, not a suggestion.** Ponytail (efficiency), code-review-graph
  (structural impact), lint, design-token compliance, and the file-size law all run
  before "done" can be claimed.

## 5. Project Intake (how every project starts)

1. On first run in a repo, Atelier asks the user to either **paste a detailed project
   md** or answer intake questions; from the answers it writes `project.md` — the
   prototype document: what the project is, features, goals, users, constraints —
   exactly what a product manager writes before execution.
2. The agent must understand **what kind of surface** it's building. Example: a
   *landing page* is marketing for a service that may not exist yet — the agent must
   know the product story before designing it. Never build before this is clear.
3. Intake also settles the structural questions once: separate frontend/backend repos
   or one? monorepo (Turborepo) or single app? which stack? Defaults are the
   industrial standard; the user can override.
4. Auth intake: does the product need **central auth across services (Google-style
   accounts.* gateway)** or per-app auth? Turnstile/captcha? OAuth providers?
   (Answers feed the Auth Law, §10.)
5. Hosting intake: Atelier knows the deployment landscape — Cloudflare Pages/Workers,
   Vercel, Google Cloud Run, Hostinger/Oracle-free-tier/AWS EC2/ECS-Fargate VPS,
   Cloudflare Tunnel for home-hosted backends — and **explains cost** for each option
   before the user chooses.

## 6. Model Routing (the engineering org chart)

Atelier treats model tiers like an engineering team, and routes automatically so the
user never manually switches models:

| Model | Role | Does |
|-------|------|------|
| **Opus** | Principal engineer / product manager | Planning, architecture, done-state definition, final verification. **Never writes granular code.** |
| **Sonnet** | Senior developer | Executes the plan: builds features, refactors, writes tests. The workhorse. |
| **Haiku** | Junior / summarizer | Summaries, log digests, memory updates, trivial edits, exploration. |

- Routing is implemented with **subagents pinned to a model in frontmatter** — the
  documented, supported mechanism — not by mutating the main session's model.
- **Opus plans → Sonnet executes** is the law. The reverse (Sonnet plans, Opus codes)
  wastes the expensive tokens on the cheap half of the job and is forbidden.
- Complexity-based escalation: minor fix → Haiku/Sonnet directly; architecture or
  ambiguous tradeoff → Opus. Parallel subagents for independent small tasks.
- Deep-work moments (design, planning) run at max effort / ultrathink; sessions are
  compacted into persistent memory rather than allowed to bloat.

## 7. Knowledge & Memory Layer (token efficiency by design)

**No single storage for everything.** Each memory type gets the medium it's fastest in:

| Store | Holds | Why |
|-------|-------|-----|
| **SQLite (`atelier.db`)** | Rules, registries (components/MCPs/tools), plans, done-state checklists, clarification log, learning events, design-guide version pointers, install manifest | Structured, queryable, changes often. The agent fetches **one row**, not a whole file → massive token savings vs re-reading .md every turn. |
| **Markdown** | The laws (design, clean code, structure, auth), stack guides, project.md | Long-form, human-editable, git-tracked; skills' discovery layer. |
| **Filesystem** | Templates, snippets, reference images/videos, generated frames/webp | Binary/bulky assets. |
| **Vector DB** | NOT used by default | We have well-defined instruction sets, not a 10,000-page corpus. Vectorless first. |

- **TOON** (token-oriented object notation, github.com/toon-format/toon) is the
  serialization format for LLM-bound payloads — cheaper than JSON in prompts.
- **gRPC** is used for internal service-to-service communication (CLI ↔ asset
  pipeline workers, background agents) — HTTP/2 + protobuf, near-instant, never for
  LLM prompts.
- **code-review-graph** gives the agent whole-repo structural awareness (callers,
  impact radius, tests-for) — cheaper and more accurate than grepping, and the
  backbone of safe migrations.
- **RAG, when a project needs it**, follows the reference pipeline: hybrid retrieval
  (BM25 + vector, pgvector/Elasticsearch) → cross-encoder re-rank (BGE-Reranker) →
  structural metadata routing (parent-child trees) → generation. For dense documents,
  **vectorless / hierarchical RAG (PageIndex)** is the high-accuracy option.

## 8. Design Law (the anti-AI-slop system)

Atelier ships a **generalized design law** — evolved from GC Design Language v1 — so
every user gets premium, industrial-grade UI, not template output:

- **Named vocabulary:** Apple HIG clarity/deference/depth · editorial minimalism /
  Swiss typographic style · glassmorphism for chrome only · enterprise motion
  choreography · micro-interactions · scrollytelling · quiet depth. Exemplars:
  Linear, Vercel, Stripe, Apple, Cloudflare.
- **The anti-style is named** so agents avoid it: rainbow gradient heroes, glossy 3D
  emoji icons, 8-hue icon backgrounds, bounce-in animations, centered feature-grid
  walls. **Never.**
- **Tokens, not vibes:** color/radius/spacing/easing/duration all named values;
  accent budget ≤10% of viewport; hairline borders; 4-based spacing scale.
- **Motion system:** ease-out-expo entrances, springs for interaction, 60–80ms
  staggers, scrub narrative (GSAP ScrollTrigger + Lenis) / trigger UI (Framer
  Motion), one hero moment per page, `prefers-reduced-motion` fallbacks,
  transform/opacity only.
- **Iconography:** Lucide 1.5px monochrome (SF-Symbols discipline); Google Fonts;
  custom SVG on-grid when a glyph is missing; Rive/Lottie for animated moments.
- **Component registry, not hallucination:** MCPs expose what's actually available —
  shadcn/ui, Aceternity, ReactBits, Motion.dev, MagicUI, Radix — with metadata
  (dark-mode, animated, a11y, SSR, deps, license). The agent picks from the registry
  and may adapt components to the use case; it never invents fake ones.
- **Storytelling sites:** parallax + scrollytelling pattern with the native asset
  pipeline (§11): mp4 → frames → webp → canvas scroll-scrub. If the user has no
  video, the agent writes a prompt for a generator (e.g. Omni) and processes the
  result through the same pipeline.
- The design law is **self-learning** (§12): owners and users extend it with their
  own references without forking the core.

## 9. Clean Code & Structure Law

- **250-word limit per file** (soft ceiling 350 when splitting would harm cohesion).
  Enforced by a hook — the write fails with guidance, not a hope the model remembers.
  Small files = readable, reviewable, composable, and cheap for agents to load.
- **DRY as law:** shared logic is extracted and imported, never rewritten. The
  code-review-graph makes duplication visible.
- **Ponytail principles built in:** YAGNI, stdlib first, native platform features
  before dependencies, shortest working diff, no speculative abstraction.
- **Comments:** only where they earn their place — premium, sparse, intent-revealing.
- **Canonical file structure per stack** — industry layouts, better than the average
  Google repo, so any developer can navigate without madness:
  - Next.js: `app/ components/ hooks/ lib/ services/ public/` (+ Turborepo `apps/`,
    `packages/` for monorepos)
  - FastAPI: `endpoints/ services/ core/ workers/ models/ schemas/`
  - Full platform: `apps/{frontend,backend,worker,model-serving} packages/ docs/
    infra/ scripts/ .github/`
- `public/` follows industry asset/docs conventions. Frontend folder naming (e.g.
  `frontend/` vs app-name) is confirmed at intake with an industrial default.

## 10. Auth Law (the crown jewel skill)

Auth is where projects die and founders cry. Atelier ships auth as a **first-class
skill** distilled from a hard-won production architecture (GrowthCharters
`auth-architecture.md`), made fully dynamic and configurable:

- **Token model:** 15-min access JWT + 30-day rotating single-use refresh tokens,
  token families, **60s rotation grace window**, sliding 30-day window (daily users
  never re-login; only >30-day inactivity forces login).
- **Silent refresh, never polling:** one-shot self-rescheduling timer ~2min before
  expiry + on-demand refresh; ALL refresh triggers funnel through a single mutex per
  app. Redirect to login is the LAST resort after silent refresh + session check.
- **The anti-pattern list ships with the skill** — interval pollers, second
  unmutexed refresh callers, double AuthProviders, state libraries for auth,
  redirect-on-missing-token, grace-window "hardening" — because these exact bugs are
  what corrupt auth when a well-meaning agent "improves" it.
- **Multi-service central auth (Google-style)** or per-app auth — chosen at intake.
  Cookie domain strategy, OAuth (state-cookie + JSON callback), passkeys/WebAuthn,
  TOTP 2FA, Turnstile/captcha — all terminate in the SAME token issuance path.
- **Session integrity guarantees:** long live-streams/videos never drop; genuinely
  logged-in users are never bounced; every login/refresh is auditable (activity log)
  like Google's "logged in from new device".
- The skill includes the **console/admin surface** requirements: the owner can see
  and revoke sessions, view auth events, and control providers dynamically.

## 11. Native Asset Pipeline (built-in tools)

Bundled tools (invoked by hooks/commands, run as gRPC workers):

- **Image:** png/jpg/anything → **webp**, compression, responsive size sets, cache
  manifest.
- **Video:** mp4 → frames → webp sequence → canvas scroll-scrub scaffold (the
  storytelling primitive). Audio compression likewise.
- **Caching guidance baked into stack guides:** Redis caching, Celery workers,
  cache invalidation on write (edit/delete → cache update → UI updates live),
  **SSE/WebSockets, never polling**, GraphQL only when the frontend truly needs a
  single flexible endpoint, gRPC for backend↔backend.

## 12. Self-Learning Engine

Atelier improves without breaking itself. **Core is read-only; workspace overlays
merge at runtime:**

- **Owner flow:** drop reference images/videos into the watched folder (or paste
  into chat) → agent files them, analyzes them, and writes a **new overlay design
  file** + a pointer row in SQLite (`design_guide_versions`). The git-tracked core
  law is never overwritten — so a `git pull` never clobbers learned taste.
- **Gateway:** a tiny skill reads the current pointer rows and tells the agent which
  files are authoritative right now (core law + N overlays, in order).
- **Promotion:** a deliberate command merges overlay deltas into the tracked law
  when the owner decides they're permanent. Two speeds: fast un-tracked iteration,
  deliberate promotion to law.
- **User flow:** `/atelier:learn` ingests anything — screenshots, code, CodePens,
  repos, new skills/MCPs people publish, and **URLs** (the agent scrapes the site,
  understands the offering — icon packs, 3D assets, component libraries — and writes
  a skill/registry row for how to install and use it).
- Self-learning agents **never edit core files accidentally** — the overlay
  architecture makes wrong edits structurally impossible, not just discouraged.

## 13. Command Surface

| Command | Does |
|---------|------|
| `/atelier:bootstrap` | One-shot install: creates `atelier.db`, seeds rules/registries, installs bundled + third-party skills/MCPs, runs the environment doctor, asks for API keys it actually needs. The user runs ONE command; the agent does the rest. |
| `/atelier:doctor` | Verifies deps (Node, Python, Docker, git), keys, MCP health, graph freshness. |
| `/atelier:plan` | Opus intake → project.md → architecture → milestones → done-state contract written to the store. |
| `/atelier:clarify` | Runs the understand-first protocol; asks only the remaining unknowns, batched. |
| `/atelier:build` | Sonnet executes the current plan through the loop engine. |
| `/atelier:review` | Ponytail + graph + lint + design-token + file-size + a11y/perf gates. |
| `/atelier:learn` | Ingest references (images/video/URLs/code/skills/MCPs) into the self-learning overlay. |
| `/atelier:ship` | Final release checklist vs the done-state contract. |
| `/atelier:status` | Current phase, active agent/model, progress, remaining criteria. |
| `/atelier:update` | Update the framework, skills, MCP definitions, registries. |

(Native `/plugin install` and `/reload-plugins` are used, not reinvented. Naming
avoids colliding with built-ins.)

## 14. Capability Negotiation

Before planning, Atelier detects what's actually available — which models (is Opus
accessible?), which MCPs are installed, whether Docker is running, which API keys
exist — and adapts the workflow instead of assuming. This keeps it portable across
Claude Code, Cursor, Gemini CLI, Codex, and future runtimes.

## 15. Open Source Requirements

- **Repo:** `atelier` — premium name, premium README (following our own design/writing
  standards), LICENSE (MIT), CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates,
  marketplace.json for `/plugin install`.
- **Contribution surface:** new skills, new MCP registries (a site's components/assets
  → an MCP), new stack guides, new deployment recipes. Every contribution passes the
  same review gates the framework enforces on user code (ponytail + 250-word law +
  design law for any UI).
- **MCP maker:** a documented path (and eventually a command) to turn a component
  site (like Aceternity, ReactBits) into a registry MCP or skill others can install.

## 16. Non-Goals

- Not a hosted service; local-first.
- No vector database by default.
- No interval polling anywhere — in framework internals or in generated code.
- Not tied to one project (GrowthCharters is the reference, not the scope) — the
  framework is universal.

## 17. Done-State for Atelier v1 (our own contract)

- [ ] `/atelier:bootstrap` takes a fresh machine to fully-armed in one command.
- [ ] Laws ship as skills: design, clean-code (250-word hook ENFORCED), structure, auth.
- [ ] SQLite store with seeded schema; agent reads rules by row, not by file.
- [ ] Model routing via pinned subagents: Opus plans, Sonnet builds, Haiku summarizes.
- [ ] Loop engine: every `/atelier:build` runs against a written done-state contract.
- [ ] Component registry MCP answers "what can I use?" for shadcn/Aceternity/ReactBits/Motion.dev.
- [ ] Asset pipeline: image→webp and video→frames→webp work end-to-end.
- [ ] Self-learning overlay: `/atelier:learn` an image → overlay file + pointer row, core untouched.
- [ ] Open-source scaffolding complete: README, CONTRIBUTING, LICENSE, templates, marketplace.
