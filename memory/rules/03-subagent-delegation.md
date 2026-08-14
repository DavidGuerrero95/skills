# 03 — Sub-agent delegation

## When to delegate

Delegate to a specialized agent in `memory/agents/*` when at least one of
the following holds:

- The task **benefits from a distinct role** (architecture, testing,
  documentation, security, debugging, data) that has different defaults
  than the main thread.
- The role can work with **narrower context**, freeing the main thread's
  window for orchestration.
- **Parallel inspection** would reduce cognitive load (e.g. one agent
  reviews tests while another reviews architecture).
- The output benefits from **independent review** (an implementation
  pass and a separate code-review pass).

Stay direct (no delegation) when the task is contained, mechanical, or
you already have all the context the agent would need.

## Delegation matrix

| Task shape                                              | Recommended delegate(s)                                  |
| ------------------------------------------------------- | -------------------------------------------------------- |
| Implement a code change (any stack)                     | `implementation-engineer`                                |
| Architecture / placement / boundary review              | `software-architect`                                     |
| Generic diff review for correctness and style           | `code-reviewer`                                          |
| Unit tests / regression coverage                        | `unit-test-engineer`                                     |
| Smoke / E2E across modules                              | `e2e-test-engineer`                                      |
| Code-smell remediation                                  | `code-smell-auditor`                                     |
| Defect / failing test investigation                     | `failure-investigator`                                   |
| Schema / migration / query design & review              | `database-engineer`                                      |
| Architecture / sequence / ownership diagrams            | `mermaid-architect`                                      |
| README / ADR / runbook authoring                        | `technical-writer`                                       |
| Shell safety / secrets / supply chain                   | `security-reviewer`                                      |
| Dependency add/upgrade / version policy                 | `dependency-auditor`                                     |
| Domain-safety review                                    | (skill `domain-safety-review`, no separate agent)        |
| State-of-the-art research (pattern selection)           | (skill `state-of-the-art-research`)                      |

## Pipelines (ordered multi-agent chains)

For recurring work that spans several agents in a fixed order, use a
**pipeline** in `memory/pipelines/` instead of ad-hoc delegation. A
pipeline fixes the stage order, the artifact passed between stages, and
the **gate** that must pass before the next stage starts.

| Work shape                    | Pipeline                                |
| ----------------------------- | --------------------------------------- |
| Deliver a scoped feature      | `pipelines/feature-delivery.md`         |
| Fix a reproducible defect     | `pipelines/bug-fix.md`                  |
| Bounded refactor of a module  | `pipelines/refactor.md`                 |
| Schema / migration / index    | `pipelines/database-change.md`          |
| API / event contract change   | `pipelines/contract-change.md`          |
| Pre-merge quality gate        | `pipelines/review-gate.md`              |

The main thread executes a pipeline by delegating to each stage's agent
in order and honoring its gate; see `pipelines/README.md` for the stage
schema and orchestration rules. Pipelines do not replace the single-agent
delegation above — they compose it.

## Boundaries on delegation

- **Use the minimum number of active delegates** needed. One implementer
  + one reviewer is usually enough.
- **Avoid deep recursive delegation.** A delegate should not, by default,
  spawn another delegate. If it must, it surfaces that first.
- **Do not delegate understanding.** The main thread keeps responsibility
  for the synthesis. Delegate inputs (search, draft, review), not
  decisions.
- **Brief the delegate completely.** A sub-agent has zero conversation
  history. Pass: goal, context, constraints, expected output shape,
  scope.
- **Foreground vs background.** Foreground when the result blocks the
  next step. Background only when the work is genuinely independent.

## Output expectations

A delegate returns a structured report:

```
Findings:    short bullets
Decisions:   what was changed (if anything) and why
Risks:       what could go wrong, what is not covered
Open items:  follow-ups that the main thread should track
Validation:  exactly which checks were run
```

The main thread is responsible for **verifying** that the delegate's
summary matches the actual diff before reporting work as done.

## Forbidden patterns

- Spawning a delegate "to look smart" when the task is trivial.
- Spawning two delegates with overlapping scope and accepting the louder
  summary.
- Delegating, then ignoring the delegate's risks section.
- Re-using a generic agent when a specialized one is listed in the
  matrix.
