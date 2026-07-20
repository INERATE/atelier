"""Paste-prompt (ladder rung 3) — data, not logic. Mirrors skills/asset-pipeline."""

TEMPLATE = """Generate a short video for a website scroll animation.
{audio}
Subject: {subject}
Style: premium industrial minimalism; near-monochrome palette on a dark #0A0A0B
background with a single {accent} accent; soft studio lighting; no on-screen
text, no logos, no people.
Camera: one continuous slow {camera}, locked horizon, absolutely no cuts.
Motion: smooth, constant speed throughout - this will be scrubbed by scroll, so
no speed ramps, no flicker.
Specs: {seconds} seconds, 16:9, highest detail."""


NO_AUDIO = "Audio: none - this is silent scroll-scrubbed background footage."


def build(subject, accent="emerald", camera="push-in", seconds="5-8", audio=False):
    """audio: False for scrollytelling (scrubbed video can't play sound), or a
    string describing the soundscape. Veo 3+ generates synced audio natively."""
    return TEMPLATE.format(
        subject=subject, accent=accent, camera=camera, seconds=seconds,
        audio=NO_AUDIO if not audio else f"Audio: {audio}",
    )
