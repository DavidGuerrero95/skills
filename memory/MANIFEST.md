# Memory manifest

This manifest exists to prevent drift and repeated instructions.

## Ownership matrix

| Concern | Canonical owner | Examples |
|---|---|---|
| Engineering invariants | `policies/01-engineering-baseline.md` | imports, build validation, framework boundaries |
| Architecture boundaries | `policies/02-clean-architecture.md` | domain purity, adapter boundaries |
| Reactive/Kafka correctness | `policies/03-reactive-and-messaging.md` | no blocking, backpressure, idempotency |
| Security & supply chain | `policies/05-security-and-secrets.md` | secrets, dependencies, dangerous commands |
| Domain guardrails | `policies/06-investment-domain-guardrails.md` | paper trading rules, risk boundaries |
| How work is executed | `rules/01-task-execution-flow.md` | inspect → plan → change → validate |
| Definition of done | `rules/02-validation-and-done-definition.md` | compile, test, smoke, docs |
| Visual architecture docs | `rules/05-diagrams-and-docs.md` | Mermaid, ADR, update triggers |
| Reusable implementation workflow | `skills/java-spring-implementation/SKILL.md` | task procedure |
| Specialized reviewer | `agents/code-smell-auditor.md` | agent persona |
| Auto-validation after edits | `hooks/post-edit-code-quality.md` | lifecycle automation |
| Explicit entrypoints | `commands/review-changes.md` | user-triggered workflow |
| Response brevity | `output-styles/terse-caveman.md` | style only |

## Anti-duplication rules

- Do not restate global engineering rules inside each skill.
- Do not place tone instructions inside skills unless the skill truly requires them.
- Do not put workflow logic in policies.
- Do not put domain policy in output styles.
- Do not put long procedures in `AGENTS.md` or `CLAUDE.md`; point to memory files instead.

## Update rules

When a repeated mistake appears:
1. fix the specific task,
2. identify the correct canonical owner,
3. update only that owner,
4. keep adapters thin.
