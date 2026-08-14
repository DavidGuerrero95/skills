# Hook — post-edit code quality

## Purpose

After a file edit, surface the next validation step the agent should
take. The implementation is in
`scripts/agentic/post_edit_code_quality.py` and is stack-agnostic.

## Trigger

- Claude Code `PostToolUse` matching `Edit|Write`.
- Codex `PostToolUse` matching `Edit|Write|^apply_patch$`.

## Responsibilities

- Inspect changed file types via `git diff --name-only`.
- Hint at the smallest meaningful next validation, by category:
  - **Source code** (`.java`, `.kt`, `.py`, `.ts`, `.js`, `.go`,
    `.rs`, …) ⇒ recommend targeted unit/integration tests + a
    lint/smell pass.
  - **Schema / config** (`.sql`, `.yaml`, `.yml`, `.toml`, migration
    files) ⇒ recommend re-checking environment assumptions, contract
    impact, and doc updates.
  - **Docs** (`.md`) ⇒ recommend cross-checking documentation against
    implementation.
- **Never run validation commands itself.** The hook only emits a
  reminder; the main agent decides whether to run the command.

## Must not do

- Block tool execution.
- Rewrite the diff.
- Run heavy commands (build, test, smoke) inside the hook.

## Output contract

Hook stdout is `{"systemMessage": "..."}` (or `{}` when there is nothing
to surface).

## Idempotency

Stateless. Re-evaluates `git diff` on every invocation and emits at most
one short message per matching change set.
