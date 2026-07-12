---
description: Show the current Atelier phase — active plan, met/unmet criteria, capabilities, recent activity.
---

Report Atelier status from the store (read-only, be fast):

1. Active plan: `python "${CLAUDE_PLUGIN_ROOT}/db/store.py" sql "SELECT id,title,status,model FROM plans ORDER BY id DESC LIMIT 3"`
2. Contract: counts of passed vs unmet `done_criteria` for the active plan;
   list unmet ones.
3. Capabilities and any missing companions (from `capabilities` + `registry`).
4. Recent: last 5 `activity_log` rows.

Output: one compact status block — phase, progress bar (n/m criteria), unmet
list, next recommended command. No prose.
