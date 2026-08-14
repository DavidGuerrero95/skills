# Pipelines — declarative multi-agent workflows

A **pipeline** is a named, ordered chain of agents (from `memory/agents/`)
that the orchestrating (main) thread runs to deliver a class of work.
Where `commands/` say *"here are the recommended delegates"* and
`rules/03-subagent-delegation.md` says *"which agent for which job"*, a
pipeline goes further: it fixes the **order**, the **artifact** that flows
from one stage to the next, and the **gate** that must pass before the
next stage starts.

Pipelines are guidance for the orchestrator — they are executed by the
main thread delegating to each agent in turn (see
`rules/03-subagent-delegation.md`). They are **not** an autonomous runner;
the main thread stays responsible for verifying each stage's output before
advancing.

## Stage schema

Every pipeline lists its stages in a table with these columns:

| Column     | Meaning                                                             |
| ---------- | ------------------------------------------------------------------ |
| `#`        | Stage order.                                                       |
| `agent`    | The delegate from `memory/agents/` (or a skill for the main thread). |
| `input`    | The artifact/context handed to the stage.                          |
| `output`   | The artifact the stage must return.                                |
| `gate`     | The condition that must hold to advance. If it fails → `on-fail`.  |
| `on-fail`  | What the orchestrator does when the gate fails.                    |

## Orchestration rules (main thread)

1. **Run stages in order.** Do not start stage *n+1* until stage *n*'s
   gate passes.
2. **Pass the artifact forward.** Each stage's `output` is the next
   stage's `input`. Brief the delegate completely (it has no history).
3. **Verify before advancing.** The main thread confirms the delegate's
   report matches reality (the diff, the test run) — a green summary is
   not proof.
4. **Honor gates.** A failed gate routes to `on-fail` (usually: loop back
   to the owning stage, or stop and surface to the user). Never skip a
   gate to "keep moving".
5. **Parallelize only independent stages.** Stages marked *(parallel)*
   may run together; a gate that depends on all of them waits for all.
6. **Keep the minimum number of delegates.** Skip a stage whose work is
   genuinely not present in the change (say so in the summary).
7. **Stop conditions win.** The escalation triggers in
   `rules/01-task-execution-flow.md` and the guardrails in
   `policies/06-domain-guardrails.md` override the pipeline.

## Available pipelines

| Pipeline                       | Use when…                                             |
| ------------------------------ | ----------------------------------------------------- |
| `feature-delivery.md`          | Delivering a scoped feature end to end.               |
| `bug-fix.md`                   | Fixing a reproducible defect with regression cover.   |
| `refactor.md`                  | A bounded, behavior-preserving refactor.              |
| `database-change.md`           | A schema / migration / index change.                  |
| `contract-change.md`           | Changing an API or event contract.                    |
| `review-gate.md`               | A pre-merge quality gate over an existing diff.       |

## Adding a pipeline

1. Confirm no existing pipeline already covers the flow.
2. Create `pipelines/<name>.md` with frontmatter (`name`, `description`,
   `trigger`) and the stage table above.
3. Reuse existing agents; do not invent a persona inline.
4. Add a row here and in `memory/MANIFEST.md`.
5. Cross-link the matching `commands/*.md` (`Pipeline:` line).
