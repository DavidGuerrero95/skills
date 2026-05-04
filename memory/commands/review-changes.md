# /review-changes

Review the current diff for correctness, architecture, quality, and
missing validation. The output is a structured review, not a fix.

## Review axes

Walk the axes in order. For each, note `file:line` and severity.

1. **Architecture / boundary placement** — `policies/02-clean-architecture.md`.
2. **Reactive correctness** — `policies/03-reactive-and-messaging.md`.
3. **Idempotency keys** — `rules/04-idempotency-and-event-contracts.md`.
4. **Code smells** — `policies/01-engineering-baseline.md`,
   `skills/code-smell-remediator`.
5. **Security & secrets** — `policies/05-security-and-secrets.md`.
6. **Tests** — coverage of the touched paths, regression for fixes,
   determinism, focused assertions.
7. **Docs** — README, ADRs, runbooks, contract docs, env vars.
8. **Investment-domain safety** (when applicable) —
   `policies/06-investment-domain-guardrails.md`,
   `skills/investment-domain-review`.

## Recommended delegates

- `code-reviewer` (lead, independent diff review)
- `java-architect` (when boundary concerns appear)
- `code-smell-auditor` (when readability concerns appear)
- `security-reviewer` (when shell, secrets, or deps concerns appear)
- `technical-writer` (when doc concerns appear)
