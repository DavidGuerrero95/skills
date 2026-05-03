#!/usr/bin/env python3
import json, re, sys

def output(obj):
    sys.stdout.write(json.dumps(obj))

raw = sys.stdin.read().strip()
data = json.loads(raw) if raw else {}
tool_input = data.get("tool_input", {})
cmd = tool_input.get("command", "") or data.get("command", "")

danger_patterns = [
    r"\brm\s+-rf\s+/(?!tmp\b)",
    r"\brm\s+-rf\s+\.\b",
    r"\bdocker\s+system\s+prune\b",
    r"\bgit\s+push\b.*--force",
    r"\bkubectl\s+delete\s+ns\b",
    r"\bdrop\s+database\b",
]
warn_patterns = [
    r"\brm\s+-rf\b",
    r"\bdocker\s+prune\b",
    r"\bterraform\s+destroy\b",
    r"\bkubectl\s+delete\b",
]

for p in danger_patterns:
    if re.search(p, cmd):
        output({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Blocked risky command: {cmd[:160]}"
            }
        })
        raise SystemExit(0)

for p in warn_patterns:
    if re.search(p, cmd):
        output({
            "systemMessage": (
                "Risky shell command detected. Re-check scope, environment, and blast radius before execution."
            )
        })
        raise SystemExit(0)

output({})
