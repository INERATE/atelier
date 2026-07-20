"""Omni Flash video via the Vertex `interactions` endpoint.

NOT predictLongRunning - a different API shape entirely (probing it the Veo
way 404s, which reads as "model missing" but is not). Shape mirrors the
google-genai SDK: client.interactions.create(model=..., input=[...]).
"""
import base64, json, os, urllib.request

MODEL = "gemini-omni-flash-preview"
# Required: the interactions API is revision-pinned; omitting it 400s/404s.
API_REVISION = "2026-05-20"
URL = ("https://aiplatform.googleapis.com/v1beta1/projects/{proj}"
       "/locations/global/interactions")


def _from_gcs(uri):
    from google.cloud import storage
    bucket, blob = uri[len("gs://"):].split("/", 1)
    return storage.Client().bucket(bucket).blob(blob).download_as_bytes()


def _video_bytes(data):
    """Video arrives inline as base64 `data` OR as a gs:// `uri` - handle both.
    Handling only `data` silently drops successful GCS-delivered results."""
    for step in data.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for c in step.get("content", []):
            if c.get("type") != "video":
                continue
            if c.get("data"):
                return base64.b64decode(c["data"])
            if c.get("uri"):
                return _from_gcs(c["uri"])
    return None


def generate(prompt, out, token, proj):
    """Returns MODEL on success, None if Omni returned no video."""
    body = {"model": MODEL,
            "input": [{"type": "user_input",
                       "content": [{"type": "text", "text": prompt}]}]}
    req = urllib.request.Request(
        URL.format(proj=proj), json.dumps(body).encode(),
        {"Authorization": f"Bearer {token}",
         "Api-Revision": API_REVISION,
         "Content-Type": "application/json; charset=utf-8"},
    )
    vid = _video_bytes(json.load(urllib.request.urlopen(req)))
    if not vid:
        return None
    with open(out, "wb") as f:
        f.write(vid)
    return MODEL
