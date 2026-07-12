-- Atelier seed: core rules + curated registry. Idempotent.
DELETE FROM rules WHERE source='core';
INSERT INTO rules (domain,key,value,source) VALUES
 ('code','file_word_budget','250 soft / 350 hard; exempt: md,json,yaml,lock,sql,generated','core'),
 ('code','dry','check graph/repo first; import, never rewrite; fix bugs in the shared function','core'),
 ('code','comments','sparse, intent-only; no narration; ponytail: notes for deliberate ceilings','core'),
 ('design','accent_budget','ONE brand accent, <=10% of any viewport','core'),
 ('design','theming','all colors as CSS variables in globals.css; semantic tokens in components; NEVER hardcode hex or per-page dark: overrides','core'),
 ('design','icons','Lucide 1.5px monochrome currentColor only; accent only on state','core'),
 ('design','motion','ease-out-expo entrances; springs 260/32/.9; stagger 60-80ms; reduced-motion fallback; transform/opacity only','core'),
 ('design','anti_style','no rainbow gradients, 3D emoji icons, colored icon circles, heavy shadows, bounce-ins, template grids','core'),
 ('structure','api_pattern','/api/v1/{feature}/{action}; thin endpoints, logic in services','core'),
 ('structure','monorepo','multiple frontends -> Turborepo apps/ + packages/','core'),
 ('auth','token_model','15min access JWT + 30day rotating single-use refresh; families; 60s grace; sliding window','core'),
 ('auth','refresh','silent one-shot timer + on-demand; single mutex per app; NEVER poll','core'),
 ('auth','redirect','login redirect is the LAST resort after silent refresh + session check','core'),
 ('stack','realtime','SSE or WebSockets, never polling; cache invalidation on write','core'),
 ('stack','llm_payloads','TOON over JSON for LLM-bound payloads; gRPC backend-to-backend','core');

DELETE FROM registry WHERE kind IN ('component','skill','mcp');
INSERT INTO registry (kind,name,source,install,usage,meta) VALUES
 ('component','shadcn/ui','https://ui.shadcn.com','shadcn MCP / npx shadcn add','Radix primitives; restyle to tokens','a11y,ssr,dark'),
 ('component','Aceternity UI','https://ui.aceternity.com','aceternityui MCP','premium animated sections; strip to one accent','animated,dark'),
 ('component','ReactBits','https://reactbits.dev','react-bits MCP','micro-interaction components','animated'),
 ('component','Motion.dev','https://motion.dev','npm i motion','springs, layout morphs','animated'),
 ('component','MagicUI','https://magicui.design','npx magicui add','marketing components; token restyle required','animated,dark'),
 ('skill','ponytail','github:ponytail','/plugin install ponytail','minimalism enforcement on every coding task',''),
 ('skill','ui-ux-pro-max','local skill','installed','style/palette/font intelligence for UI work',''),
 ('mcp','code-review-graph','local','code-review-graph build','structural graph: impact radius, callers, tests-for',''),
 ('mcp','stitch','MCP','installed','high-fidelity screen generation + design systems','');
