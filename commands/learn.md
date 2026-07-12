---
description: Teach Atelier — ingest images, videos, URLs, code, or new skills/MCPs into self-learning overlays. Usage: /atelier:learn <paste/describe/attach references>
---

Ingest these references into Atelier's self-learning layer: $ARGUMENTS

1. Gather inputs: anything attached/pasted in this conversation PLUS any new
   files in `workspace/references/` not yet in `learning_events`
   (`python "${CLAUDE_PLUGIN_ROOT}/db/store.py" sql "SELECT path_or_url FROM learning_events"`).
2. Delegate to the **learner** agent — it classifies, files, extracts rules,
   writes overlays + pointer rows + registry entries. Core files stay
   untouched.
3. For URLs the learner cannot fetch, use web search/fetch yourself and hand it
   the content.
4. Report: what was learned (per item, one line), where it lives (overlay path
   / registry row), and that the gateway will now include it in every UI task.
   Suggest `/atelier:promote <overlay>` for anything that should become
   permanent, git-tracked law.
