# Stack Guide — Next.js (App Router)

## When to use
Any serious frontend: marketing sites, dashboards, multi-app platforms. Multiple
apps sharing auth/ui/config → Turborepo monorepo (see structure-law).

## Decision rules
- **Server Components by default**; `"use client"` only for interactivity.
- Styling: Tailwind CSS 4 with tokens as CSS variables in `globals.css` —
  components use semantic classes, never hardcoded colors (design-law).
- Components: Radix/shadcn primitives restyled to tokens; registry MCPs
  (shadcn, Aceternity, ReactBits) before writing custom.
- Forms: React Hook Form + Zod. Toasts: Sonner. Themes: next-themes
  (`data-theme` on root drives the token set).
- Animation: Framer Motion for UI; GSAP ScrollTrigger + Lenis only on
  narrative/landing pages.
- Data: fetch in server components; SSE for AI streaming; WebSockets for live;
  **never polling**.
- Images: `next/image`, assets pre-compressed to webp by the asset pipeline.

## The 5 mistakes agents make
1. `"use client"` on everything — killing RSC benefits and bundle size.
2. Hardcoding colors / `dark:` overrides per page instead of tokens.
3. Fetching in `useEffect` what a server component gets for free.
4. Giant `page.tsx` files — the 250-word law forces proper component splits.
5. Adding state libraries for what URL params / server state already hold.
