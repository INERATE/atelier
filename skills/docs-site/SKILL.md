---
name: docs-site
description: Build a premium documentation site (Claude-docs style) with Astro Starlight, restyled to the design law, deployed free on GitHub Pages. Covers MDX vs Markdown, base-path setup, sidebar, search, and the deploy workflow. Load when the user asks for docs, a documentation site, a knowledge base, or a developer guide site.
---

# Docs Site

The lazy premium answer for documentation is **Astro Starlight**: dark/light
themes, sidebar, mobile nav, and offline full-text search (Pagefind) all built
in — you write markdown, it ships a static site. Never hand-roll a docs shell;
never reach for Docusaurus (heavier, React runtime) unless the project is
already React-docs-committed.

## Recipe (proven live at inerate.github.io/docs)

**Separate repo** — docs never live inside a plugin/library repo users clone.
Name the repo `docs` under the org → serves at `<org>.github.io/docs`.

Five files, scaffolded by hand (`npm create astro` can stall on Windows —
write the files directly, then `npm install`):

1. `package.json` — deps only: `astro ^5`, `@astrojs/starlight ^0.36`.
2. `astro.config.mjs` — `site: 'https://<org>.github.io'`, `base: '/docs'`
   (**forgetting `base` breaks every asset and link**), `starlight({ title,
   sidebar, customCss: ['./src/styles/custom.css'] })`. Sidebar groups by
   audience: Start here / Concepts / Using it / Maintainers.
3. `src/content.config.ts` — `docsLoader()` + `docsSchema()` verbatim.
4. `src/styles/custom.css` — map Starlight vars to design-law tokens:
   `--sl-color-accent`, `--sl-color-bg`, `--sl-color-text` for BOTH
   `:root` and `[data-theme='light']`. This is the whole restyle.
5. `.github/workflows/deploy.yml` — `withastro/action@v3` build job +
   `actions/deploy-pages@v4` deploy job; enable Pages with
   `gh api repos/<org>/docs/pages -X POST -f build_type=workflow`.

Push markdown → live in ~90s. No manual builds ever.

## MDX vs Markdown

- `.md` — default for every page. Frontmatter `title` + `description` required.
- `.mdx` — ONLY when a page needs components: Starlight's `<Card>`,
  `<CardGrid>`, `<Tabs>`, `<Steps>`, `<LinkCard>` (import from
  `@astrojs/starlight/components`), or custom Astro components. Typical: the
  landing `index.mdx` with a hero + card grid; everything else stays `.md`.
- Never put raw HTML layout in `.md` — if a page needs structure, it's `.mdx`
  with components.

Landing page frontmatter: `template: splash`, `hero:` with `tagline` and
`actions` — gives the big centered hero without any custom code.

## Laws

- Content pages are plain prose + code blocks; components are seasoning,
  not structure. One `<CardGrid>` per page maximum.
- Internal links are root-relative WITH the base: `/docs/start/install/`.
- Every page answers one question; title says it ("Install & first project",
  not "Getting Started").
- A `privacy.md` page (local-only, no telemetry) costs 5 minutes and is
  required by plugin-marketplace submission forms — add it day one.
