#!/usr/bin/env python3
"""Pre-write secret scan hook.

Reads the tool input from stdin and inspects it for obviously
secret-shaped strings (API keys, tokens, JDBC URLs with credentials,
PEM private keys). Emits a deny decision when a high-confidence match
is found in a path that should not contain secrets.

Contract: see /memory/hooks/pre-write-secret-scan.md
"""
from __future__ import annotations

import json
import re
import sys


DENY_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained PAT"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "PEM private key"),
    (r"jdbc:[a-z]+://[^\s\"'<>` ]*:[^@\s\"'<>` ]+@", "JDBC URL with embedded credentials"),
    (r"\b[0-9]{8,12}:AA[A-Za-z0-9_\-]{30,}\b", "Telegram bot token"),
]

PLACEHOLDER_SAFE_SUFFIXES = (
    ".env.example",
    "/test/",
    "/tests/",
    "Test.java",
    "Tests.java",
    ".md",
)

PLACEHOLDER_HINTS = ("REDACTED", "your-", "xxxxxx", "placeholder")


def _emit(payload):
    sys.stdout.write(json.dumps(payload))


def _is_placeholder_safe(path, content):
    if not path:
        return False
    if any(path.endswith(s) or s in path for s in PLACEHOLDER_SAFE_SUFFIXES):
        if any(hint.lower() in content.lower() for hint in PLACEHOLDER_HINTS):
            return True
    return False


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        _emit({})
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        _emit({})
        return

    tool_input = data.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or tool_input.get("path")

    candidate = ""
    for key in ("content", "new_string", "patch", "text"):
        value = tool_input.get(key)
        if isinstance(value, str):
            candidate += "\n" + value

    if not candidate.strip():
        _emit({})
        return

    for pattern, label in DENY_PATTERNS:
        match = re.search(pattern, candidate)
        if not match:
            continue
        if _is_placeholder_safe(path, candidate):
            _emit({
                "systemMessage": (
                    "Possible " + label + "-shaped placeholder in " + str(path)
                    + ". Confirm it is a documented placeholder, not a real secret."
                )
            })
            return
        snippet = match.group(0)[:24]
        _emit({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Likely " + label + " detected in payload (prefix: "
                    + snippet + "...). Move the secret to env vars and reference it via .env.example."
                ),
            }
        })
        return

    _emit({})


if __name__ == "__main__":
    main()
