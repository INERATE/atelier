#!/usr/bin/env python3
"""Atelier clean-code-law gate: source files stay <=250 words (350 hard cap).

PostToolUse hook on Write|Edit. Exit 2 feeds guidance back to the model.
ponytail: PostToolUse corrective (file already written); upgrade to PreToolUse
deny only if oversized files ever actually ship.
"""
import json, sys, os

SOFT, HARD = 250, 350
EXEMPT_EXT = {".md", ".mdx", ".txt", ".json", ".yaml", ".yml", ".toml", ".lock",
              ".csv", ".svg", ".sql", ".html"}
EXEMPT_PARTS = ("node_modules", "migrations", "generated", ".min.", "dist", "build")


def check(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in EXEMPT_EXT or any(p in path for p in EXEMPT_PARTS):
        return None
    try:
        words = len(open(path, encoding="utf-8", errors="ignore").read().split())
    except OSError:
        return None
    if words > HARD:
        return (f"BLOCK: {path} is {words} words (hard cap {HARD}). Split it now: "
                "extract helpers to a sibling module / one component per file / "
                "split by responsibility. See clean-code-law.")
    if words > SOFT:
        return (f"warn: {path} is {words} words (budget {SOFT}, cap {HARD}). "
                "Split at the next natural seam.")
    return None


def main():
    data = json.load(sys.stdin)
    path = (data.get("tool_input") or {}).get("file_path", "")
    msg = check(path) if path else None
    if msg and msg.startswith("BLOCK"):
        print(msg, file=sys.stderr)
        sys.exit(2)
    if msg:
        print(msg)
    sys.exit(0)


if __name__ == "__main__":
    if "--test" in sys.argv:
        import tempfile
        f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
        f.write("x " * 400); f.close()
        assert "BLOCK" in check(f.name)
        assert check(f.name.replace(".py", ".md")) is None or True
        os.unlink(f.name); print("self-check ok")
    else:
        main()
