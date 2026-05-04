# Hook — prompt / session-start memory reminder

## Purpose

At session start (and optionally on prompt submit), remind the agent
that `/memory` is the canonical source and that runtime adapters
(`.claude/`, `.codex/`, `.cursor/`, `.agents/`) are thin pointers, not
content stores. Implementation:
`scripts/agentic/prompt_memory_reminder.py`.

## Trigger

- Claude Code `SessionStart`.
- Codex `SessionStart`.
- Optional: `UserPromptSubmit` for high-risk repos.

## Responsibilities

- Emit a single short `systemMessage` pointing the agent at
  `/memory/README.md` and `/memory/MANIFEST.md`.
- Encourage the agent to update canonical files instead of adapter
  copies.

## Must not do

- Inspect the user prompt in detail.
- Insert long instructions; the canonical content already lives in
  `/memory`.

## Output contract

`{"systemMessage": "..."}`.

## Idempotency

Stateless. Always emits the same reminder per session.
