---
name: structure-law
description: The Atelier Structure Law — canonical, industrial-standard file structures per stack (Next.js, FastAPI, monorepo, full platform), naming rules, and the intake questions that settle layout once. Load before scaffolding or moving files.
---

# Structure Law

Every stack has ONE canonical layout. Repos never invent their own. Structure
is settled at intake and recorded in `projects` — never re-litigated per task.

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
