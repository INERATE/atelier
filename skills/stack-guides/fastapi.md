# Stack Guide — FastAPI (Python backends & AI services)

## When to use
REST/GraphQL APIs, AI/LLM services (uvicorn + async), anything Python-native
(ML, embeddings, document processing).

## Decision rules
- **Async everywhere**: AsyncSession + asyncpg; never sync SQLAlchemy in routes.
- Layers per structure-law: thin `endpoints/` → logic in `services/` →
  infrastructure in `core/`. DI via `Depends()`.
- Pydantic v2 schemas for every request/response. `uv` for packages, not pip.
- Long jobs (parsing, scoring, emails) → Celery + Redis queue; API returns
  immediately, frontend gets progress via **SSE — not polling**.
- Caching: Redis with explicit invalidation on write (edit/delete → cache
  update → UI reflects live). Cache keys documented next to the service.
- LLM calls: model-router pattern (primary → fallback), token/cost logging per
  call, retry ONLY transient errors (429/5xx) — 4xx fails fast to the fallback.
- **GraphQL** (Strawberry) only when the frontend genuinely needs one flexible
  endpoint; **gRPC** for backend↔backend service calls; REST otherwise.
- RAG: hybrid retrieval (BM25 + pgvector) → cross-encoder re-rank → parent
  context expansion; PageIndex/hierarchical for dense documents.
- `database/schema.sql` is the single source of truth; every model change
  updates it AND migrates the live DB.

## The 5 mistakes agents make
1. Business logic in endpoint handlers instead of services.
2. Sync DB calls (or `requests`) inside async routes — blocking the loop.
3. Frontend polling for job status instead of SSE.
4. Exponential-backoff retries on 404/400 — burn minutes, mask real bugs.
5. Editing models without updating schema.sql + the live database.
