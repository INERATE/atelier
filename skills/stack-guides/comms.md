# Stack Guide — Communication Protocols (REST / GraphQL / gRPC / SSE / WS / TOON)

## The decision table

| Need | Use | Never |
|------|-----|-------|
| Standard frontend↔backend API | REST `/api/v1/{feature}/{action}` | inventing RPC-over-REST |
| Frontend needs flexible queries over one endpoint (many views, one schema) | GraphQL (Strawberry/Apollo) | GraphQL "because modern" — it adds N+1 and caching complexity |
| Backend↔backend service calls (internal microservices, workers, daemons) | gRPC (HTTP/2 + protobuf — near-instant, typed) | gRPC to browsers (needs proxy; not worth it) |
| Server→client streaming (AI tokens, job progress, notifications) | SSE — one-way, auto-reconnect, plain HTTP | **polling — banned everywhere** |
| Bidirectional real-time (chat, live collab, presence) | WebSockets (or Durable Objects on CF) | SSE hacks for two-way |
| LLM-bound payloads (prompts, tool results) | TOON / pipe-rows — token-lean | raw JSON blobs in prompts |

## Rules

- Start REST. Add GraphQL only when the frontend team actually suffers from
  over/under-fetching. Add gRPC only when two backend services talk hot paths.
- Every stream must handle: reconnect (SSE `Last-Event-ID`), backpressure, and
  a clean close. Every consumer must render partial data.
- Cache invalidation beats cache expiry: on write → invalidate → push update
  (SSE/WS) so the UI refreshes without reload (see redis-celery guide).

## The 5 mistakes agents make

1. Polling for job status when SSE is one endpoint away.
2. GraphQL for a CRUD app with three views.
3. gRPC to the browser through a fragile proxy.
4. Streaming JSON strings inside JSON envelopes (double encoding).
5. No reconnect handling — one dropped connection kills the live UI.
