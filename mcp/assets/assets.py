#!/usr/bin/env python3
"""Atelier asset pipeline CLI.

  assets.py webp <image> [quality=82]        any raster -> .webp beside it
  assets.py frames <video> [fps=24] [q=80]   mp4 -> webp frame sequence (ffmpeg)
  assets.py cut <image> [tol=32]             flat background -> transparent webp

Records results in workspace/atelier.db asset_manifest when present.
ponytail: direct CLI; wrap as MCP/gRPC worker only if batch volume demands it.
"""
import os, sqlite3, subprocess, sys


def manifest(src, out, kind, b0, b1):
    db = os.path.join(os.getcwd(), "workspace", "atelier.db")
    if os.path.exists(db):
        c = sqlite3.connect(db)
        c.execute("INSERT INTO asset_manifest (src,out,kind,bytes_before,bytes_after)"
                  " VALUES (?,?,?,?,?)", (src, out, kind, b0, b1))
        c.commit()


def webp(path, quality=82):
    from PIL import Image
    out = os.path.splitext(path)[0] + ".webp"
    Image.open(path).convert("RGBA").save(out, "WEBP", quality=quality, method=6)
    b0, b1 = os.path.getsize(path), os.path.getsize(out)
    manifest(path, out, "image", b0, b1)
    print(f"ok|{out}|{b0}->{b1}B ({100 - b1 * 100 // max(b0, 1)}% smaller)")


def frames(path, fps=24, quality=80):
    outdir = os.path.splitext(path)[0] + "_frames"
    os.makedirs(outdir, exist_ok=True)
    try:
        r = subprocess.run(["ffmpeg", "-y", "-i", path, "-vf", f"fps={fps},scale=1600:-2",
                            "-quality", str(quality), os.path.join(outdir, "frame_%04d.webp")],
                           capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("ffmpeg not installed (winget install Gyan.FFmpeg) — skipping frames, other work can continue")
    if r.returncode:
        sys.exit(f"ffmpeg failed: {r.stderr[-200:]}")
    n = len(os.listdir(outdir))
    manifest(path, outdir, "video", os.path.getsize(path), n)
    print(f"ok|{outdir}|{n} frames @ {fps}fps")


def cut(path, tol=32):
    # ponytail: corner-color threshold — right for flat logo/icon bg; photos need rembg
    from PIL import Image
    img = Image.open(path).convert("RGBA")
    px, (w, h) = img.load(), img.size
    bg = px[0, 0]
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) <= tol * 3:
                px[x, y] = (p[0], p[1], p[2], 0)
    out = os.path.splitext(path)[0] + "_cut.webp"
    img.save(out, "WEBP", lossless=True)
    manifest(path, out, "image", os.path.getsize(path), os.path.getsize(out))
    print(f"ok|{out}|transparent")


if __name__ == "__main__":
    a = sys.argv
    if len(a) > 2 and a[1] == "webp":
        webp(a[2], int(a[3]) if len(a) > 3 else 82)
    elif len(a) > 2 and a[1] == "frames":
        frames(a[2], int(a[3]) if len(a) > 3 else 24)
    elif len(a) > 2 and a[1] == "cut":
        cut(a[2], int(a[3]) if len(a) > 3 else 32)
    else:
        print(__doc__)
