#!/usr/bin/env python3
"""Session-start reminder: /memory is canonical; adapters are pointers.

Contract: see /memory/hooks/prompt-memory-reminder.md
"""
import json
import sys

sys.stdout.write(json.dumps({
    "systemMessage": (
        "Use /memory as the canonical instruction source (README.md, "
        "MANIFEST.md, policies/, rules/, stacks/, skills/, agents/). "
        "Runtime adapters (.claude/, .codex/, .cursor/, .agents/, and the "
        "Copilot instructions under .github/) are thin pointers — do not "
        "add duplicated rules there."
    )
}))
