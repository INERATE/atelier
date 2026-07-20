---
name: asset-pipeline
description: Atelier's native asset tools — image→webp compression, video→webp frame sequences, scrollytelling scaffolding, and AI video generation (Gemini Omni Flash / Veo 3.1) with a graceful no-credentials fallback. Load when handling images, video, storytelling sections, or media generation.
---

# Asset Pipeline

## Tools

- `python <plugin>/mcp/assets/assets.py webp <image> [quality]` — any raster →
  webp beside it (Pillow). Run on EVERY raster an agent adds to `public/`.
- `python <plugin>/mcp/assets/assets.py frames <video> [fps]` — mp4 → webp
  frame sequence (needs ffmpeg; missing → tell the user the one-line install,
  continue with other work).
- `python <plugin>/mcp/assets/assets.py cut <image> [tol=32]` — flat background →
  transparent webp (samples the corner color; raise tol for gradients/noise).
- All record `asset_manifest` rows. Serve only webp to browsers.

## Transparency & icons (no model can do this — we do)

NO image model (Gemini, Imagen, DALL·E) outputs a real alpha channel. The
recipe: generate the mark on a FLAT background (the logo prompt below already
forces this), then `assets.py cut` strips it locally — free, offline, zero
credentials. Photos / complex subjects: `pip install rembg`, then
`rembg i in.png out.png` (local U2Net model, also key-free).

## Scrollytelling recipe (the storytelling primitive)

1. Get an mp4 (user-provided in `workspace/references/video/`, or generate — below).
2. `assets.py frames video.mp4 24` → `video_frames/frame_0001.webp …`
3. Copy frames to `public/frames/<name>/`; use `templates/ScrollScrub.tsx`
   (canvas scrub, sticky viewport). `prefers-reduced-motion` → static poster.
4. Design-law still applies: ONE hero moment per page.

## AI video generation — the ladder (never exit on missing credentials)

**Omni** = `gemini-omni-flash-preview`, Google's text→video model (Veo 3.1 is the
fallback family). Don't hand-roll the REST calls — the ladder is implemented:

```
python <plugin>/mcp/assets/video.py "a slow orbit around a matte black cube"
# or: from video import generate; rung, detail = generate(subject, out="hero.mp4")
```

### Verify every generation — measure, don't eyeball

```
python <plugin>/mcp/assets/verify.py hero.mp4 "#10B981" --audio
```

Prints accent coverage % and mean audio dB, exits nonzero on failure. Run it on
every generated video before showing the user. Two real defects shipped because
nobody measured: a file with a valid AAC stream that was **silent** (mean −91 dB
— "has audio" is not "is audible"), and a Veo clip whose prompt demanded one
accent while the frame read **90% emerald** against the ≤10% budget. Rewriting
the colour rule three ways brought it to 1.8%, then 0.7% — but only measuring
proved it. Report the number, never an adjective.

### Audio — silence is a choice, not a default to inherit

Veo 3+ generates **synced audio natively** (its headline feature over Veo 2).
Two things must agree or you get silence:

```python
generate("a machine room", audio="low industrial hum, distant servos")
```

This sets `generateAudio: true` in the request **and** writes the soundscape into
the prompt. Setting only the prompt does nothing — the API param governs.

`audio=False` (the default) is correct **only** for scroll-scrubbed
scrollytelling, where the browser never plays the file. For a hero, demo, or
social video, **ask the user** — do not inherit silence from the scrollytelling
recipe below. That inheritance shipped silent Veo 3 output for exactly this reason.

`generate()` returns `(rung, detail)`. Rungs 1–2 wrote the mp4 and `detail` is the
model that served it. **Rung 3 means `detail` IS the paste-prompt** — that is a
success path, not a failure: show it to the user and keep working. An expired key
falls through to the next rung instead of raising.

