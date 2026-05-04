# /implement-feature

Use the implementation engineer and architecture guidance to deliver a
scoped feature safely.

## When to use

- A new behavior is requested with a defined surface (one or two
  services, one or two contracts).
- The change is bounded and the validation ladder is clear.

## When NOT to use

- A large refactor — open an ADR and use `/refactor-module`.
- A pure bug fix — use `/root-cause-analysis`.
- A docs-only update — use `/sync-documentation`.

## Steps

1. Inspect the relevant modules and immediate neighbors.
2. Read the applicable policies and rules:
   - `policies/01-engineering-baseline.md`
   - `policies/02-clean-architecture.md`
   - `policies/03-reactive-and-messaging.md` (when relevant)
   - `rules/01-task-execution-flow.md`
   - `rules/02-validation-and-done-definition.md`
3. Implement the smallest safe diff (delegate to
   `agents/java-implementation-engineer`).
4. Add or update targeted tests
   (delegate to `agents/unit-test-engineer` when appropriate).
5. Run a code-smell pass (delegate to
   `agents/code-smell-auditor`).
6. Update documentation when behavior or contracts changed
   (delegate to `agents/technical-writer`).
7. If the change is cross-service, run smoke / E2E
   (delegate to `agents/e2e-test-engineer`).

## Recommended delegates

- `java-implementation-engineer` (lead)
- `unit-test-engineer`
- `code-smell-auditor`
- `technical-writer` when behavior or contracts changed
- `mermaid-architect` when flows or ownership changed
- `code-reviewer` for an independent pass before merge
