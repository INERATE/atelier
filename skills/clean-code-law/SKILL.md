---
name: clean-code-law
description: The Atelier Clean Code Law — 250-word-per-file budget, DRY via the graph, ponytail minimalism, and the comment policy. Load before writing or refactoring any source code.
---

# Clean Code Law

Small files, no repetition, no speculation. Any developer must be able to edit
the codebase without going mad in thousand-line files.

## The 250-word rule

- **Budget: ≤250 words per source file** (whitespace-separated tokens, code and
  comments). **Hard cap: 350** when splitting would genuinely harm cohesion.
- Enforced by the `file-size-gate` hook — an oversized write comes back to you
  with instructions; split before continuing.
- **Exempt:** docs (`*.md`), lockfiles, generated files, migrations, JSON/YAML
  data, vendored code. Config lives in `rules` (domain `code`) and can be tuned.
- Why: small files are readable, reviewable, independently testable, cheap for
  agents to load, and force real module boundaries.

## How to split (in preference order)

1. Extract pure helpers into a sibling module the file imports.
2. Split by responsibility (parsing vs validation vs IO), never by line count.
3. Component files: one component per file; hooks into `hooks/`; variants into
   a `variants.ts`.
4. If a file resists splitting, the design is wrong — fix the design.

## DRY (never repeat yourself)

Before writing anything, check it doesn't already exist: code-review-graph
(`semantic_search_nodes`) or repo search. If it exists, import it. If it almost
exists, extend it where it lives. A bug fix goes in the shared function all
callers route through — never patched per-caller.

## Ponytail alignment (the ladder is law here too)

Does it need to exist? → reuse in-repo → stdlib → native platform → installed
dep → one line → only then minimal new code. No interfaces with one
implementation, no config for constants, no scaffolding "for later".

## Comments

Premium and sparse: only constraints the code cannot show (invariants, gotchas,
external contracts, `ponytail:` ceiling notes). Never narrate what the next
line does. No dead code, no commented-out blocks.

## Every non-trivial file leaves one check

A branch/loop/parser/money/security path ships with the smallest runnable check
that fails if the logic breaks (an `assert` self-check or one tiny test). No
frameworks unless the project already has one.
