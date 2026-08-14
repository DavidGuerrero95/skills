# /memory manifest

This manifest is the source of truth for **who owns what** inside
`/memory`. It exists to prevent duplicate rules, drift between files, and
accidental re-authoring of canonical content inside runtime adapters.

## Ownership matrix

| Concern                                            | Canonical owner                                       |
| -------------------------------------------------- | ----------------------------------------------------- |
| Memory governance / change control                 | `policies/00-governance.md`                           |
| Engineering invariants (stack-agnostic)            | `policies/01-engineering-baseline.md`                 |
| Hexagonal / clean architecture                     | `policies/02-clean-architecture.md`                   |
| Async + messaging correctness                      | `policies/03-async-and-messaging.md`                  |
| Testing + quality gates                            | `policies/04-testing-and-quality-gates.md`            |
| Security & secrets                                 | `policies/05-security-and-secrets.md`                 |
| Domain guardrails (project template)               | `policies/06-domain-guardrails.md`                    |
| Documentation traceability                         | `policies/07-documentation-and-traceability.md`       |
| Project working mode                               | `rules/00-project-baseline.md`                        |
| Task execution flow                                | `rules/01-task-execution-flow.md`                     |
| Validation + Definition of Done                    | `rules/02-validation-and-done-definition.md`          |
| Sub-agent delegation matrix                        | `rules/03-subagent-delegation.md`                     |
| Idempotency + event-contract review                | `rules/04-idempotency-and-event-contracts.md`         |
| Diagrams + docs cadence                            | `rules/05-diagrams-and-docs.md`                       |
| Stack profiles index                               | `stacks/README.md`                                    |
| Stack: Java + Spring Boot                          | `stacks/java-spring.md`                               |
| Stack: Python + FastAPI                            | `stacks/python-fastapi.md`                            |
| Stack: Node + TypeScript                           | `stacks/node-typescript.md`                           |
| Stack: PostgreSQL                                  | `stacks/postgresql.md`                                |
| Stack: MongoDB                                     | `stacks/mongodb.md`                                   |
| Stack: Redis / Valkey                              | `stacks/redis.md`                                     |
| Stack: Kafka / event streaming                     | `stacks/messaging-kafka.md`                           |
| Stack: REST / HTTP API design                      | `stacks/rest-api-design.md`                           |
| Stack: Docker / local infra                        | `stacks/docker-compose.md`                            |
| Reusable: implement / refactor a feature           | `skills/feature-implementation/SKILL.md`              |
| Reusable: async + messaging work                   | `skills/async-messaging-engineering/SKILL.md`         |
| Reusable: unit tests                               | `skills/unit-test-crafter/SKILL.md`                   |
| Reusable: smoke / E2E                              | `skills/e2e-test-crafter/SKILL.md`                    |
| Reusable: bug investigation                        | `skills/implementation-bug-hunter/SKILL.md`           |
| Reusable: code-smell remediation                   | `skills/code-smell-remediator/SKILL.md`               |
| Reusable: domain-safety review                     | `skills/domain-safety-review/SKILL.md`                |
| Reusable: database design / migrations             | `skills/database-design/SKILL.md`                     |
| Reusable: Mermaid diagrams                         | `skills/mermaid-architecture-diagrams/SKILL.md`       |
| Reusable: state-of-the-art research                | `skills/state-of-the-art-research/SKILL.md`           |
| Reusable: technical doc writing                    | `skills/technical-doc-writer/SKILL.md`                |
| Reusable: dependency management                    | `skills/dependency-management/SKILL.md`               |
| Specialized agent: implementation                  | `agents/implementation-engineer.md`                   |
| Specialized agent: architecture                    | `agents/software-architect.md`                        |
| Specialized agent: unit tests                      | `agents/unit-test-engineer.md`                        |
| Specialized agent: E2E tests                       | `agents/e2e-test-engineer.md`                         |
| Specialized agent: code-smell auditor              | `agents/code-smell-auditor.md`                        |
| Specialized agent: failure investigator            | `agents/failure-investigator.md`                      |
| Specialized agent: database engineer               | `agents/database-engineer.md`                         |
| Specialized agent: Mermaid architect               | `agents/mermaid-architect.md`                         |
| Specialized agent: technical writer                | `agents/technical-writer.md`                          |
| Specialized agent: security reviewer               | `agents/security-reviewer.md`                         |
| Specialized agent: code reviewer                   | `agents/code-reviewer.md`                             |
| Specialized agent: dependency auditor              | `agents/dependency-auditor.md`                        |
| Hook: post-edit code quality reminder              | `hooks/post-edit-code-quality.md`                     |
| Hook: post-task docs sync                          | `hooks/post-task-docs-sync.md`                        |
| Hook: pre-bash safety guard                        | `hooks/pre-bash-safety-guard.md`                      |
| Hook: pre-write secret scan                        | `hooks/pre-write-secret-scan.md`                      |
| Hook: prompt memory reminder                       | `hooks/prompt-memory-reminder.md`                     |
| Hook: session-end orphan check                     | `hooks/session-end-orphan-check.md`                   |
| Hook: subagent-stop summary                        | `hooks/subagent-stop-summary.md`                      |
| Command: implement feature                         | `commands/implement-feature.md`                       |
| Command: review changes                            | `commands/review-changes.md`                          |
| Command: audit code smells                         | `commands/audit-code-smells.md`                       |
| Command: write E2E tests                           | `commands/write-e2e-tests.md`                         |
| Command: fix failing tests                         | `commands/fix-failing-tests.md`                       |
| Command: root-cause analysis                       | `commands/root-cause-analysis.md`                     |
| Command: generate diagrams                         | `commands/generate-diagrams.md`                       |
| Command: sync documentation                        | `commands/sync-documentation.md`                      |
| Command: refactor module                           | `commands/refactor-module.md`                         |
| Command: design database                           | `commands/design-database.md`                         |
| Output style: terse caveman                        | `output-styles/terse-caveman.md`                      |
| Output style: teaching senior                      | `output-styles/teaching-senior.md`                    |
| Output style: architect audit                      | `output-styles/architect-audit.md`                    |
| Output style: incident responder                   | `output-styles/incident-responder.md`                 |

## Anti-duplication rules

1. **One owner per concern.** Before adding a new file, find the existing
   owner in this matrix and update it instead.
2. **Policies do not contain workflow.** Long procedures live in
   `skills/`.
3. **Policies do not contain stack syntax.** Language/datastore specifics
   live in `stacks/`.
4. **Skills do not redeclare policy or stack rules.** They link via
   `Read first`.
5. **Agents do not contain workflow.** They link to one or more skills.
6. **Output styles affect tone only.** They never set validation rules.
7. **Adapter folders never own content.** `.claude/`, `.codex/`,
   `.cursor/`, `.agents/`, and the Copilot instructions under `.github/`
   reference canonical files; they do not redefine them.
8. **`AGENTS.md` and `CLAUDE.md` stay short.** They are operating guides,
   not policy stores.

## Maintenance loop

When a recurring mistake or gap appears:

1. Fix the immediate task.
2. Identify the canonical owner from this matrix.
3. Update only that owner — keep the diff small.
4. If the responsibility is genuinely new, add a file *and* a row here.
5. Re-check adapters: are they still thin pointers?
