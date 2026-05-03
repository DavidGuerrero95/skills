#!/usr/bin/env python3
import json, subprocess, sys

def changed():
    try:
        out = subprocess.check_output(["git", "diff", "--name-only"], text=True).strip()
        return [x for x in out.splitlines() if x.strip()]
    except Exception:
        return []

files = changed()
code_touched = any(f.endswith((".java", ".sql", ".yaml", ".yml", ".sh", ".py")) for f in files)
docs_touched = any(f.startswith("docs/") or f.endswith(".md") for f in files)

msg = None
if code_touched and not docs_touched:
    msg = "Code changed without doc updates. Check whether README, ADRs, runbooks, Mermaid diagrams, or contract docs must be updated."

sys.stdout.write(json.dumps({"systemMessage": msg} if msg else {}))
