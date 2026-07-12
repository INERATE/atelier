---
description: Health check — re-probe environment, verify store integrity, companion MCPs/skills, and graph freshness.
---

Run the Atelier health check and fix what you can:

1. Re-probe tools (node, python3, git, docker, ffmpeg, pnpm/uv) and refresh
   `capabilities` rows with current versions.
2. Store: `PRAGMA integrity_check` on `workspace/atelier.db`; verify
   `meta.schema_version` matches the plugin's `db/schema.sql`.
3. Companions: registry MCPs respond? ponytail + code-review-graph present?
   Graph stale (many commits since last index)? → run `code-review-graph update`.
4. Hooks: `python "${CLAUDE_PLUGIN_ROOT}/hooks/file_size_gate.py" --test` and
   `session_start.py --test`.
5. Report: ✅/❌ table with the one-line fix for every ❌. Fix automatically
   what needs no secret or destructive action.
