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
    video._post = lambda url, body, hdr: sent.update(body) or (_ for _ in ()).throw(
        RuntimeError("stop after capture"))
    os.environ["GOOGLE_API_KEY"] = "x"
    video.generate("a cube", audio="low industrial hum")
    assert sent["parameters"]["generateAudio"] is True, sent
    assert "industrial hum" in sent["instances"][0]["prompt"]


if __name__ == "__main__":
    test_rung3_when_no_credentials()
    test_bad_key_still_falls_through()
    test_audio_reaches_the_request_body()
    print("ok")
