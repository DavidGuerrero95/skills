---
name: implementation-bug-hunter
description: Investigate failing behavior, trace root cause, propose the smallest safe fix, and add regression validation. Use for production-like defects, failing tests, wrong mappings, broken contracts, scheduler/reconciliation issues, and subtle async behavior.
license: MIT
metadata:
  scope: defect-root-cause
  version: "2.0"
---

# Implementation bug hunter

## When to use

- A production-like defect is reported and reproducible.
- A test is failing or flaky.
- A message arrived with the wrong shape, was dead-lettered, or produced
  an inconsistent projection.
- A scheduler / reconciliation tick produced unexpected effects.
- An async flow behaves non-deterministically.

## When NOT to use

- Cleanup tasks — `skills/code-smell-remediator`.
- Greenfield implementation — `skills/feature-implementation`.
- Smoke / E2E authoring — `skills/e2e-test-crafter`.

## Read first

- `memory/rules/01-task-execution-flow.md`
- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/03-async-and-messaging.md`
- `memory/rules/04-idempotency-and-event-contracts.md`

## Workflow

1. **Reproduce or restate.** Write the failure as a one-paragraph
   reproduction: exact input, observed output, expected output, and (if
   intermittent) the conditions that trigger it.

2. **Narrow the boundary.** Bisect the path (module → unit). Use logs,
   dead-letter inspection, dashboards. Find the first place actual
   diverges from expected.

3. **Identify the smallest plausible root cause.** State it in one
   sentence. Distinguish symptom from cause — the symptom may be
   downstream while the cause is upstream.

4. **Write the failing regression test first.** It must reproduce the
   bug deterministically and fail without the fix.

5. **Apply the smallest safe fix**, inside the layer that owns the
   responsibility. Do not bundle unrelated cleanup.

6. **Validate.** Regression test green, rest of the module's tests
   green, smoke / E2E when the bug crosses modules.

7. **Summarize** cause, fix, validation, follow-ups.

## Output expected from this skill

```
Reproduction:
 - <one-paragraph>

Root cause:
 - <one-sentence>; located at <file:line>

Fix:
 - <one-paragraph>

Regression test:
 - <TestName>#scenario

Validation:
 - [ran]  <test command>
 - [ran]  <smoke/E2E>   (when applicable)

Follow-ups:
 - <item> (if any)
```

## Common patterns to consider

- **Async subtleties:** missing empty-handling, swallowed error,
  reordering under concurrency, signal lost after error-recovery.
- **Idempotency mismatch:** using the envelope id where the business key
  (command id, projection counter) was required.
- **Schema drift:** producer and consumer disagree on a field name,
  type, or optionality.
- **Time-of-day:** scheduler on the wrong zone or before infra is ready.
- **Race condition:** two replicas without a distributed lock.
- **Stale cache:** TTL too short or too long for the window.

## Forbidden patterns

- "Fixing" a flaky test by disabling it or adding a sleep.
- Patching a symptom downstream when the cause is upstream.
- Marking the bug fixed without a failing-then-green regression test.
- Bundling unrelated refactors with the fix.
