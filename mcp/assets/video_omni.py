"""Omni Flash video via the Vertex `interactions` endpoint.

NOT predictLongRunning - Omni uses a different API shape entirely (probing it
with predictLongRunning 404s, which reads as "model missing" but is not).
Omni has NO audio track: silent video only. Audio work goes to Veo (video.py).
"""
import base64, json, os, urllib.request

MODEL = "gemini-omni-flash-preview"
URL = ("https://aiplatform.googleapis.com/v1beta1/projects/{proj}"
       "/locations/global/interactions")


def _video_bytes(data):
    for step in data.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for c in step.get("content", []):
            if c.get("type") == "video" and c.get("data"):
                return base64.b64decode(c["data"])
    return None


def generate(prompt, out, token, proj):
    """Returns MODEL on success, None if Omni gave no video. Never for audio."""
    req = urllib.request.Request(
        URL.format(proj=proj),
        json.dumps({"model": MODEL,
                    "input": [{"type": "text", "text": prompt}]}).encode(),
        {"Authorization": f"Bearer {token}",
         "Content-Type": "application/json; charset=utf-8"},
    )
    vid = _video_bytes(json.load(urllib.request.urlopen(req)))
    if not vid:
        return None
    with open(out, "wb") as f:
        f.write(vid)
    return MODEL
