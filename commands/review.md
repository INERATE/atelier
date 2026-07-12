---
description: Run the Atelier gates — ponytail, graph impact, lint/typecheck, design tokens, file sizes — and update the done-state contract with evidence.
---

Review the current changes (or: $ARGUMENTS) against every applicable gate:

1. **Minimalism**: ponytail review — flag reinvented stdlib, dead flexibility,
   unneeded deps.
2. **Impact**: code-review-graph `detect_changes` + `get_impact_radius`; check
   `tests_for` coverage on changed functions.
3. **Mechanical**: project lint + typecheck; run each changed file's self-check.
4. **Size law**: any source file >250 words → list with split suggestions
   (>350 should have been blocked — investigate if found).
5. **Design** (UI changes only): gateway → design-law checklist §9, including
   the no-hardcoded-colors rule; verify dark AND light resolve.
6. **Auth** (auth changes only): auth-law shipping checklist, line by line.

Then update `done_criteria.passed` + evidence via store.py for every criterion
a gate proves, and report findings ranked by severity — with the exact fix for
each, not just the complaint.
