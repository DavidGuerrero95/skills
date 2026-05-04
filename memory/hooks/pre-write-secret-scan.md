# Hook — pre-write secret scan

## Purpose

Block obviously secret-shaped strings from being written to disk via
`Edit` / `Write` tool calls. Implementation:
`scripts/agentic/pre_write_secret_scan.py`.

## Trigger

- Claude Code `PreToolUse` matching `Edit|Write`.
- Codex `PreToolUse` matching `Edit|Write|^apply_patch$`.

## Responsibilities

### Deny

- AWS-shaped keys (`AKIA[0-9A-Z]{16}`).
- OpenAI-shaped keys (`sk-[A-Za-z0-9]{20,}`).
- Slack tokens (`xox[baprs]-...`).
- GitHub PATs (`ghp_...`, `github_pat_...`).
- JDBC URLs with embedded credentials.
- PEM private keys (`-----BEGIN ... PRIVATE KEY-----`).
- Telegram bot tokens (`[0-9]{8,12}:AA[A-Za-z0-9_\-]{30,}`).

### Warn

- Strings that look like secrets but are inside `.env.example` /
  `*.test.*` paths and are clearly placeholder shapes (`xxxx-xxxx`,
  `REDACTED`, `your-api-key-here`).

### Allow

- Everything else.

## Must not do

- Block legitimate `.env.example` updates that use clear placeholders.
- Replace the secret silently in the diff.
- Duplicate the destructive-command logic owned by
  `pre-bash-safety-guard`.

## Output contract

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Likely secret detected in payload..."
  }
}
```

or `{ "systemMessage": "..." }` for warnings, or `{}` for allow.

## Idempotency

Stateless. The same payload produces the same decision.
