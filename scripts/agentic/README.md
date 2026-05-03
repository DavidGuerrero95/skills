# Agentic hook scripts

These scripts are intentionally lightweight and conservative.

## Goals

- provide safe, deterministic hook behavior,
- avoid hiding major behavior changes,
- emit reminders or guardrail decisions,
- remain easy to inspect and edit.

## Notes

- All scripts read JSON from stdin when invoked as hooks.
- They are best-effort helpers, not perfect enforcement boundaries.
- Adjust command paths for your shell/runtime if needed.
