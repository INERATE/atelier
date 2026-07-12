---
name: mcp-maker
description: Turn any component site, asset library, or API into something agents can use — a registry entry, a skill, or a full MCP server. Load when the user says "add this site/library to Atelier" or wants to contribute a new integration.
---

# MCP Maker

Not everything needs an MCP server. Pick the cheapest rung that works:

## The decision ladder

| The source is… | Build this | Effort |
|----------------|-----------|--------|
| Copy-paste components with a repo (ReactBits-style) | **Registry row** + the GitHub-MCP pattern (agent reads real source from the repo) | 2 min |
| A library with a CLI (`npx x add <c>`) | **Registry row** with the install command | 2 min |
| Knowledge/patterns/rules (a design system, a guide) | **Skill** (`SKILL.md`) | 30 min |
| A live API the agent must query (search, generate, fetch) | **MCP server** | hours |

## Registry row (the 90% case)

```
python <plugin>/db/store.py exec "INSERT INTO registry (kind,name,source,install,usage,meta)
  VALUES ('component','<Name>','<url>','<install cmd>','<when/how to use>','<tags>')"
```
For repos without CLIs, set usage to: "read source via GitHub MCP:
search <owner>/<repo> for <component>" — the agent pulls real code, zero hallucination.

## Skill (knowledge)

`skills/<name>/SKILL.md`: frontmatter description ≤2 sentences stating WHEN to
load it; body teaches decision rules and exact values, not tutorials. Add a
`framework_map` row so `store.py map <topic>` finds it. Follow clean-code-law
for any bundled scripts.

## MCP server (only for live APIs)

Minimal stdio server exposing 2–3 tools (`search_x`, `get_x`); TOON-lean
responses (no JSON bloat back to the model); version-pin in `registry`;
document env vars in `.env.example`. If an official MCP exists (shadcn,
aceternity), NEVER rebuild it — registry-row it.

## Contribution path

Fork → add row/skill/server per above → self-check (skill loads, row queries,
server answers) → PR using the proposal template. Review gates apply
(ponytail: the ladder rung must be justified).
