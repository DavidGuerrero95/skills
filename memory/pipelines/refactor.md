---
name: refactor
description: Bounded, behavior-preserving refactor of a single module — characterization tests first, planned steps, cleanup, review.
trigger: A module with duplication, mixed responsibilities, or long functions, too large for a smell pass but smaller than a redesign.
---

# Pipeline — Refactor

## When to run

A bounded refactor of one module (`commands/refactor-module.md`). Not a
cross-module redesign (open an ADR), a bug fix (`bug-fix.md`), or a
trivial cleanup (`code-smell-auditor` alone).

## Preconditions

- Scope is a single module. Entry/exit invariants are stated in writing.

## Stages

| # | agent                  | input                          | output                        | gate                                              | on-fail                                       |
| - | ---------------------- | ------------------------------ | ----------------------------- | ------------------------------------------------- | --------------------------------------------- |
| 1 | `software-architect`   | module + stated invariants     | target structure + step plan  | plan is behavior-preserving; no new boundary break | if a redesign is needed → stop, open an ADR    |
| 2 | `unit-test-engineer`   | module                         | characterization tests        | tests capture current behavior and are **green**   | add missing coverage at stage 2                |
| 3 | `code-smell-auditor`   | step plan + green tests        | refactored code (per step)    | tests stay green after **every** step             | revert the last step; re-plan                  |
| 4 | `code-reviewer`        | diff                           | findings                      | no `blocker`; no behavior change slipped in        | loop to stage 3                                 |
| 5 | `technical-writer` *(only if placement/behavior documented)* | diff | doc / ADR update              | docs match the new structure                       | loop to stage 5                                 |

## Output

```
Module:        <name>
Invariants:    <entry/exit>
Steps applied: rename → extract → move → inline (as needed)
Tests:         characterization green throughout
Review:        blockers resolved
```
