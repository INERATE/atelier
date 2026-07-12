---
name: design-law
description: The Atelier Design Law — premium, industrial-grade UI. Load BEFORE any UI/design work (pages, components, animations, icons, landing pages). Defines the style vocabulary, tokens, motion physics, component canon, reference canon, and the banned AI-slop anti-style.
---

# Atelier Design Law

When a prompt says "make it premium", it means **exactly this document**. If a
choice isn't covered, pick the calmer, quieter option. First run the gateway
skill — overlays in `design_guide_versions` may extend this law.

## 1. Vocabulary (say these words, get this taste)

| Term | Meaning | Exemplars |
|------|---------|-----------|
| Apple HIG | Clarity, deference to content, depth via layers | macOS, iOS |
| Editorial minimalism / Swiss style | Typography IS the design: strict grid, huge type-scale contrast, whitespace, near-monochrome, ONE accent | Linear, Vercel, Stripe |
| Glassmorphism (chrome only) | backdrop-blur panels for navbars/docks/overlays — never every card | macOS Big Sur |
| Enterprise motion choreography | Motion as physics system: springs, scroll-scrub, staggers | Cloudflare, Apple product pages |
| Scrollytelling | Scroll-scrubbed narrative scenes, pinned sections, frame sequences | Apple AirPods, Cloudflare home |
| Blueprint motif | Dotted/dashed hairline grid background, corner tick marks on cards, schematic diagrams | Cloudflare 2026 |
| Quiet depth | Depth from top-light insets and layering, not drop shadows | macOS windows |

## 2. Reference canon (studied, not copied)

- **Cloudflare.com (2026)** — the gold standard for dark editorial marketing:
  near-black `#0B0B0C` base, dotted blueprint grid with corner ticks framing
  sections, ONE saturated accent (their orange) used for CTA bands and state,
  massive grotesk display headlines ("Build without boundaries"), bento feature
  cards with hairlines + live product mock terminals, full-bleed accent CTA
  bands with floating outlined glyph cards, pill segmented pricing toggles,
  logo-tab quote carousel, benefit ticker strip above the footer.
- **GitHub.com** — dark hero with a single soft radial glow behind centered
  display type, product screenshot in a framed window below the fold, gradient
  restraint everywhere else.
- **Linear / Vercel / Stripe** — hairlines, tabular numerals, serif-italic
  editorial accents, monochrome discipline.
- **GC Design Language** (GrowthCharters) — the parent of this law; emerald
  accent variant proving the system is brand-parameterizable.

## 3. Tokens (numbers, not vibes)

```
--bg:        #0A0A0B dark / #FAFAF8 light      --bg-raised: #141518 / #FFFFFF
--ink:       #F5F5F3 / #1A1A18                 --ink-2: #9B9B98   --ink-3: #5C5C5A
--hairline:  rgba(255,255,255,.08) / rgba(0,0,0,.08)
--accent:    THE user's ONE brand color (project intake) — budget ≤10% of any viewport
Radius: 8 inputs / 12 cards / 16 modals / full pills.  Spacing: 4-scale, ≥96px between landing sections.
Depth: layering + inset top-light `0 1px 0 rgba(255,255,255,.04)`; drop shadows ONLY on floating layers.
```

Type: grotesk UI/display (weights 400/500/600, -2% tracking on display), serif
italic for ONE emphasized phrase per major headline + big stats. Kickers: 11px
uppercase 0.14em `--ink-3`. Display: `clamp(3rem, 8vw, 7rem)`. Data numerals:
`tabular-nums`.

**Theming is centralized — NEVER hardcoded.** Every color/radius/shadow lives as
a CSS variable in ONE place (`globals.css` / tokens file); components reference
semantic tokens (`bg-background`, `text-ink-2`, `border-hairline`), never hex
values or `dark:` one-offs per page. Dark, light, or any future theme = flip the
variable set on `:root[data-theme]` — zero per-page edits. A hardcoded color in
a component is a review failure.

