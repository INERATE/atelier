"""AI video generation ladder. Rung 1 Gemini API -> 2 Vertex -> 3 paste-prompt.
Never exits nonzero on missing credentials: rung 3 IS a success path."""
import base64, json, os, sys, time, urllib.request
from video_prompt import build

GEM = "https://generativelanguage.googleapis.com/v1beta"
MODELS = ["gemini-omni-flash-preview", "veo-3.1-generate-preview"]


def _post(url, body, headers):
    req = urllib.request.Request(url, json.dumps(body).encode(), headers)
    return json.load(urllib.request.urlopen(req))


def _poll(get, tries=60):
    for _ in range(tries):
        op = get()
        if op.get("done"):
            return op
        time.sleep(10)
    raise TimeoutError("generation did not finish")


def _gemini(prompt, key, out, audio=False):
    body = {"instances": [{"prompt": prompt}],
            "parameters": {"aspectRatio": "16:9", "generateAudio": bool(audio)}}
    hdr = {"Content-Type": "application/json"}
    for m in MODELS:
        try:
            op = _post(f"{GEM}/models/{m}:predictLongRunning?key={key}", body, hdr)
        except Exception:
            continue  # model not on this key; try next rung of the model list
        op = _poll(lambda: json.load(urllib.request.urlopen(
            f"{GEM}/{op['name']}?key={key}")))
        uri = op["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
        with urllib.request.urlopen(f"{uri}&key={key}") as r, open(out, "wb") as f:
            f.write(r.read())
        return m
    return None


def _vertex(prompt, out, audio=False):
    import google.auth  # only needed on this rung
    from google.auth.transport.requests import Request
    cred, proj = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    cred.refresh(Request())
    proj = os.getenv("GOOGLE_CLOUD_PROJECT", proj)
    loc = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    base = (f"https://{loc}-aiplatform.googleapis.com/v1/projects/{proj}"
            f"/locations/{loc}/publishers/google/models")
    hdr = {"Authorization": f"Bearer {cred.token}", "Content-Type": "application/json"}
    for m in ["veo-3.1-generate-preview", "veo-3.0-generate-001"]:
        try:
            op = _post(f"{base}/{m}:predictLongRunning",
                       {"instances": [{"prompt": prompt}],
                        "parameters": {"aspectRatio": "16:9", "sampleCount": 1,
                                       "generateAudio": bool(audio)}}, hdr)
        except Exception:
            continue
        done = _poll(lambda: _post(f"{base}/{m}:fetchPredictOperation",
                                   {"operationName": op["name"]}, hdr))
        vid = done["response"]["videos"][0]
        open(out, "wb").write(base64.b64decode(vid["bytesBase64Encoded"]))
        return m
    return None


def generate(subject, out="generated.mp4", audio=False, **kw):
    """Returns (rung, detail). rung 3 means: no creds, hand the prompt over.
    audio=False is the scrollytelling default (scrubbed video has no playback);
    pass a soundscape string for hero/social video - ASK, never assume silence."""
    prompt = build(subject, audio=audio, **kw)
    key = os.getenv("GOOGLE_API_KEY")
    if key:
        m = _gemini(prompt, key, out, audio)
        if m:
            return 1, m
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            m = _vertex(prompt, out, audio)
            if m:
                return 2, m
        except Exception as e:
            print(f"vertex unavailable: {e}", file=sys.stderr)
    return 3, prompt


if __name__ == "__main__":
    rung, detail = generate(*sys.argv[1:2] or ["a slow orbit around a matte black cube"])
    print(f"rung {rung}\n{detail}")
