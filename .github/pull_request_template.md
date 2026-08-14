## Summary

<!-- One or two sentences: what changed and why. -->

## Change type

- [ ] Feature
- [ ] Bug fix (includes a failing-then-green regression test)
- [ ] Refactor (behavior-preserving)
- [ ] Docs / infra / CI

## Checklist (see /memory)

- [ ] Code is in the correct layer (`policies/02-clean-architecture.md`)
- [ ] Follows the active stack profile (`stacks/*`)
- [ ] Async correctness — no blocking on the runtime, empty case handled
- [ ] Idempotency keys respected (`rules/04-idempotency-and-event-contracts.md`)
- [ ] Tests added/updated; deterministic; observable-effect assertions
- [ ] No secrets; new env vars documented in `.env.example`
- [ ] Docs updated when behavior/contracts changed
- [ ] Domain guardrails reviewed if a critical path was touched
      (`policies/06-domain-guardrails.md`)

## Validation

```
- [ran]  <build/type-check>
- [ran]  <tests>
- [skip] <what> (reason)
```

## Open follow-ups

<!-- Anything intentionally deferred. -->
