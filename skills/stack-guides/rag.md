# Stack Guide — RAG, PageIndex & ADK

## Rung 0: do you need RAG at all?

If the corpus fits in context (< ~100K tokens), just include it. RAG adds
retrieval failure modes; earn them. Structured facts → SQLite/Postgres rows,
not embeddings (exact recall beats similar recall).

## The production pipeline (when you do need it)

```
[Query]
  → 1. Hybrid retrieval: BM25 + vector (pgvector / Elasticsearch) — top ~50
  → 2. Cross-encoder re-rank (BGE-Reranker class) — top ~15 highest-quality
  → 3. Structural routing: parent-child trees — pull full pages/sections
       around the winners, not naked chunks
  → [LLM generation with grounded, cited context]
```

- **pgvector by default** — native Postgres, no extra service, `<->` operator.
  A dedicated vector DB (Qdrant) only at serious scale or heavy filtering.
- Chunk on structure (headings/sections), never fixed 512-token windows.
  Store parent ids so step 3 can expand.
- Always cite sources in the answer; uncited RAG is hallucination with props.

## Vectorless / hierarchical (PageIndex)

For dense documents (financial reports, contracts, manuals): build a
**structural tree** (`pageindex` — LiteLLM under the hood, routes to any model)
and let the LLM *reason down the tree* instead of similarity-matching chunks.
Higher accuracy, higher cost — pick it when wrong answers are expensive.

## ADK (Google Agent Development Kit)

Multi-agent orchestration (graph workflows, agent teams). Rule from
production: a single structured-output call does NOT need ADK — it adds
latency and complexity for zero gain. Reach for it only when you truly have
planner + tools + memory agents cooperating.

## The 5 mistakes agents make

1. Embedding everything when the corpus fits in context.
2. Vector-only retrieval — misses exact terms BM25 catches (names, codes).
3. Skipping the re-ranker; feeding the LLM 50 mediocre chunks.
4. Fixed-size chunks that cut tables and clauses in half.
5. ADK/agent-frameworks for what one prompt with a schema does.
