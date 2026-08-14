---
name: unit-test-crafter
description: Create or improve focused unit tests in any stack with readable fixtures, deterministic assertions, and regression coverage for bug fixes. Use whenever new domain rules, use cases, mappers, validators, or pure logic land, or when a defect needs a regression test.
license: MIT
metadata:
  scope: unit-testing
  version: "2.0"
---

# Unit test crafter

## When to use

- New or modified domain rules, value objects, aggregates.
- Use-case orchestration (mock the ports, not the adapters).
- Pure mappers, validators, calculators.
- A bug fix that needs a regression test.

## When NOT to use

- Adapter / persistence / messaging behavior — use Testcontainers
  integration tests (`skills/async-messaging-engineering` or a
  dedicated integration test).
- Cross-module workflows — `skills/e2e-test-crafter`.
- Pure refactors already covered by green tests.

## Read first

- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/01-engineering-baseline.md`
- The active `memory/stacks/<stack>.md` for the test toolchain
  (JUnit5+Mockito+AssertJ, pytest+pytest-asyncio, Vitest/Jest, …).
- `memory/rules/02-validation-and-done-definition.md`

## Workflow

1. **Define the scenarios.** State each as `given … when … then …`.
   One scenario per test.
2. **Pick the smallest unit.** Exercise one unit (or a tightly-coupled
   pair) and stub everything else.
3. **Use focused assertions.**
   - Assert on the observable effect, not on whether a method was called.
   - Capture arguments and assert on the captured value instead of loose
     matchers.
4. **Use named test-data builders/factories** for non-trivial fixtures.
5. **Cover edge cases explicitly:** empty / null / boundary values and
   domain invariants.
6. **Add a regression test for every bug fix** first; it must fail
   without the fix.
7. **Run** the impacted module's tests and coverage using the stack's
   commands.

## Output expected from this skill

```
Tests added:
 - <TestName>#scenario_1
 - <TestName>#scenario_2

Defect covered (if any):
 - <one-line description>

Edge cases still not covered:
 - <only when intentional, with reason>

Validation:
 - [ran]  <test command>
 - [ran]  <coverage command> (where applicable)
```

## Conventions

- Test names read like sentences:
  `should_<verb>_<expected>_when_<condition>`.
- Avoid hidden setup via deep inheritance; prefer a short named factory
  in setup.
- For async code, use the runtime's test utilities (`StepVerifier`,
  `pytest-asyncio`, awaited assertions); do not block to inspect values
  except as a last-resort bounded triage.

## Forbidden patterns

- Tests that depend on machine clock or wall-clock zones.
- Tests that hit the network.
- Tests that assert on log lines.
- Disabling a failing test instead of fixing it.
- Coverage padding (asserting only that construction returned non-null).
- Marking a bug fix done without a failing-then-green regression test.
