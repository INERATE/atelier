# Industry palette catalog

These recipes provide distinct, production-ready directions when brand evidence
does not already define a palette. Pick one recipe from the index and use its
named neutral family with its named accent pair. Never browse the tables for an
arbitrary favorite color.

## Recipe index

| Recipe | Neutral | Accent | Best fit | Character |
|---|---|---|---|---|
| Graphite Cobalt | Graphite | Cobalt | finance, security, B2B SaaS | precise, credible, calm |
| Carbon Signal | Carbon | Signal orange | infrastructure, developer tools | technical, energetic, direct |
| Slate Indigo | Graphite | Electric indigo | AI, education, community | intelligent, expressive, modern |
| Midnight Cyan | Midnight | Mineral cyan | health, science, analytics | clinical, lucid, fresh |
| Ink Vermilion | Paper | Vermilion | media, culture, publishing | editorial, confident, human |
| Aubergine Magenta | Aubergine | Editorial magenta | fashion, beauty, creative tools | cultured, vivid, premium |
| Bronze Noir | Carbon | Bronze | luxury, hospitality, architecture | tactile, composed, exclusive |
| Paper Crimson | Paper | Crimson | civic, advocacy, high-attention editorial | authoritative, urgent, clear |
| Alpine Teal | Forest | Alpine teal | wellness, sustainability operations | balanced, grounded, clean |
| Field Green | Forest | Field green | climate, nature, agriculture | organic, trustworthy, practical |
| Precision Mono | Paper | Monochrome | professional tools, portfolios, editorial | rigorous, timeless, quiet |
| Midnight Azure | Midnight | Azure | logistics, enterprise platforms, aviation | dependable, spacious, operational |

Field Green still requires direct brand or subject evidence. Precision Mono
uses contrast, typography, and density for hierarchy; it must not acquire a
second decorative hue.

## Neutral families

Each row lists `bg / raised / ink / ink-2 / hairline`. The hairline is for
separation; controls that depend on a visible boundary need a separate token
verified at 3:1.

| Neutral | Dark | Light |
|---|---|---|
| Graphite | `#090B10 / #121722 / #F4F7FF / #A6B0C0 / #283141` | `#F7F8FB / #FFFFFF / #121722 / #586477 / #D5DAE3` |
| Carbon | `#0D0B09 / #17130F / #F8F4EE / #ACA197 / #33291F` | `#FBF8F4 / #FFFFFF / #211A15 / #655B52 / #DED5CB` |
| Midnight | `#071019 / #0D1A26 / #EDF7FF / #9CAFC1 / #203246` | `#F4F8FC / #FFFFFF / #101B27 / #526577 / #D1DCE7` |
| Aubergine | `#110A10 / #1C111A / #FAF3F8 / #B4A1AE / #382735` | `#FBF7FA / #FFFFFF / #251720 / #6C5965 / #E3D7DF` |
| Paper | `#101010 / #191918 / #F5F4EF / #AAA9A3 / #31312E` | `#FCFBF7 / #FFFFFF / #1C1B18 / #64615B / #DDDAD0` |
| Forest | `#08100B / #101A14 / #F1F8F3 / #9EAEA3 / #26352B` | `#F5F9F5 / #FFFFFF / #17221A / #58665C / #D4DED6` |

## Accent pairs

Each cell lists `accent / on-accent`. The pairs exceed 4.5:1 for text placed on
the accent. Ordinary accent-colored text must be checked against its actual
canvas because that is a different contrast pair.

| Accent | Dark theme | Light theme |
|---|---|---|
| Cobalt | `#6EA8FF / #07111F` | `#1859C9 / #FFFFFF` |
| Signal orange | `#FF8A4C / #241006` | `#B83A08 / #FFFFFF` |
| Electric indigo | `#A78BFA / #160B2D` | `#5B3CC4 / #FFFFFF` |
| Mineral cyan | `#55D5E8 / #061A1E` | `#087F92 / #FFFFFF` |
| Vermilion | `#FF806D / #260A06` | `#BD321E / #FFFFFF` |
| Editorial magenta | `#F08AC1 / #290917` | `#A92367 / #FFFFFF` |
| Bronze | `#D8AD68 / #211407` | `#84540E / #FFFFFF` |
| Crimson | `#FF8492 / #29070C` | `#AD2338 / #FFFFFF` |
| Alpine teal | `#5AD2C6 / #061C1A` | `#087B73 / #FFFFFF` |
| Field green | `#6CCB91 / #071C10` | `#187445 / #FFFFFF` |
| Monochrome | `#F4F4F0 / #111112` | `#202124 / #FFFFFF` |
| Azure | `#73B7FF / #071421` | `#1467B8 / #FFFFFF` |

## Implementation contract

Map the selected values to semantic tokens in the single theme source:
`--bg`, `--bg-raised`, `--ink`, `--ink-2`, `--hairline`, `--accent`, and
`--on-accent`. Derive hover and pressed values in OKLCH when supported, changing
lightness by roughly 0.04 while preserving hue and chroma. Store the resolved
values as tokens so every browser receives deterministic colors.

Keep status tokens separate: `--success`, `--warning`, `--danger`, and `--info`
are functional signals with text or icon reinforcement. They never replace
`--accent`, appear in decorative gradients, or compete with the primary action.

Before shipping, measure the exact rendered pairs: 4.5:1 for normal text, 3:1
for large text and essential UI boundaries, and 3:1 for focus indicators against
adjacent colors. Check common color-vision deficiencies and verify that labels,
icons, patterns, or position carry every meaning without hue alone.
