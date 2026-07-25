# Stack Guide — Scale Patterns (large lists, search, loading)

For a "console"/admin table over a large dataset (thousands–millions of rows).

## Loading state

Skeleton **per loadable container**, not one page-level spinner — each card/
panel/table shows its own skeleton the instant its request fires, so fast
sections render while slow ones are still loading. Never gate the whole page
behind the slowest fetch.

## List rendering: pagination vs infinite scroll

Offer both as a user toggle, not a fixed choice — persist the pick per view:

- **Pagination**: numbered pages (`1 2 3 … 10` or `1 … 41 42 43 … 1000`),
  server returns one page (`LIMIT/OFFSET` or keyset) per request. Better for
  tabular data users need to jump around or cite a row position in.
- **Infinite scroll**: fetch next chunk on reaching a scroll sentinel
  (IntersectionObserver), append rows. Better for feeds. Never actually
  "infinite" — same page-size chunks as pagination, just auto-triggered.
- Both hit the identical paginated endpoint; the toggle only changes how the
  client requests the next chunk. Don't build two backends.

## Type-ahead search at scale

- Debounce ~250ms; cancel the in-flight request on each keystroke (AbortController).
- Query an **indexed column** (`ILIKE` + trigram/GIN index, or a search
  engine) — never a full table scan per keystroke.
- Cache hot results in Redis (cache-aside, see [[stack-guides/redis-celery]]).
- **Rank by relevance to the viewer, not just match**: results from the
  user's own org/team/connections first, then global matches — mirror how
  LinkedIn ranks 1st-degree connections above strangers for the same query.
  Do this with a `ORDER BY (tenant_id = $viewer_tenant) DESC, rank` clause or
  a boosted search-engine query, not a second round-trip.

## N+1 at the API layer

GraphQL (or any nested-resource REST response) → **DataLoader/batch pattern**
for every relation, or the "list of orgs, each with a member count" query
becomes N+1 database round-trips. Batch + cache per-request.

## The 4 mistakes agents make

1. One full-page spinner instead of per-container skeletons.
2. Search box firing a request per keystroke with no debounce/cancel.
3. `LIKE '%term%'` (leading wildcard) on an unindexed column — always a scan.
4. Nested GraphQL resolvers each doing their own query — no batching.
