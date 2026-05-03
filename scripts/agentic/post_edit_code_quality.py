#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

def git_changed():
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", "--cached"], text=True).strip()
        staged = [x for x in out.splitlines() if x.strip()]
    except Exception:
        staged = []
    try:
        out = subprocess.check_output(["git", "diff", "--name-only"], text=True).strip()
        unstaged = [x for x in out.splitlines() if x.strip()]
    except Exception:
        unstaged = []
    return sorted(set(staged + unstaged))

changed = git_changed()
interesting = [p for p in changed if p.endswith((".java", ".kt", ".gradle", ".md", ".yaml", ".yml", ".sql"))]

msg = None
if any(p.endswith(".java") for p in interesting):
    msg = "Java-related files changed. Run targeted unit/integration validation and consider a code-smell review."
elif any(p.endswith((".sql", ".yaml", ".yml")) for p in interesting):
    msg = "Infra/config files changed. Re-check environment assumptions, contract impact, and docs."
elif any(p.endswith(".md") for p in interesting):
    msg = "Documentation files changed. Verify they still match the implemented behavior."

sys.stdout.write(json.dumps({"systemMessage": msg} if msg else {}))
