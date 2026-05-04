# Hook — session-end orphan check

## Purpose

Best-effort detection of lingering local agent / tool processes so the
operator can clean up explicit long-running work and avoid accidental
token / credit consumption from forgotten background tasks.
Implementation: `scripts/agentic/session_end_orphan_check.py`.

## Trigger

- Claude Code `Stop` and `SessionEnd`.
- Codex `Stop`.

## Responsibilities

- Enumerate local processes whose command line contains
  `claude` or `codex` (case-insensitive), excluding the current
  process.
- Emit a `systemMessage` summarizing the count and a few sample
  command lines (truncated).
- Emit nothing when zero matches are found.

## Must not do

- Kill processes automatically. Visibility only.
- Inspect remote machines.
- Pretend to provide a guaranteed token-leak prevention; this is a
  hygiene check.

## Output contract

`{"systemMessage": "..."}` or `{}`.

## Idempotency

Stateless. The output is a function of the current process list.
