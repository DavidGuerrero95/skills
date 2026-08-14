---
name: review-gate
description: Pre-merge quality gate over an existing diff — parallel independent reviews consolidated into one merge decision.
trigger: A non-trivial diff is ready for merge, especially when the implementer also wrote the tests.
---

# Pipeline — Review gate

## When to run

Before merging a non-trivial change (`commands/review-changes.md`). This
pipeline does not implement fixes — it produces a merge decision and a
list of required corrections.

## Preconditions

- The diff is complete and builds; tests have been run at least once.

## Stages

| # | agent                  | input | output                        | gate                                  | on-fail                                  |
| - | ---------------------- | ----- | ----------------------------- | ------------------------------------- | ---------------------------------------- |
| 1a *(parallel)* | `code-reviewer`      | diff  | correctness/layer/idempotency findings | —                              | —                                        |
| 1b *(parallel)* | `code-smell-auditor` | diff  | maintainability findings      | —                                     | —                                        |
| 1c *(parallel)* | `security-reviewer`  | diff  | secrets/shell/supply-chain findings | —                               | —                                        |
| 1d *(parallel)* | `dependency-auditor` *(only if deps changed)* | diff | dependency findings | —                          | —                                        |
| 1e *(parallel)* | `skills/domain-safety-review` *(only if a domain-critical path changed)* | diff | guardrail findings | —                | —                                        |
| 2 | *(main thread)*        | all findings | consolidated merge decision   | **no `blocker` open across any reviewer** | route each blocker to its owning implementation pipeline (`feature-delivery` / `bug-fix` / `refactor`) |

## Orchestration note

Stages 1a–1e run in parallel (independent, read-only). Stage 2 waits for
all of them, de-duplicates overlapping findings, and emits one decision.
The main thread verifies each finding against the diff before accepting
it.

## Output

```
Merge decision: APPROVE | CHANGES REQUIRED
Blockers:       <bullet> (owner pipeline: ...)
Warnings:       <bullet>
Reviewed by:    code-reviewer, code-smell-auditor, security-reviewer[, ...]
```
