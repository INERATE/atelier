---
description: Project intake + architecture + done-state contract (architect/Opus). Usage: /atelier:plan <what you want to build>
---

Run the Atelier planning phase for: $ARGUMENTS

1. Load the **loop-engine** skill and follow Understand → Clarify → Plan.
2. If `workspace/project.md` does not exist, run intake first: ask the user to
   paste a detailed project md OR answer the intake batch (what/users/features/
   goals; stack; repo layout per structure-law; auth mode per auth-law; hosting
   per deploy-advisor with costs; ONE brand accent color). Write
   `workspace/project.md` from the answers and record the choices in `projects`.
3. Delegate planning to the **architect** agent (it thinks at max depth). It
   must persist the plan to `plans` (status 'active') and every done-criterion
   to `done_criteria` via store.py.
4. Log any questions asked + answers into `clarifications`.
5. Present to the user: the plan summary, the done-state contract as a
   checklist, cost table if hosting is involved, and the first `/atelier:build`
   step.
