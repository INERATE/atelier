---
description: One-shot Atelier setup — workspace, SQLite store, environment doctor, companion tools. Run once per project.
---

Set up Atelier in this repository. Do everything yourself; ask the user only
for secrets you cannot detect.

1. **Probe the environment** (node, python3, git, docker, ffmpeg, pnpm/uv) and
   record each result: after init, `python "${CLAUDE_PLUGIN_ROOT}/db/store.py"
   exec "INSERT OR REPLACE INTO capabilities VALUES ('<name>',<0|1>,'<version>',datetime('now'))"`.
2. **Create the store**: `python "${CLAUDE_PLUGIN_ROOT}/db/store.py" init` —
   creates `workspace/atelier.db` with schema + seeded rules/registry. Add
   `workspace/` to the project `.gitignore` if missing.
3. **Verify companions**: check which registry MCPs (shadcn, aceternity,
   react-bits, stitch) and skills (ponytail, code-review-graph) are available;
   update `registry` rows' meta with availability. If code-review-graph is
   installed but unindexed, run `code-review-graph build`.
4. **Credentials (optional — never block on this)**: ask ONE question — how to
   connect Google AI for media generation: (a) public Gemini API key →
   `GOOGLE_API_KEY`, (b) Vertex AI → paste the service-account JSON **path** →
   `GOOGLE_APPLICATION_CREDENTIALS` + `GOOGLE_CLOUD_PROJECT` +
   `GOOGLE_CLOUD_LOCATION=global`, or (c) skip. Write choices to the project
   `.env` (create it; confirm `.env` is gitignored). Keys NEVER go in the
   SQLite store or committed files. On skip: say "no token — media generation
   will use the paste-prompt fallback" and continue.
5. **Report**: a compact table — capabilities found, store path, companions
   available/missing (with the one-line install for anything missing),
   credentials mode (public / vertex / none).
6. Offer next step: `/atelier:plan` to run project intake.
