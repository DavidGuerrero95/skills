# Hook — post-edit code quality

## Purpose

After a file edit, surface the next validation step the agent should
take and (when configured) trigger a lightweight smell / test
reminder. The implementation is in
`scripts/agentic/post_edit_code_quality.py`.

## Trigger

- Claude Code `PostToolUse` matching `Edit|Write`.
- Codex `PostToolUse` matching `Edit|Write|^apply_patch$`.

## Responsibilities

- Inspect changed file types via `git diff --name-only`.
- Hint at the smallest meaningful next validation:
  - `.java` ⇒ recommend targeted unit/integration tests + smell pass.
  - `.sql / .yaml / .yml` ⇒ recommend re-checking environment
    assumptions, contract impact, doc updates.
  - `.md` ⇒ recommend cross-checking documentation against
    implementation.
- **Never run validation commands itself.** The hook only emits a
  reminder; the main agent decides whether to run the command.

## Must not do

- Block tool execution.
- Rewrite the diff.
- Run heavy commands (build, test, smoke) inside the hook.

## Output contract

Hook stdout is a JSON payload of the form
`{"systemMessage": "..."}` (or `{}` when there is nothing to surface).

## Idempotency

The hook is stateless. It re-evaluates `git diff` on every invocation
and emits at most one short message per matching change set.
