---
name: bug-fix
description: Fix a reproducible defect — reproduce, root-cause, failing regression test, smallest safe fix, review — with a gate between each stage.
trigger: A reproducible defect or a failing/flaky test.
---

# Pipeline — Bug fix

## When to run

A reproducible defect (`commands/root-cause-analysis.md`,
`commands/fix-failing-tests.md`). Not for cleanup (`refactor.md`) or new
behavior (`feature-delivery.md`).

## Preconditions

- A concrete reproduction (input, observed, expected) exists or can be
  produced.

## Stages

| # | agent                     | input                          | output                              | gate                                              | on-fail                                       |
| - | ------------------------- | ------------------------------ | ----------------------------------- | ------------------------------------------------- | --------------------------------------------- |
| 1 | `failure-investigator`    | reproduction                   | root cause (one sentence + file:line) | cause is the true origin, not a symptom          | keep bisecting at stage 1                      |
| 2 | `failure-investigator` or `unit-test-engineer` | root cause | **failing** regression test         | test fails *without* the fix (proves the bug)     | rewrite the test at stage 2                     |
| 3 | `failure-investigator`    | failing test + root cause      | smallest safe fix in the owning layer | regression test now green; module tests green     | loop to stage 3; if fix needs a boundary change → stop, escalate |
| 4 | `e2e-test-engineer` *(only if the bug crosses modules)* | fix | smoke/E2E run                       | smoke passes                                      | loop to stage 3                                 |
| 5 | `code-reviewer`           | diff + regression test         | findings                            | no `blocker`; fix has no unrelated changes        | loop to stage 3                                 |
| 6 | `technical-writer` *(only if behavior/contract changed)* | diff | doc update                          | docs match new behavior                           | loop to stage 6                                 |

## Output

```
Reproduction: <one paragraph>
Root cause:   <one sentence>; <file:line>
Regression:   <TestName>#scenario (failing→green)
Fix:          <files>
Validation:   [ran] regression + module tests [ran|skip] smoke
```
