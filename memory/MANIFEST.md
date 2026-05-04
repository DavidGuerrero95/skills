# /memory manifest

This manifest is the source of truth for **who owns what** inside `/memory`.
It exists to prevent duplicate rules, drift between files, and accidental
re-authoring of canonical content inside runtime adapters.

## Ownership matrix

| Concern                                            | Canonical owner                                       | Examples                                                                       |
| -------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------ |
| Memory governance / change control                 | `policies/00-governance.md`                           | When to add a file, anti-duplication rules                                     |
| Engineering invariants                             | `policies/01-engineering-baseline.md`                 | Java 21 features, Spring 4.x conventions, imports, build validation            |
| Hexagonal / clean architecture                     | `policies/02-clean-architecture.md`                   | Layer purity, package boundaries, transaction ownership                        |
| Reactive + Kafka correctness                       | `policies/03-reactive-and-messaging.md`               | No `block()`, backpressure, contract evolution, SCRAM/SASL                     |
| Testing + quality gates                            | `policies/04-testing-and-quality-gates.md`            | JUnit 5, Spotless, Sonar gates, JaCoCo 70 % line coverage                      |
| Security & secrets                                 | `policies/05-security-and-secrets.md`                 | `.env` discipline, destructive command guardrails, supply-chain checks         |
| Investment-domain guardrails                       | `policies/06-investment-domain-guardrails.md`         | Paper trading safety, risk parameter sources, notification ownership           |
| Documentation traceability                         | `policies/07-documentation-and-traceability.md`       | When to update README/ADRs/runbooks/diagrams                                   |
| Project working mode                               | `rules/00-project-baseline.md`                        | Inspect → change → validate → summarize                                        |
| Task execution flow                                | `rules/01-task-execution-flow.md`                     | Definition of ready, sequence of steps                                         |
| Validation + Definition of Done                    | `rules/02-validation-and-done-definition.md`          | Validation ladder, exact gradle commands                                       |
| Sub-agent delegation matrix                        | `rules/03-subagent-delegation.md`                     | Which agent for which job, depth limits                                        |
| Idempotency + event-contract review                | `rules/04-idempotency-and-event-contracts.md`         | Per-layer keys, replay behavior, DLQ semantics                                 |
| Diagrams + docs cadence                            | `rules/05-diagrams-and-docs.md`                       | Mermaid sources, where they live, update triggers                              |
| Reusable: implement Java/Spring change             | `skills/java-spring-implementation/SKILL.md`          | Workflow for production-ready Java diffs                                       |
| Reusable: reactive + Kafka work                    | `skills/reactive-kafka-engineering/SKILL.md`          | Reactor chains, consumers/producers, retries                                   |
| Reusable: unit tests                               | `skills/unit-test-crafter/SKILL.md`                   | JUnit 5 + Mockito patterns, fixtures, regression coverage                      |
| Reusable: smoke / E2E                              | `skills/e2e-test-crafter/SKILL.md`                    | Operator scripts, multi-service flows                                          |
| Reusable: bug investigation                        | `skills/implementation-bug-hunter/SKILL.md`           | Root-cause workflow, regression                                                |
| Reusable: code-smell remediation                   | `skills/code-smell-remediator/SKILL.md`               | Behavior-preserving cleanup                                                    |
| Reusable: investment-domain review                 | `skills/investment-domain-review/SKILL.md`            | Trading safety review                                                          |
| Reusable: Mermaid diagrams                         | `skills/mermaid-architecture-diagrams/SKILL.md`       | Mermaid output that matches reality                                            |
| Reusable: state-of-the-art research                | `skills/state-of-the-art-research/SKILL.md`           | Pattern selection grounded in repo                                             |
| Reusable: technical doc writing                    | `skills/technical-doc-writer/SKILL.md`                | README/ADR/runbook authoring                                                   |
| Reusable: dependency management                    | `skills/dependency-management/SKILL.md`               | Add/upgrade Gradle deps, supply-chain checks                                   |
| Specialized agent: Java implementation             | `agents/java-implementation-engineer.md`              | Implementation persona                                                         |
| Specialized agent: Java architecture               | `agents/java-architect.md`                            | Architecture persona                                                           |
| Specialized agent: unit tests                      | `agents/unit-test-engineer.md`                        | Focused unit test persona                                                      |
| Specialized agent: E2E tests                       | `agents/e2e-test-engineer.md`                         | Smoke / E2E persona                                                            |
| Specialized agent: code-smell auditor              | `agents/code-smell-auditor.md`                        | Cleanup persona                                                                |
| Specialized agent: failure investigator            | `agents/failure-investigator.md`                      | Debug persona                                                                  |
| Specialized agent: Mermaid architect               | `agents/mermaid-architect.md`                         | Diagram persona                                                                |
| Specialized agent: technical writer                | `agents/technical-writer.md`                          | Docs persona                                                                   |
| Specialized agent: security reviewer               | `agents/security-reviewer.md`                         | Shell, secrets, supply chain                                                   |
| Specialized agent: code reviewer                   | `agents/code-reviewer.md`                             | Diff-only review for correctness and style                                     |
| Specialized agent: dependency auditor              | `agents/dependency-auditor.md`                        | Gradle deps + version policy                                                   |
| Hook: post-edit code quality reminder              | `hooks/post-edit-code-quality.md`                     | After Edit/Write — suggest validation/smell pass                               |
| Hook: post-task docs sync                          | `hooks/post-task-docs-sync.md`                        | On Stop — flag doc drift                                                       |
| Hook: pre-bash safety guard                        | `hooks/pre-bash-safety-guard.md`                      | Block destructive commands before execution                                    |
| Hook: pre-write secret scan                        | `hooks/pre-write-secret-scan.md`                      | Block obvious secrets in Edit/Write payloads                                   |
| Hook: prompt memory reminder                       | `hooks/prompt-memory-reminder.md`                     | Session start — point to `/memory`                                             |
| Hook: session-end orphan check                     | `hooks/session-end-orphan-check.md`                   | Stop / SessionEnd — flag lingering processes                                   |
| Hook: subagent-stop summary                        | `hooks/subagent-stop-summary.md`                      | SubagentStop — reminder to surface delegate output                             |
| Command: implement feature                        | `commands/implement-feature.md`                       | `/implement-feature` workflow                                                   |
| Command: review changes                            | `commands/review-changes.md`                          | `/review-changes` axes                                                          |
| Command: audit code smells                         | `commands/audit-code-smells.md`                       | `/audit-code-smells` workflow                                                   |
| Command: write E2E tests                           | `commands/write-e2e-tests.md`                         | `/write-e2e-tests` workflow                                                     |
| Command: fix failing tests                         | `commands/fix-failing-tests.md`                       | `/fix-failing-tests` workflow                                                   |
| Command: root-cause analysis                       | `commands/root-cause-analysis.md`                     | `/root-cause-analysis` workflow                                                 |
| Command: generate diagrams                         | `commands/generate-diagrams.md`                       | `/generate-diagrams` workflow                                                   |
| Command: sync documentation                        | `commands/sync-documentation.md`                      | `/sync-documentation` workflow                                                 |
| Command: refactor module                           | `commands/refactor-module.md`                         | `/refactor-module` workflow                                                    |
| Output style: terse caveman                        | `output-styles/terse-caveman.md`                      | Minimal user-facing words                                                      |
| Output style: teaching senior                      | `output-styles/teaching-senior.md`                    | Didactic explanation                                                           |
| Output style: architect audit                      | `output-styles/architect-audit.md`                    | Structured tradeoff-aware                                                      |
| Output style: incident responder                   | `output-styles/incident-responder.md`                 | Triage-first crisp reporting                                                   |

## Anti-duplication rules

1. **One owner per concern.** Before adding a new file, find the existing
   owner in this matrix and update it instead.
2. **Policies do not contain workflow.** Long procedures live in `skills/`.
3. **Skills do not redeclare policy.** They link to it via `Read first`.
4. **Agents do not contain workflow.** They link to one or more skills.
5. **Output styles affect tone only.** They never set validation rules.
6. **Adapter folders never own content.** `.claude/`, `.codex/`, `.cursor/`,
   `.agents/` reference canonical files; they do not redefine them.
7. **`AGENTS.md` and `CLAUDE.md` stay short.** They are operating guides,
   not policy stores. Point readers to `/memory`.

## Maintenance loop

When a recurring mistake or gap appears:

1. Fix the immediate task.
2. Identify the canonical owner from this matrix.
3. Update only that owner — keep the diff small.
4. If the responsibility is genuinely new, add a file *and* a row here.
5. Re-check adapters: are they still thin pointers?
