---
name: code-smell-remediator
description: Identify and reduce code smells, duplication, dead code, weak naming, oversized methods, and poor boundary placement without destabilizing behavior.
---


# Code smell remediator

## Use for

- cleanup after feature work,
- refactor candidates,
- readability improvements,
- Sonar-driven remediation,
- boundary tightening.

## Rules

- Prefer behavior-preserving cleanup.
- Reduce duplication at the right abstraction level.
- Do not expand a refactor beyond the justified scope.
- Call out architecture violations explicitly.

## Read first

- `/memory/policies/01-engineering-baseline.md`
- `/memory/policies/02-clean-architecture.md`

## Output

Return:
- smells found,
- smells fixed,
- smells deferred,
- any risks from deferred cleanup.
