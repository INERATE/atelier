#!/usr/bin/env python3
"""SessionStart hook: surface the active Atelier plan + unmet criteria so a
fresh/compacted session resumes exactly where work stopped."""
import json, os, sqlite3, sys

DB = os.path.join(os.getcwd(), "workspace", "atelier.db")


def context():
    if not os.path.exists(DB):
        return ""
    c = sqlite3.connect(DB)
    plan = c.execute(
        "SELECT id,title FROM plans WHERE status='active' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if not plan:
        return "Atelier store present; no active plan. /atelier:plan to start."
    unmet = c.execute(
        "SELECT criterion FROM done_criteria WHERE plan_id=? AND passed=0", (plan[0],)
    ).fetchall()
    lines = [f"Atelier active plan #{plan[0]}: {plan[1]}",
             f"Unmet done-criteria ({len(unmet)}):"]
    lines += [f"- {u[0]}" for u in unmet[:12]]
    return "\n".join(lines)


def main():
    out = context()
    if out:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": out}}))
    sys.exit(0)


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert context() is not None
        print("self-check ok")
    else:
        main()
