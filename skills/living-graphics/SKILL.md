---
name: living-graphics
description: Continuous, self-contained component animations — Cloudflare/Stripe-style dynamic infographics. Inline SVG schematics with flowing data packets, pulsing nodes, and state-reactive timelines that run inside a card, not across the page. Load when building animated cards, data-flow diagrams, "how it works" graphics, ambient loops, or interactive micro-experiences.
---

# Living Graphics

Scrollytelling moves a camera down the page. **Living graphics live inside one
component**: a schematic where data visibly flows, nodes pulse, and the loop
never stops — and shifts state when the user hovers or switches a tab. This is
the signature move of premium tech marketing (Cloudflare's pipeline diagrams,
Stripe's payment flows).

## The technique ladder (stop at the first rung that holds)

1. **CSS keyframes on inline SVG** — animate `stroke-dashoffset` on a dashed
   path and the wire itself flows. Covers ~90% of these graphics. Zero JS.
2. **Traveling packets** — a `<circle>` with CSS `offset-path: path('…')` +
   `offset-distance` keyframes rides any wire. Stagger with `animation-delay`.
3. **State shifts (tabs/hover)** — JS does ONE thing: set `data-state` on the
   component. CSS variables scoped to `[data-state="paid"]` change speed,
   color, and which wires run. Never re-render the SVG.
4. **rAF / GSAP timeline** — only for sequenced choreography CSS can't express
   (pause → morph → resume). GSAP only if the project already has it.
5. **Rive / Lottie** — when a *designed* asset exists (Rive editor / After
   Effects → JSON + tiny runtime). This is the "user made the animation"
   option; offer it, don't default to it.

## The recipe — a data-pipeline graphic

- **Inline `<svg>`, never `<img>`** — every line and label must be targetable.
- Geometry on the 24px blueprint grid: hairline boxes (`stroke: var(--hairline-2)`,
  1.5px), dashed connectors `stroke-dasharray: 3 7`, corner ticks on key nodes.
- Flow: `@keyframes flow { to { stroke-dashoffset: -10 } }` on wires,
  1–2s linear infinite. Packets: accent-filled circles on `offset-path`,
  3–6s cycles, opacity fades at both ends.
- Color: monochrome ink for structure; the ONE accent marks only what moves
  (packets, the live node). Text: 10–11px uppercase, tracked, `--ink-3`.

## Laws (design-law still governs)

- Animate ONLY `transform`, `opacity`, `stroke-dashoffset`, `offset-distance` —
  compositor-cheap, no layout thrash.
- Ambient loops are quiet: 2–6s cycles, low contrast, no bouncing. They must
  not compete with the page's ONE hero moment.
- `prefers-reduced-motion: reduce` → the loop stops and the graphic shows its
  complete static state (all wires visible, packets hidden).
- Many loops on one page? Pause offscreen: IntersectionObserver toggles a
  `.paused` class → `animation-play-state: paused`.

## Reference skeleton

```html
<svg viewBox="0 0 800 200">
  <rect class="node" x="20" y="70" width="120" height="60" rx="8"/>
  <path class="wire" d="M140 100 H320"/>
  <circle class="pkt" r="3" style="offset-path:path('M140 100 H320')"/>
</svg>
<style>
.node{fill:none;stroke:var(--hairline-2);stroke-width:1.5}
.wire{stroke:var(--hairline-2);stroke-width:1.5;stroke-dasharray:3 7;animation:flow 1.4s linear infinite}
.pkt{fill:var(--accent);animation:travel 4s linear infinite}
@keyframes flow{to{stroke-dashoffset:-10}}
@keyframes travel{0%{offset-distance:0%;opacity:0}10%{opacity:1}90%{opacity:1}100%{offset-distance:100%;opacity:0}}
@media (prefers-reduced-motion:reduce){.wire,.pkt{animation:none}.pkt{display:none}}
</style>
```

Live example: the pipeline card on https://inerate.github.io — built exactly
from this recipe, no video, no library.
