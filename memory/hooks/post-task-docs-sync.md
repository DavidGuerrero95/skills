# Hook — post-task docs sync

## Purpose

When a task ends and code changed without a matching doc update,
generate a reminder pointing the agent at the affected docs (README,
ADRs, runbooks, diagrams, contract docs). Implementation:
`scripts/agentic/post_task_docs_sync.py`.

## Trigger

- Claude Code `Stop`.
- Codex `Stop`.

## Responsibilities

- Inspect `git diff --name-only`.
- If code-bearing files changed (`.java`, `.sql`, `.yaml`, `.yml`,
  `.sh`, `.py`) **and** no doc file changed (`.md`, `docs/...`), emit
  a one-line reminder.
- Suggest concrete doc surfaces to check, per
  `policies/07-documentation-and-traceability.md`.

## Must not do

- Edit documentation itself.
- Run validation commands.
- Block the Stop event.

## Output contract

Hook stdout is `{"systemMessage": "..."}` or `{}`.

## Idempotency

Stateless. Re-evaluates the diff on every Stop. The same diff produces
the same reminder.
