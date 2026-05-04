# Hook — subagent-stop summary

## Purpose

When a sub-agent finishes (`SubagentStop`), remind the main thread to
verify and surface the delegate's output before continuing. The hook
also runs the orphan-process check so a sub-agent that spawned a
background helper does not leak. Implementation:
`scripts/agentic/session_end_orphan_check.py` (re-used).

## Trigger

- Claude Code `SubagentStop`.

## Responsibilities

- Re-run the orphan-process scan
  (`session_end_orphan_check.py`).
- Emit a `systemMessage` reminding the main agent to:
  - read the delegate's structured deliverable,
  - verify the diff matches the delegate's summary,
  - decide whether another delegate is required.

## Must not do

- Block the SubagentStop event.
- Auto-spawn another sub-agent.
- Edit files.

## Output contract

`{"systemMessage": "..."}` or `{}`.

## Idempotency

Stateless. The output depends only on the current process list and the
fixed reminder text.
