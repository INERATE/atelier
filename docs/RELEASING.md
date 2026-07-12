# Releasing & Updating

The single rule everything hangs on: **Claude Code only ships what the
`version` field in `.claude-plugin/plugin.json` announces.** Commits without a
bump never reach users — no error, no hint.

## Owner / contributor — every release

1. Make the change. Code files stay ≤ 250 words (CI hard-caps at 350).
2. Seed discipline: `db/seed/seed.sql` must stay **idempotent** — core rows
   land via `INSERT OR REPLACE` against a unique key (registry) or
   `DELETE … WHERE source='core'` + insert (rules). Never a plain `INSERT`;
   that's how the v0.2.2 duplication bug happened.
3. New skill/tool/agent? Add its `framework_map` row in the seed, or agents
   can never find it (`store.py map <topic>` is how they discover pieces).
4. **Bump `version`** in `.claude-plugin/plugin.json`:
   patch = fix · minor = new skill/tool/command · major = breaking schema.
5. Commit `release: vX.Y.Z — what changed`, push to `main`, confirm CI green.
   That IS the release — no registry, no upload, no build.

Pre-push check (what CI runs): `claude plugin validate .`, both hooks
`--test`, `store.py init` + the three seed greps, manifests parse, word audit.

## Users — getting updates

- Manual: `/plugin update atelier` (or `claude plugin update atelier`), then restart.
- Automatic: `/plugin` → Marketplaces → `atelier-marketplace` → **Enable
  auto-update** — third-party marketplaces are OFF by default; official
  Anthropic ones are ON.
- Then `/atelier:update` inside a project migrates its store.

## Agents — what /atelier:update guarantees

`store.py init` IS the migration: schema is `CREATE IF NOT EXISTS`, seed is
idempotent and self-healing (dedupes, upserts core rows). It never touches
`workspace/overlays/`, plans, criteria, or user-learned registry rows. Report
schema_version and row counts before → after; that's the whole contract.
