"""Vertex rung: service-account auth, Omni-or-Veo choice, predictLongRunning."""
import base64, os, sys
import video_omni
from video_http import post, poll

# GA first, then fast preview, then the deprecated 3.0 as a last resort.
# veo-3.0-generate-001 was slated for discontinuation 2026-06-30 - it still
# answers for some projects but must not be the primary target.
VEO = ["veo-3.1-generate-001", "veo-3.1-fast-generate-preview",
       "veo-3.0-generate-001"]


def _auth():
    import google.auth  # only needed on this rung
    from google.auth.transport.requests import Request
    cred, proj = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    cred.refresh(Request())
    return cred.token, os.getenv("GOOGLE_CLOUD_PROJECT", proj)


def generate(prompt, out, audio=False):
    token, proj = _auth()
    if not audio:  # Omni is faster/cheaper but silent-only, so never for audio
        try:
            m = video_omni.generate(prompt, out, token, proj)
            if m:
                return m
        except Exception as e:
            print(f"omni unavailable, using veo: {e}", file=sys.stderr)
    loc = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    base = (f"https://{loc}-aiplatform.googleapis.com/v1/projects/{proj}"
            f"/locations/{loc}/publishers/google/models")
    hdr = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for m in VEO:
        try:
            op = post(f"{base}/{m}:predictLongRunning",
                      {"instances": [{"prompt": prompt}],
                       "parameters": {"aspectRatio": "16:9", "sampleCount": 1,
                                      "generateAudio": bool(audio)}}, hdr)
        except Exception:
            continue
        done = poll(lambda: post(f"{base}/{m}:fetchPredictOperation",
                                 {"operationName": op["name"]}, hdr))
        vid = done["response"]["videos"][0]
        with open(out, "wb") as f:
            f.write(base64.b64decode(vid["bytesBase64Encoded"]))
        return m
    return None
