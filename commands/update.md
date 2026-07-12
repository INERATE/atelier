---
description: Update Atelier — pull the latest plugin, migrate the store, refresh companions, verify health.
---

Update this project's Atelier installation:

1. **Plugin**: tell the user to run `/plugin update atelier` (marketplace
   plugins update through the host; you cannot do it for them). If the plugin
   directory is a git checkout, `git pull` it.
2. **Store migration**: `python "${CLAUDE_PLUGIN_ROOT}/db/store.py" init` —
   schema is `CREATE IF NOT EXISTS` and seed is idempotent (core rows replaced,
   overlay/user rows untouched), so init IS the migration runner. Compare
   `meta.schema_version` before/after and report the change.
3. **Companions**: re-check registry MCPs/skills versions; flag anything
   broken or newly available.
4. **Verify**: run the `/atelier:doctor` checks; report a before → after
   summary (schema version, rule count, map nodes, companions).

Never touch `workspace/overlays/`, references, plans, or any user data during
an update — only core-sourced rows and schema.
