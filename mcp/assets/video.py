"""AI video ladder. Rung 1 Gemini API -> 2 Vertex -> 3 paste-prompt.
Never exits nonzero on missing credentials: rung 3 IS a success path.

MODEL CHOICE IS DRIVEN BY AUDIO. Omni Flash has no audio track; only Veo 3+
generates synced sound. audio=True therefore forces Veo everywhere.
"""
import json, os, sys, urllib.request
import video_vertex
from video_http import post, poll
from video_prompt import build

GEM = "https://generativelanguage.googleapis.com/v1beta"


def _gemini(prompt, key, out, audio=False):
    body = {"instances": [{"prompt": prompt}],
            "parameters": {"aspectRatio": "16:9", "generateAudio": bool(audio)}}
    hdr = {"Content-Type": "application/json"}
    for m in video_vertex.VEO:
        try:
            op = post(f"{GEM}/models/{m}:predictLongRunning?key={key}", body, hdr)
        except Exception:
            continue  # model not on this key; try the next one
        op = poll(lambda: json.load(urllib.request.urlopen(
            f"{GEM}/{op['name']}?key={key}")))
        uri = op["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
        with urllib.request.urlopen(f"{uri}&key={key}") as r, open(out, "wb") as f:
            f.write(r.read())
        return m
    return None


def generate(subject, out="generated.mp4", audio=False, **kw):
    """Returns (rung, detail). rung 3 means: no creds, hand the prompt over.

    audio=False -> silent; fine for scroll-scrubbed scrollytelling, and lets
    the cheaper Omni serve it. audio="<soundscape>" -> forces Veo 3+.
    ASK the user which they want; never inherit silence by default.
    """
    prompt = build(subject, audio=audio, **kw)
    key = os.getenv("GOOGLE_API_KEY")
    if key:
        m = _gemini(prompt, key, out, audio)
        if m:
            return 1, m
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            m = video_vertex.generate(prompt, out, audio)
            if m:
                return 2, m
        except Exception as e:
            print(f"vertex unavailable: {e}", file=sys.stderr)
    return 3, prompt


if __name__ == "__main__":
    a = sys.argv[1:]
    subject = a[0] if a else "a slow orbit around a matte black cube"
    rung, detail = generate(subject, audio=a[1] if len(a) > 1 else False)
    print(f"rung {rung}\n{detail}")
