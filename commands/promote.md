---
description: Make a learned overlay permanent — move it from the gitignored workspace into tracked project design docs. Usage: /atelier:promote <overlay-file-or-'latest'>
---

Promote the overlay: $ARGUMENTS (or the newest unpromoted one).

1. List candidates:
   `python "${CLAUDE_PLUGIN_ROOT}/db/store.py" sql "SELECT id,path FROM design_guide_versions WHERE kind='overlay' AND promoted=0"`
2. Show the user the overlay's content and confirm the promotion — this is a
   deliberate human act, never automatic.
3. Move the file from `workspace/overlays/` to `docs/design/` in the project
   (git-tracked). Update the pointer row: new path, `promoted=1`. Update its
   `rules` rows' source to `overlay-promoted:<file>`.
4. Referenced media the overlay needs (images/frames) → copy into
   `docs/design/assets/` and fix paths.
5. Commit is the user's call — stage nothing without asking. Report the diff
   summary.

The plugin's core design-law file is NEVER edited by promotion — project law
lives in the project's own `docs/design/`, layered above core by the gateway.