| Rung | Needs | Model |
|------|-------|-------|
| 1. Public Gemini API | `GOOGLE_API_KEY` | `gemini-omni-flash-preview` (live since 2026-06-30); Veo 3.1 fallback |
| 2. Vertex AI | `GOOGLE_APPLICATION_CREDENTIALS` (service-account JSON path) + `GOOGLE_CLOUD_PROJECT` + `GOOGLE_CLOUD_LOCATION` | **Veo 3.0 is what actually serves** (3.1 preview 404s on many projects). Omni is tried first only when `audio=False` — it is silent-only and speaks the `v1beta1 interactions` API, not `predictLongRunning`; probing it the Veo way 404s and misreads as "model missing". Always report which model served. |
| 3. **No credentials** | nothing | Emit the paste-prompt below for the user's Gemini app (Omni Flash powers it for subscribers). NOT an error — say "no token, continuing" and proceed. |
| 4. Nothing works | — | Ask the user to drop any mp4 into `workspace/references/video/`. |

Credentials live in the project `.env` (gitignored — verify), written at
bootstrap. Standard var names above (they match gcloud/Vertex conventions).
Never store keys in the SQLite store or any committed file.

## The paste-prompt (rung 3 — write it FOR the user, filled in)

> Generate a short video for a website scroll animation.
> **Audio:** none — silent scroll-scrubbed footage. *(For a hero/social video
> instead, replace this line with the soundscape you want.)*
> **Subject:** <one concrete scene — object, environment, mood>.
> **Style:** premium industrial minimalism; near-monochrome palette on a dark
> `#0A0A0B` background with a single <accent color> accent; soft studio
> lighting; no on-screen text, no logos, no people (unless specified).
> **Camera:** one continuous slow <push-in | orbit | pan>, locked horizon,
> absolutely no cuts.
> **Motion:** smooth, constant speed throughout — this will be scrubbed by
> scroll, so no speed ramps, no flicker.
> **Specs:** 5–8 seconds, 16:9, highest detail.

Tell the user: paste into the Gemini app, download the mp4, drop it in
`workspace/references/video/`, then run `/atelier:build` to continue — the
pipeline handles frames automatically. If Gemini refuses, simplify the Subject
line (concrete object, neutral scene) and retry once.

## Image generation — pick the model by job (same credential ladder)

| Model ID | Speed / cost | Use for |
|----------|-------------|---------|
| `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite) | sub-2s, cheapest, 1K max | **bulk + drafts**: storyboard frames, icon/variant batches, layout comps, anything iterated fast; supports multi-turn local edits |
| `gemini-3.1-flash-image` | fast, up to 4K, strong text rendering | **default** for final site imagery and logos |
| `gemini-3-pro-image` | slow, premium | complex hero compositions only |

`gemini-2.5-flash-image` is legacy — never use it in new work. For
storytelling, offer the user the Lite option explicitly: a 20–30 frame
storyboard costs ~$1 and lands in under a minute, then regenerate only the
keeper frames on the default model.

## Logo & brand-mark generation (same ladder, image models)

When a project needs a logo/mark: rung 1–2 call the Gemini image models
above with the same credentials (`GOOGLE_API_KEY`, or Vertex with
service-account creds); rung 3 emit the universal prompt below for ANY
platform (Gemini app, ChatGPT/DALL·E, Midjourney). Always generate light + dark variants, convert to webp, and
check crispness at 16px. The mark must obey design-law: flat vector look,
hairline geometry, near-monochrome + the project's ONE accent — never
gradients, 3D, or mascots.

**Universal logo prompt (fill the brackets, works on every platform):**

> Minimal geometric logo mark for "<NAME>", a premium <what it does> company.
> Concept: <one visual idea tied to what the company means — e.g. "a loop
> whose final segment resolves into a filled square: iteration reaching
> done">. Style: Swiss / International Typographic Style, flat vector, thin
> hairline strokes of consistent 1.5px optical weight like an architectural
> schematic, generous negative space; no gradients, no 3D, no shadows, no
> mascots, no extra glyphs. Colors: ink-black strokes on off-white #FAFAF8
> with exactly ONE small filled element in <ACCENT HEX>. Must stay crisp at
> 16px favicon size. Second variant: dark mode — off-white #F5F5F3 strokes on
> near-black #0A0A0B, same accent element. Optional lockup: wordmark
> "<NAME>" in a grotesk sans, weight 500–600, all caps, +6–8% letter-spacing.

If the output has clutter, append: "absolutely no background texture, no
reflections — mark and wordmark only," and retry once.
