"""Measure generated media instead of eyeballing it.

Catches the two defects that shipped before: video that looks fine but is
silent, and video that obeys the palette in words while flooding the frame
with accent. Both were only found by measuring - do this every generation.
"""
import json, re, subprocess, sys


def audio(path):
    """(has_stream, mean_dB). Real audio ~ -30..-10 dB; silence reads -91/-inf."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
         "stream=codec_name", "-of", "json", path],
        capture_output=True, text=True)
    if not json.loads(probe.stdout or "{}").get("streams"):
        return False, None
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", out)
    db = m.group(1) if m else None
    return True, (None if db in (None, "-inf") else float(db))


def accent_ratio(path, hex_color, tol=60):
    """Fraction of pixels near the accent. Design law caps it at 0.10."""
    from PIL import Image
    r0, g0, b0 = (int(hex_color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    if path.lower().endswith((".mp4", ".mov", ".webm")):
        subprocess.run(["ffmpeg", "-y", "-i", path, "-vf", "thumbnail",
                        "-frames:v", "1", "_probe.png"], capture_output=True)
        path = "_probe.png"
    im = Image.open(path).convert("RGB").resize((320, 180))
    px = list(im.getdata())
    hit = sum(1 for r, g, b in px
              if (r - r0) ** 2 + (g - g0) ** 2 + (b - b0) ** 2 < tol ** 2)
    return hit / len(px)


def report(path, hex_color="#10B981", want_audio=False):
    """Prints PASS/FAIL per check. Returns True only if every check passed."""
    has, db = audio(path)
    ratio = accent_ratio(path, hex_color)
    audible = has and db is not None and db > -60
    ok_audio = audible if want_audio else True
    ok_accent = ratio <= 0.10
    print(f"audio: stream={has} mean={db} dB -> "
          f"{'PASS' if ok_audio else 'FAIL (asked for sound, got silence)'}")
    print(f"accent: {ratio:.1%} -> {'PASS' if ok_accent else 'FAIL (cap 10%)'}")
    return ok_audio and ok_accent


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(0 if report(a[0], *(a[1:] or ["#10B981"]),
                         want_audio="--audio" in a) else 1)
