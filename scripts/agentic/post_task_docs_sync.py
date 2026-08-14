#!/usr/bin/env python3
"""Post-task docs-sync reminder hook (stack-agnostic).

If code-bearing files changed without a matching doc update, emit a
one-line reminder. It never edits docs or runs validation.

Contract: see /memory/hooks/post-task-docs-sync.md
"""
import json
import subprocess
import sys

CODE_EXT = (
    ".java", ".kt", ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs",
    ".rb", ".cs", ".scala", ".php", ".sql", ".yaml", ".yml", ".toml", ".sh",
)


def changed():
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only"], text=True
        ).strip()
        return [x for x in out.splitlines() if x.strip()]
    except Exception:
        return []


def main():
    files = changed()
    code_touched = any(f.endswith(CODE_EXT) for f in files)
    docs_touched = any(f.startswith("docs/") or f.endswith(".md") for f in files)

    msg = None
    if code_touched and not docs_touched:
        msg = (
            "Code changed without doc updates. Check whether README, ADRs, "
            "runbooks, Mermaid diagrams, or contract docs must be updated "
            "(see policies/07-documentation-and-traceability.md)."
        )
    sys.stdout.write(json.dumps({"systemMessage": msg} if msg else {}))


if __name__ == "__main__":
    main()
