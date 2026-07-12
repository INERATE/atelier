---
description: Final release gate — verify the entire done-state contract with evidence, then produce the ship report.
---

Run the Atelier ship gate for the active plan:

1. Re-run `/atelier:review` gates fresh — no trusting stale evidence.
2. Verify EVERY `done_criteria` row: automated kinds re-executed now; manual
   kinds confirmed by the user in this conversation (quote their confirmation
   as evidence).
3. Any criterion unmet → NOT shippable. List exactly what's missing and stop.
4. All met → mark the plan `status='shipped'`, write an `activity_log` entry,
   and produce the ship report: what was built, evidence per criterion,
   deployment steps (deploy-advisor) with costs, and post-ship checks
   (monitoring, error tracking, cache behavior).
