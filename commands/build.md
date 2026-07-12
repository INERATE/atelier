---
description: Execute the active plan through the loop engine (builder/Sonnet; summarizer/Haiku for digests). Refuses to finish with unmet criteria.
---

Execute the active Atelier plan (or the specific task: $ARGUMENTS).

1. Load the active plan + unmet criteria:
   `python "${CLAUDE_PLUGIN_ROOT}/db/store.py" sql "SELECT id,title FROM plans WHERE status='active'"`
   `... sql "SELECT id,criterion,check_kind FROM done_criteria WHERE passed=0"`
   No active plan → tell the user to run `/atelier:plan` and stop.
2. Route per the loop-engine model table: implementation tasks → **builder**
   agent (parallel builders for independent tasks); digests/log updates →
   **summarizer**; if a task reveals an architectural hole, stop and send it
   back through **architect** — never improvise architecture at build tier.
3. For UI tasks: gateway skill first, then design-law. For auth: auth-law. All
   code: clean-code-law + structure-law.
4. After each task, run its automated checks and update `done_criteria` with
   evidence. Then re-query unmet criteria and continue the loop.
5. Terminate ONLY when unmet criteria = 0 (manual ones need the user's explicit
   confirmation, logged as evidence). Report: what shipped, evidence per
   criterion, anything deferred with a `ponytail:` note.
