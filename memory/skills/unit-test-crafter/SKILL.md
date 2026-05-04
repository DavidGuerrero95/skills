---
name: unit-test-crafter
description: Create or improve focused unit tests for Java 21 code in this repository with readable fixtures, deterministic assertions, regression coverage for bug fixes, and JaCoCo-friendly structure. Use whenever new domain rules, use cases, mappers, validators or pure logic land, or when a defect needs a regression test.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: junit5-mockito-assertj
  version: "1.1"
---

# Unit test crafter

## When to use

- New or modified domain rules, value objects, aggregates.
- Use-case orchestration (mock the ports, not the adapters).
- Pure mappers, validators, calculators.
- A bug fix that needs a regression test.

## When NOT to use

- Adapter / persistence / messaging behavior — use Testcontainers via
  `skills/reactive-kafka-engineering` or a dedicated integration test.
- Cross-service workflows — `skills/e2e-test-crafter`.
- Pure refactors that already have green tests covering the change.

## Read first

- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/01-engineering-baseline.md`
- `memory/rules/02-validation-and-done-definition.md`

## Workflow

1. **Define the scenarios.** State each scenario in the form
   `given … when … then …`. One scenario per test method.
2. **Pick the smallest unit.** A unit test exercises one class
   (or a closely-coupled pair) and stubs everything else.
3. **Use focused assertions.**
   - Prefer AssertJ for fluent assertions.
   - Capture arguments and assert on the captured object instead of
     `Mockito.eq(...)`.
   - Assert on observable effect, not on whether a method was called.
4. **Use `[ClassName]TestData` builders** for any non-trivial fixture
   so the same setup is reused.
5. **Cover edge cases explicitly.**
   - Empty / null / boundary values.
   - Domain-specific invariants (negative quantities, stale market
     context, expired cooldowns).
6. **Add a regression test for every bug fix** before applying the
   fix. The test must fail without the fix.
7. **Run** the impacted module's tests:

   ```powershell
   .\gradlew.bat :<service>:<module>:test
   ```

8. **Update the JaCoCo merged report** if the module ships its own:

   ```powershell
   .\gradlew.bat :<service>:jacocoMergedReport :<service>:jacocoTestCoverageVerification --no-daemon
   ```

## Output expected from this skill

```
Tests added:
 - ClassNameTest#scenario_1
 - ClassNameTest#scenario_2

Defect covered (if any):
 - <one-line description>

Edge cases still not covered:
 - <only when intentional, with reason>

Validation:
 - [ran]  ./gradlew :<service>:test
 - [ran]  ./gradlew :<service>:jacocoTestCoverageVerification (where applicable)
```

## Conventions

- Test classes mirror the production class (`ClassNameTest`).
- Test methods read like sentences: `should_<verb>_<expected>_when_<condition>`.
- Avoid hidden setup via inheritance. Prefer `@BeforeEach` with a
  short, named factory call.
- Use Mockito strictness `STRICT_STUBS` (the project default).
- Reactor: use `StepVerifier` for `Mono` / `Flux` assertions; do not
  call `.block()` to inspect values in tests beyond a single
  `.block(Duration.ofSeconds(5))` for last-resort triage.

## Forbidden patterns

- Tests that depend on machine clock or wall-clock zones.
- Tests that hit the network.
- Tests that assert on log lines.
- Suppressing failures with `@Disabled` instead of fixing the test.
- Coverage padding (asserting `assertNotNull(obj)` after construction
  with no real check).
- Marking a bug fix as done without a failing-then-green regression
  test.
