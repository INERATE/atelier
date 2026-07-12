# Stack Guide — Redis Caching & Celery Jobs

## Caching (Redis)

- **Pattern: cache-aside.** Read: try cache → miss → DB → set with TTL.
  Write: update DB → **invalidate the key immediately** → (optionally) push
  the fresh value over SSE/WS so every client updates without refresh.
- Key design: `{entity}:{id}:{view}` (e.g. `user:42:profile`). Document keys
  next to the service that owns them. One owner per key family.
- TTLs are a safety net, not the strategy: short (60–300s) for hot lists,
  invalidation for anything a user edits. Never cache auth decisions.
- Rate limiting and locks also live in Redis (`SETNX` + expiry) — reuse the
  same instance; don't add infra.

## Background jobs (Celery + Redis broker)

- Anything >1s of work (parsing, scoring, emails, media) goes to a worker.
  The API enqueues, returns `202` + job id instantly; progress streams to the
  client via **SSE — never polled**.
- **Tasks must be idempotent** (safe to retry) and small; chain steps instead
  of one mega-task. Retry only transient failures (429/5xx) with backoff;
  4xx fails fast to a dead-letter state a human can inspect.
- Calling async code from sync Celery: one `asyncio.run()` bridge at the task
  boundary — never nest event loops. Do not "refactor away" this bridge.
- Log per task: duration, retries, cost (if LLM). Every queue needs a depth
  alarm — a silent backlog is an outage.

## The 5 mistakes agents make

1. Caching without invalidation — stale UI, users refresh in vain.
2. Long work in the request handler because "it's only a few seconds".
3. Non-idempotent tasks + retries = double emails / double charges.
4. Two sources of truth (cache written before DB commit).
5. Celery for sub-second work — the queue round-trip costs more than the job.
