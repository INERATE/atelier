"""Vertex rung: service-account auth, Omni-or-Veo choice, predictLongRunning."""
import base64, os, sys
import video_omni
from video_http import post, poll

# GA first, then fast preview, then the deprecated 3.0 as a last resort.
# veo-3.0-generate-001 was slated for discontinuation 2026-06-30 - it still
# answers for some projects but must not be the primary target.
VEO = ["veo-3.1-generate-001", "veo-3.1-fast-generate-preview",
       "veo-3.0-generate-001"]


def _playable(path):
    """Omni is preferred, so its output must be checked before we trust it:
    a truncated or empty file would otherwise ship as a 'successful' video."""
    if not os.path.exists(path) or os.path.getsize(path) < 10_000:
        return False
    try:
        import verify
        return verify.has_video(path)
    except Exception:
        return True  # no ffprobe: size check above is all we can prove


def _has_audio(path):
    """Audible, not merely present - a valid AAC track can measure -91 dB."""
    try:
        import verify
        has, db = verify.audio(path)
        return has and db is not None and db > -60
    except Exception:
        return False  # no ffmpeg: can't prove sound, so prefer Veo


def _auth():
    import google.auth  # only needed on this rung
    from google.auth.transport.requests import Request
    cred, proj = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    cred.refresh(Request())
    return cred.token, os.getenv("GOOGLE_CLOUD_PROJECT", proj)


def generate(prompt, out, audio=False):
    token, proj = _auth()
    # Omni is faster/cheaper. Whether it returns an audio track is disputed
    # across Google's own docs, so don't assume either way: try it, then MEASURE
    # the file. Silent result on an audio request -> fall through to Veo.
    try:
        m = video_omni.generate(prompt, out, token, proj)
        if m and _playable(out) and (not audio or _has_audio(out)):
            return m
        if m:
            print("omni output unusable (empty or silent); retrying on veo",
                  file=sys.stderr)
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
