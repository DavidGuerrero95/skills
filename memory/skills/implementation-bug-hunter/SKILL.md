---
name: implementation-bug-hunter
description: Investigate failing behavior, trace root cause, propose the smallest safe fix, and add regression validation. Use for production-like defects, failing tests, wrong event mappings, broken contracts, scheduler / reconciliation issues and subtle reactive behavior.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: defect-root-cause
  version: "1.1"
---

# Implementation bug hunter

## When to use

- A production-like defect is reported and reproducible.
- A test is failing or flaky.
- An event arrived with the wrong shape, was rejected to DLQ, or
  produced an inconsistent projection.
- A scheduler / reconciliation tick produced unexpected effects.
- A reactive flow behaves non-deterministically.

## When NOT to use

- Cleanup tasks — `skills/code-smell-remediator`.
- Greenfield implementation — `skills/java-spring-implementation`.
- Smoke / E2E authoring — `skills/e2e-test-crafter`.

## Read first

- `memory/rules/01-task-execution-flow.md`
- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/03-reactive-and-messaging.md`
- `memory/rules/04-idempotency-and-event-contracts.md`

## Workflow

1. **Reproduce or restate.**
   - Write the failure as a one-paragraph reproduction.
   - Capture the exact input, the observed output, and the expected
     output.
   - If the bug is intermittent, capture the conditions under which it
     reproduces.

2. **Narrow the boundary.**
   - Bisect the path: which service? which module? which class?
   - Use logs, DLQ inspection, Grafana / Prometheus panels.
   - Identify the first place where the actual diverges from expected.

3. **Identify the smallest plausible root cause.**
   - State it in one sentence.
   - Distinguish symptoms from cause; the symptom may be in a
     downstream service while the cause is upstream.

4. **Write the failing regression test first.**
   - The test must reproduce the bug deterministically.
   - It must fail without the fix and pass with the fix.

5. **Apply the smallest safe fix.**
   - Stay inside the layer that owns the responsibility.
   - Do not bundle unrelated cleanup into the fix.

6. **Validate.**
   - Run the regression test (now green).
   - Run the rest of the impacted module's tests.
   - Run the relevant smoke / E2E if the bug crosses services.

7. **Summarize cause, fix, validation, and follow-ups.**

## Output expected from this skill

```
Reproduction:
 - <one-paragraph>

Root cause:
 - <one-sentence>; located at <file:line>

Fix:
 - <one-paragraph>

Regression test:
 - <ClassNameTest#scenario>

Validation:
 - [ran]  ./gradlew :<service>:test
 - [ran]  bash infrastructure/scripts/smoke-...sh   (when applicable)

Follow-ups:
 - <item> (if any)
```

## Common patterns to consider

- **Reactive subtleties:** missing `switchIfEmpty`, swallowed
  `Throwable`, `flatMap` reordering, signal lost after `onErrorResume`.
- **Idempotency mismatch:** the consumer treats `eventId` as the
  business key when it should use `clientOrderId` or
  `clientOrderId + cumulativeFilledQuantity`.
- **Schema drift:** producer and consumer disagree on a field name,
  type, or optionality.
- **Time-of-day:** scheduler running on the wrong zone or before infra
  is ready.
- **Race condition:** two replicas of a scheduler running without a
  Valkey distributed lock.
- **Stale cache:** Valkey TTL too short or too long for the cooldown.

## Forbidden patterns

- "Fixing" a flaky test by adding `@Disabled` or `Thread.sleep`.
- Patching a symptom in a downstream service when the cause is in the
  producer.
- Marking the bug fixed without a failing-then-green regression test.
- Bundling unrelated refactors with the fix.
