#!/usr/bin/env python3
"""Post-edit code-quality reminder hook (stack-agnostic).

Reads changed files from git and emits a single short reminder about the
smallest meaningful next validation. It never runs validation itself.

Contract: see /memory/hooks/post-edit-code-quality.md
"""
import json
import subprocess
import sys

CODE_EXT = (
    ".java", ".kt", ".py", ".ts", ".tsx", ".js", ".jsx",
    ".go", ".rs", ".rb", ".cs", ".scala", ".php",
)
SCHEMA_CONFIG_EXT = (".sql", ".yaml", ".yml", ".toml", ".properties")


def git_changed():
    files = []
    for args in (
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
    ):
        try:
            out = subprocess.check_output(args, text=True).strip()
            files.extend(x for x in out.splitlines() if x.strip())
        except Exception:
            pass
    return sorted(set(files))


def main():
    changed = git_changed()
    msg = None
    if any(p.endswith(CODE_EXT) for p in changed):
        msg = (
            "Source files changed. Run targeted unit/integration tests for "
            "the touched module and consider a lint/smell pass."
        )
    elif any(p.endswith(SCHEMA_CONFIG_EXT) for p in changed):
        msg = (
            "Schema/config files changed. Re-check environment assumptions, "
            "contract impact, and whether docs must be updated."
        )
    elif any(p.endswith(".md") for p in changed):
        msg = (
            "Documentation files changed. Verify they still match the "
            "implemented behavior."
        )
    sys.stdout.write(json.dumps({"systemMessage": msg} if msg else {}))


if __name__ == "__main__":
    main()
