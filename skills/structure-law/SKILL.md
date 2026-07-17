---
name: structure-law
description: The Atelier Structure Law — canonical, industrial-standard file structures per stack (Next.js, FastAPI, monorepo, full platform), naming rules, and the intake questions that settle layout once. Load before scaffolding or moving files.
---

# Structure Law

Every stack has ONE canonical layout. Repos never invent their own. Structure
is settled at intake and recorded in `projects` — never re-litigated per task.

## The structure ladder (pick by project size, once)

There is no single "correct" structure — there is one correct structure **per
project size**. Climb only as far as the project demands:

| Project shape | Structure |
|---|---|
| Portfolio, practice app, tiny site | **Flat** — `src/{components,pages,assets}` |
| Medium app, small team | **Type-based** — `src/{components,hooks,services,utils,context,pages,types}` |
| Production app, SaaS, dashboards | **Feature-based** — `src/features/<name>/{components,hooks,api,pages,types,index.ts}` + `shared/ layouts/ routes/` |
| Design system / component library | **Atomic** — `components/{atoms,molecules,organisms,templates,pages}` |
| Large multi-domain SaaS / enterprise | **Domain-driven** — `src/modules/{users,orders,payments,…}` |

Rules of the ladder:

- **Feature-based is the production default.** Related files stay together;
  features ship and delete as units. Type-based scatters one feature across
  seven folders — acceptable only below ~30 components.
- **Atomic only for reusable component libraries.** In a product app it forces
  "is this a molecule or organism?" debates that produce zero user value.
- **Never scaffold a higher rung "for later"** — a flat project moves to
  feature-based when the second real feature lands, not before (ponytail).
- Each feature exports through its own `index.ts`; nothing deep-imports across
  features. But **no giant root barrels** — one `index.ts` re-exporting the
  world breaks tree-shaking and creates circular imports.
- Colocate what only one route uses (App Router: `_components/` inside the
  route). Promote to `shared/` on second use, never on first.

## Intake questions (asked once)

1. Frontend and backend: separate repos or one? *(default: one repo, separated
   apps)*
2. Multiple frontends? → Turborepo monorepo. Single app? → plain Next.js.
3. Frontend folder name: `frontend/` or product name? *(default: `apps/<name>`)*
4. Model serving / workers as separate services? *(default: yes if AI/ML or
   long jobs exist)*

## Next.js app (App Router)

```
app/            # routes; server components by default
components/     # one component per file; ui/ for primitives
hooks/          # use*.ts
lib/            # pure utils, api clients, auth
services/       # domain logic calling APIs
public/         # assets: images/ fonts/ icons/ (industry conventions)
styles/         # globals.css, tokens
```

## Turborepo monorepo (multiple frontends)

```
apps/           # app/ marketing/ studio/ admin/ … (one Next.js app each)
packages/       # ui/ auth/ config/ types/ eslint-config/
turbo.json  pnpm-workspace.yaml
```

## FastAPI backend

```
app/
  api/v1/endpoints/   # thin route handlers
  services/           # business logic, LLM/external APIs
  core/               # config, db, redis, security — no business logic
  workers/            # celery tasks
  models/  schemas/   # SQLAlchemy | Pydantic
database/schema.sql   # single source of truth
```

## Full platform (frontend + backend + ML + infra)

```
apps/{frontend…, backend-api, worker, model-serving}
packages/   docs/   infra/{docker, cloudflared}   scripts/   .github/workflows/
docker-compose.yml   .env.example   README.md
```

## Rules

- URL pattern for APIs: `/api/v1/{feature}/{action}`; keep endpoints thin,
  logic in services.
- `public/` mirrors industry conventions; docs live in `docs/`, never scattered.
- Shared code goes to `packages/`/`lib/` on second use — DRY is structural.
- Env: every var documented in `.env.example`; secrets never committed.
- New file? It has exactly one obvious home in the trees above. If it doesn't,
  the task is misdesigned — stop and fix the plan.
