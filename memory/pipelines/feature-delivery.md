---
name: feature-delivery
description: End-to-end delivery of a scoped feature — architecture check, implementation, tests, review, and docs — with a gate between each stage.
trigger: A new bounded behavior with a defined surface (one or two modules / contracts).
---

# Pipeline — Feature delivery

## When to run

A scoped feature (`commands/implement-feature.md`). Not for large
refactors (`refactor.md`), pure bug fixes (`bug-fix.md`), or contract
changes (`contract-change.md`).

## Preconditions

- The task is stated in one sentence and the impacted layer(s) known.
- The active stack profile (`stacks/*`) and policies are read.

## Stages

| # | agent                     | input                              | output                          | gate                                              | on-fail                                        |
| - | ------------------------- | ---------------------------------- | ------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| 1 | `software-architect`      | task + impacted modules            | placement plan (layers, ports)  | placement respects `policies/02`; no new boundary violation | if a boundary must change → stop, open an ADR  |
| 2 | `implementation-engineer` | placement plan                     | minimal diff + wiring           | builds / type-checks; stays in the planned layers | loop to stage 2 with the failure                |
| 3 | `unit-test-engineer`      | diff                               | unit tests                      | **tests green**; observable-effect assertions     | loop to stage 2 (real bug) or stage 3 (test)   |
| 4 | `database-engineer` *(only if schema changed)* | diff + schema delta   | migration + indexes             | migration additive + verified on Testcontainers   | loop to stage 4                                 |
| 5 | `code-reviewer`           | diff + tests                       | findings (severity-tagged)      | **no `blocker` open**                             | loop to stage 2 with the blockers               |
| 6 | `e2e-test-engineer` *(only if cross-module)* | diff + workflow      | smoke/E2E run                   | smoke passes (`N/N`)                              | loop to the owning stage                         |
| 7 | `technical-writer`        | diff + contract deltas             | updated docs / `.env.example`   | docs match behavior; contracts updated            | loop to stage 7                                 |

## Output

```
Feature: <one line>
Stages run: 1..7 (skipped: <n> — reason)
Diff:       <files>
Tests:      <green summary>
Review:     <blockers resolved>
Docs:       <surfaces updated>
Validation: [ran] ...  [skip] ... (reason)
```
