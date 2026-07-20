"""Smallest check that fails if the ladder breaks. No network, no credentials."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import video


def test_rung3_when_no_credentials(monkeypatch=None):
    for k in ("GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ.pop(k, None)
    rung, prompt = video.generate("a matte black cube")
    assert rung == 3, "missing creds must fall to the paste-prompt, not error"
    assert "matte black cube" in prompt
    assert "no cuts" in prompt and "16:9" in prompt


def test_bad_key_still_falls_through():
    os.environ["GOOGLE_API_KEY"] = "invalid-key"
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    rung, _ = video.generate("a matte black cube")
    assert rung == 3, "an invalid key must degrade to rung 3, not crash"


def test_audio_reaches_the_request_body():
    """The v0.3.3 bug: prompt said 'no audio' and generateAudio was never sent,
    so every video came back silent with no way to ask for sound."""
    sent = {}
    video.post = lambda url, body, hdr: sent.update(body) or (_ for _ in ()).throw(
        RuntimeError("stop after capture"))
    os.environ["GOOGLE_API_KEY"] = "x"
    video.generate("a cube", audio="low industrial hum")
    assert sent["parameters"]["generateAudio"] is True, sent
    assert "industrial hum" in sent["instances"][0]["prompt"]


def test_silent_omni_result_falls_through_to_veo():
    """Whether Omni returns audio is disputed in Google's own docs, so the
    rule is measured, not assumed: if an audio request comes back silent,
    it must reach Veo instead of being handed over as a silent file."""
    import video_omni, video_vertex
    reached = []
    video_omni.generate = lambda *a: "gemini-omni-flash-preview"
    video_vertex._has_audio = lambda p: False  # Omni gave us silence
    video_vertex._auth = lambda: ("token", "proj")
    video_vertex._playable = lambda p: True
    video_vertex.post = lambda url, body, hdr: reached.append(url) or (
        _ for _ in ()).throw(RuntimeError("stop at veo"))
    try:
        video_vertex.generate("a cube", "out.mp4", audio="a hum")
    except Exception:
        pass
    assert reached, "silent Omni output must fall through to Veo"
    assert "veo-3.1-generate-001" in reached[0], reached


def test_silent_omni_is_fine_when_no_audio_wanted():
    import video_omni, video_vertex
    video_omni.generate = lambda *a: "gemini-omni-flash-preview"
    video_vertex._auth = lambda: ("token", "proj")
    video_vertex._playable = lambda p: True
    assert video_vertex.generate("a cube", "out.mp4") == "gemini-omni-flash-preview"


if __name__ == "__main__":
    test_rung3_when_no_credentials()
    test_bad_key_still_falls_through()
    test_audio_reaches_the_request_body()
    test_silent_omni_result_falls_through_to_veo()
    test_silent_omni_is_fine_when_no_audio_wanted()
    print("ok")
