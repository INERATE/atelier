---
description: Understand-first clarification — reads everything, then asks only the unknowns, batched once.
---

Run the Atelier clarification protocol (loop-engine skill, steps 1–2) for the
current task or: $ARGUMENTS

1. Read before asking: repo, CLAUDE.md, `workspace/project.md`, store rules,
   prior `clarifications` rows, the graph. Search the web only for missing
   external facts.
2. Produce two lists: **assumptions** (defaults you will proceed with — each
   with its industrial-standard justification) and **unknowns** (only questions
   whose answer changes what gets built).
3. Ask the unknowns in ONE batch. Never re-ask anything already answered in
   `clarifications`.
4. Persist every question + answer to `clarifications` via store.py, then
   continue the loop.
