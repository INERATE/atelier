# Palette inference

Select color from evidence before drawing a screen. Record four short lines in
the plan or design notes: product mood, evidence inspected, chosen accent with
light/dark variants, and why it fits better than the nearest alternative.

Use this evidence order:

1. Explicit user brand rules and accessibility requirements.
2. Existing logo, product screenshots, design tokens, and marketing assets.
3. The product's real environment: audience, task intensity, subject matter,
   content density, and emotional register.
4. A restrained category prior only when the first three provide no signal.

Extract dominant asset colors, then reject colors that are incidental,
low-contrast, overrepresented in competitor templates, or semantically wrong.
Preserve a recognizable established brand unless it fails accessibility. Use a
neutral canvas with one accent; derive hover, focus, muted, and foreground
tokens from that accent rather than introducing more hues.

When the evidence does not already define a complete palette, select one named
recipe from [the industry palette catalog](palette-catalog.md). Use the recipe
as a coherent set: do not combine its canvas with an unrelated accent merely
for novelty. The catalog is a starting point, not a substitute for brand
evidence. It deliberately spans cool, warm, chromatic, and monochrome canvases
so unrelated products do not collapse into the same visual identity.

Category priors are tie-breakers, not brand stereotypes:

- developer/infrastructure: signal orange, indigo, or cool blue
- finance/security/B2B productivity: cobalt or deep blue
- health/science: cyan or mineral blue; teal only with supporting evidence
- culture/media/creative: coral, vermilion, or editorial magenta
- premium/luxury/hospitality: bronze, ochre, or warm ivory on ink
- education/community: indigo or clear blue
- climate/nature: forest green only when the subject itself supports it
- unknown: Graphite Cobalt from the catalog

Green and emerald require direct evidence: an existing brand, nature/climate
semantics, a success/status state, or an explicit request. Familiarity with an
older Atelier example is not evidence. Status green never becomes the brand
accent automatically.

Generate dark and light values from perceptual color space when the stack
supports it. Verify normal text at 4.5:1, large text at 3:1, component boundaries
and focus states at 3:1, and do not communicate state by color alone. Check the
accent at 360, 768, and 1280 pixels; it should occupy no more than ten percent
of a typical viewport.

Do not treat semantic status colors as extra brand accents. Success, warning,
danger, and info colors appear only beside a label or icon, stay inside the
component that needs them, and never drive decorative sections or marketing
artwork.
