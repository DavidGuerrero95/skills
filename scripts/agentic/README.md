# Agentic hook scripts

These scripts are intentionally lightweight, conservative, and
stateless. They implement the contracts defined under
`/memory/hooks/`. The hook configuration lives in
`.claude/settings.json` (Claude Code) and `.codex/hooks.json` (Codex).

## Goals

- Provide safe, deterministic hook behavior.
- Avoid hiding major behavior changes from the user.
- Emit reminders or guardrail decisions as `systemMessage` payloads.
- Remain easy to inspect and edit.

## Inventory

| Script                              | Hook contract                                  | Trigger                                     |
| ----------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| `prompt_memory_reminder.py`         | `/memory/hooks/prompt-memory-reminder.md`      | `SessionStart`                              |
| `pre_bash_safety_guard.py`          | `/memory/hooks/pre-bash-safety-guard.md`       | `PreToolUse` (Bash)                         |
| `pre_write_secret_scan.py`          | `/memory/hooks/pre-write-secret-scan.md`       | `PreToolUse` (Edit, Write, apply_patch)     |
| `post_edit_code_quality.py`         | `/memory/hooks/post-edit-code-quality.md`      | `PostToolUse` (Edit, Write, apply_patch)    |
| `post_task_docs_sync.py`            | `/memory/hooks/post-task-docs-sync.md`         | `Stop`                                      |
| `session_end_orphan_check.py`       | `/memory/hooks/session-end-orphan-check.md` and `/memory/hooks/subagent-stop-summary.md` | `Stop`, `SessionEnd`, `SubagentStop` |

## Notes

- All scripts read JSON from stdin when invoked as hooks.
- All scripts write a JSON object to stdout.
- They are best-effort helpers, not perfect enforcement boundaries.
- Adjust the Python interpreter (`python3` vs `python`) for your shell
  if needed; on Windows the harness runs the scripts via the
  configured Python launcher.

## Local smoke

```bash
echo '{}' | python3 scripts/agentic/prompt_memory_reminder.py
echo '{}' | python3 scripts/agentic/pre_bash_safety_guard.py
# (Replace the placeholder with a real-looking shape locally to test the deny path.)
echo '{"tool_input": {"file_path": "src/X.java", "content": "<your-fake-key-here>"}}' \
  | python3 scripts/agentic/pre_write_secret_scan.py
echo '{}' | python3 scripts/agentic/post_edit_code_quality.py
echo '{}' | python3 scripts/agentic/post_task_docs_sync.py
echo '{}' | python3 scripts/agentic/session_end_orphan_check.py
```
