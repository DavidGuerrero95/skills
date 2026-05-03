# Pre Bash safety guard

## Purpose

Block or challenge obviously destructive shell commands before execution.

## Trigger

- Before Bash / shell tool usage.

## Responsibilities

- detect destructive command patterns,
- deny clearly unsafe commands,
- warn on risky commands,
- allow routine read-only commands.

## Must not do

- silently rewrite commands in surprising ways,
- pretend to provide complete security,
- duplicate dependency or docs logic.
