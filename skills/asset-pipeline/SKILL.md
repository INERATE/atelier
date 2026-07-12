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
- Both record `asset_manifest` rows. Serve only webp to browsers.

## Scrollytelling recipe (the storytelling primitive)

1. Get an mp4 (user-provided in `workspace/references/video/`, or generate — below).
2. `assets.py frames video.mp4 24` → `video_frames/frame_0001.webp …`
3. Copy frames to `public/frames/<name>/`; use `templates/ScrollScrub.tsx`
   (canvas scrub, sticky viewport). `prefers-reduced-motion` → static poster.
4. Design-law still applies: ONE hero moment per page.

## AI video generation — the ladder (never exit on missing credentials)

| Rung | Needs | Model |
|------|-------|-------|
| 1. Public Gemini API | `GOOGLE_API_KEY` | `gemini-omni-flash-preview` (live since 2026-06-30); Veo 3.1 fallback |
| 2. Vertex AI | `GOOGLE_APPLICATION_CREDENTIALS` (service-account JSON path) + `GOOGLE_CLOUD_PROJECT` + `GOOGLE_CLOUD_LOCATION` | Veo 3.1 now; Omni Flash as Vertex rollout completes |
| 3. **No credentials** | nothing | Emit the paste-prompt below for the user's Gemini app (Omni Flash powers it for subscribers). NOT an error — say "no token, continuing" and proceed. |
| 4. Nothing works | — | Ask the user to drop any mp4 into `workspace/references/video/`. |

Credentials live in the project `.env` (gitignored — verify), written at
bootstrap. Standard var names above (they match gcloud/Vertex conventions).
Never store keys in the SQLite store or any committed file.

## The paste-prompt (rung 3 — write it FOR the user, filled in)

> Generate a short video, no audio, for a website scroll animation.
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
