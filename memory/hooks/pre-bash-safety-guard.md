# Hook — pre-bash safety guard

## Purpose

Block obviously destructive shell commands before they execute, and
warn on risky-but-reasonable commands. Implementation:
`scripts/agentic/pre_bash_safety_guard.py`.

## Trigger

- Claude Code `PreToolUse` matching `Bash`.
- Codex `PreToolUse` matching `^Bash$`.

## Responsibilities

### Deny (the hook returns `permissionDecision: deny`)

- `rm -rf /` (or anywhere outside `/tmp`).
- `rm -rf .` at the repo root.
- `docker system prune` (any flags).
- `git push --force ...`.
- `kubectl delete ns ...`.
- `drop database ...` issued through `psql` / `mongosh` / equivalent.

### Warn (the hook returns a `systemMessage`)

- `rm -rf <path>`.
- `docker prune` (any flavor).
- `terraform destroy`.
- `kubectl delete ...`.

### Allow

- All other commands. Allow without modification.

## Must not do

- Silently rewrite the command.
- Pretend to provide complete security; this is a guardrail, not a
  policy enforcer.
- Duplicate logic owned by `pre-write-secret-scan` or
  `session-end-orphan-check`.

## Output contract

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "..."
  }
}
```

or

```json
{ "systemMessage": "..." }
```

or `{}` when allowing.

## Idempotency

Stateless. Same command → same decision.
