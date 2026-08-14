#!/usr/bin/env python3
"""Validate the agentic baseline integrity.

Checks that every runtime adapter is a thin pointer to an existing
canonical file under /memory, and that no adapter references a canonical
file that no longer exists. Exits non-zero on any problem so CI fails.

Run: python3 scripts/validate_baseline.py
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors: list[str] = []


def canonical_exists(rel: str) -> bool:
    return os.path.isfile(os.path.join(ROOT, rel.lstrip("/")))


def check_pointers(pattern: str, kind: str) -> int:
    n = 0
    for path in glob.glob(os.path.join(ROOT, pattern), recursive=True):
        n += 1
        text = open(path, encoding="utf-8").read()
        refs = re.findall(r"`(/memory/[^`]+)`", text)
        refs = [r for r in refs if r.endswith((".md", "SKILL.md"))]
        if not refs:
            errors.append(f"[{kind}] {os.path.relpath(path, ROOT)}: no /memory pointer found")
            continue
        for r in refs:
            if not canonical_exists(r):
                errors.append(
                    f"[{kind}] {os.path.relpath(path, ROOT)}: dangling pointer -> {r}"
                )
    return n


def check_canonical_present() -> None:
    required_dirs = [
        "memory/policies", "memory/rules", "memory/stacks", "memory/skills",
        "memory/agents", "memory/hooks", "memory/commands", "memory/output-styles",
    ]
    for d in required_dirs:
        if not os.path.isdir(os.path.join(ROOT, d)):
            errors.append(f"[structure] missing canonical dir: {d}")
    for f in ["memory/README.md", "memory/MANIFEST.md", "CLAUDE.md", "AGENTS.md"]:
        if not os.path.isfile(os.path.join(ROOT, f)):
            errors.append(f"[structure] missing required file: {f}")


def check_hooks_have_impl() -> None:
    for path in glob.glob(os.path.join(ROOT, "memory/hooks/*.md")):
        text = open(path, encoding="utf-8").read()
        for impl in re.findall(r"`scripts/agentic/([A-Za-z0-9_]+\.py)`", text):
            if not os.path.isfile(os.path.join(ROOT, "scripts/agentic", impl)):
                errors.append(
                    f"[hooks] {os.path.relpath(path, ROOT)}: missing impl scripts/agentic/{impl}"
                )


def main() -> int:
    check_canonical_present()
    check_hooks_have_impl()
    counts = {
        "claude-agents": check_pointers(".claude/agents/*.md", "claude"),
        "claude-skills": check_pointers(".claude/skills/*/SKILL.md", "claude"),
        "claude-commands": check_pointers(".claude/commands/*.md", "claude"),
        "claude-styles": check_pointers(".claude/output-styles/*.md", "claude"),
        "codex-skills": check_pointers(".codex/skills/*/SKILL.md", "codex"),
        "codex-policies": check_pointers(".codex/policies/*.md", "codex"),
        "cursor-rules": check_pointers(".cursor/rules/*.mdc", "cursor"),
        "agents-skills": check_pointers(".agents/skills/*/SKILL.md", "agents"),
        "copilot": check_pointers(".github/instructions/*.instructions.md", "copilot"),
    }

    print("Adapter pointer counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

    if errors:
        print("\nBASELINE VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nBaseline OK: all adapters point to existing canonical files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
