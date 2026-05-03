# Governance policy

## Purpose

Define the non-negotiable governance for this memory system.

## Rules

- `/memory` is the canonical source of truth for agent behavior in this repository.
- Tool-specific folders may adapt memory for discovery, but they must not become independent policy stores.
- New instruction files must declare a single clear responsibility.
- When two files appear to overlap, shrink or merge the weaker one instead of tolerating duplication.
- Prefer additive local specialization over broad global verbosity.
- Keep root instruction files concise and operational.
- Every reusable behavior should answer:
  - when it applies,
  - when it does not apply,
  - what inputs it expects,
  - what validation it requires.

## Change control

A new file is justified only if:
- it serves a distinct trigger or responsibility,
- it reduces ambiguity,
- and it does not mostly restate another file.