## 4. Motion system

- Entrances: `cubic-bezier(0.16,1,0.3,1)`; interactive: spring `{stiffness:260,
  damping:32, mass:0.9}` — max one overshoot. Micro 150–250ms, element
  300–500ms, scene 600–900ms; >1s only scroll-scrubbed.
- Stagger lists 60–80ms, 24px rise+fade. **Scrub narrative (GSAP ScrollTrigger
  + Lenis), trigger UI (Framer Motion).** Shared-element morphs via `layoutId`.
- ONE hero moment per page. Exits ~60% of enter, opacity-led. Interruptible.
  `prefers-reduced-motion` → fades only. Animate transform/opacity/canvas ONLY.
- Signature micro-interactions: hover lift −2px + border brighten; press
  scale(.98) spring; count-up stats (once); checkmark stroke-draw; word-reveal
  AI streaming; per-component skeletons (no full-page spinners).

## 5. Iconography & imagery

Lucide only, 1.5px stroke, 16/20/24, `currentColor` monochrome — never filled,
multicolor, or in colored circles. Accent only on state (verified/live/active).
Gaps → Phosphor thin or custom SVG on the 24px grid. Animated: Rive/Lottie,
monochrome+accent, single-loop. Emoji never in chrome. Illustrations: abstract
geometric blueprint motif (dot grids, wireframe globes, hairline schematics).
Product imagery: real UI in device frames on dotted-grid pedestals with corner
ticks — never fake dashboards. Fonts via Google Fonts (or system).

## 6. Component canon & registry

Card = raised surface, hairline, radius 12–16, 24px padding, top-light; header
row = 36px bordered icon square + title + uppercase tag. Stat block = serif
numeral over uppercase label, vertical hairline dividers. Nav = glass pill,
condenses on scroll. Buttons: primary ink-filled pill (inverts on hover),
secondary ghost hairline; ONE primary per view. Inputs: sunken + accent hairline
focus glow. Tables: hairline separators, 11px uppercase heads.

**Never hallucinate components.** Query the registries first — shadcn/ui (MCP),
Aceternity (MCP), ReactBits (MCP), Motion.dev, MagicUI, Radix — then adapt to
these tokens. `python <plugin>/db/store.py registry component` lists what's
available.

## 7. Landing-page anatomy (the Cloudflare-grade default)

1. Hero: one massive claim, subline, single primary CTA; ONE hero moment.
2. Proof strip: customer logos / "42% of Fortune 500"-style stat.
3. Quote carousel with logo tabs (real quotes only).
4. Problem→solution split panel (dark chaos vs accent-clean, à la "fighting
   infra" vs "shipping").
5. Bento grid of features with live product mocks.
6. Pricing: pill segment toggle, hairline tier cards, honest numbers.
7. Full-bleed accent CTA band + benefit ticker.
8. Dense multi-column footer.
Scrollytelling (video→frames scrub) when the product has a narrative.

## 8. The anti-style (BANNED — the "AI-slop" look)

Rainbow/purple-pink gradient heroes · glossy 3D emoji icons · colored icon
circles in 8 hues · heavy card shadows · bounce-in animations · centered
feature-grid walls · fake dashboard screenshots · multiple accent colors ·
full-page spinners. If it looks like a template, delete it.

## 9. Review checklist (UI may not ship failing any)

- [ ] One accent, ≤10% viewport; near-monochrome otherwise
- [ ] Hairlines not shadows; top-light insets; correct radii
- [ ] Type scale + serif-italic accent used once per headline; tabular numerals
- [ ] Motion: springs/expo, staggered, reduced-motion fallback, no layout thrash
- [ ] Lucide monochrome icons only; no emoji in chrome
- [ ] Components sourced from registry, restyled to tokens
- [ ] Dark AND light themes resolve; responsive at 360/768/1280
- [ ] Zero anti-style items present
