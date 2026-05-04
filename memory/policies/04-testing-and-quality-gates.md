# 04 — Testing and quality gates

## Purpose

Define the minimum validation expected for any change, and the merge
gates that block work from landing. The exact validation **ladder** for
a given change lives in `rules/02-validation-and-done-definition.md`.

## Minimum validation per change

- **Compile** the changed module or feature path.
- **Run targeted unit tests** for touched behavior.
- **Run integration tests** when adapters, persistence, messaging, or
  contracts change.
- **Run smoke / E2E scripts** when the task crosses service boundaries
  or affects an operator-visible workflow.
- **Re-run Spotless and JaCoCo** when the touched module ships its own
  coverage report.

## Quality expectations

- **Tests are first-class code.** They are reviewed and refactored with
  the production code they cover.
- Tests must be **deterministic**. No `Thread.sleep`, no time-of-day
  assertions, no flaky network calls.
- Prefer **focused assertions** over permissive matchers. Assert on the
  observable effect, not on whether a method was called.
- Avoid `Mockito.eq(...)` unless there is no safe alternative.
  Prefer captured arguments and equality on the captured object.
- Add a **regression test for every bug fix.** A fix without a failing
  test reproducing the bug is incomplete.
- Update fixtures via `[ClassName]TestData` builders rather than
  inlining setup blocks across files.
- Use Testcontainers for adapter integration tests (Kafka, PostgreSQL,
  MongoDB, Valkey). Do not mock the protocol surface of these systems.

## Merge gates (blocking)

- **Spotless** clean: no formatting violations.
- **Sonar Bugs and Vulnerabilities** at zero on the change set. Code
  smells are reviewed; bugs and vulnerabilities are merge blockers.
- **JaCoCo merged report** ≥ **70 % line coverage** per service. The
  exclusions are `**/*Application.class`, `**/config/**`, `**/dto/**`,
  `**/*Properties.class`, `**/*MapperImpl.class`.
- **Pipeline workflow** `.github/workflows/ci.yml` green for the branch
  before requesting review.

## Useful commands

```powershell
# Per service — Windows PowerShell, from repo root
.\gradlew.bat clean test jacocoMergedReport jacocoTestCoverageVerification --no-daemon

# Targeted Kafka integration tests
.\gradlew.bat :portfolio_service_ms:infrastructure:entry-points:kafka-consumer:integrationTest `
              :execution-service-ms:infrastructure:entry-points:kafka-consumer:integrationTest
```

```bash
# WSL — full smoke
bash infrastructure/scripts/start-all.sh
bash infrastructure/scripts/start-services.sh
bash infrastructure/scripts/smoke-all-services.sh
bash infrastructure/scripts/smoke-paper-trading-e2e.sh --dry-run
```

```bash
# Coverage check from repo root, against the merged report
python .github/scripts/check-jacoco-coverage.py --minimum 70
```

## Documentation requirements

When validation is intentionally **not** run, the change summary must
state:

- **what** was skipped,
- **why** it was skipped (non-blocking, environment unavailable, etc.),
- and **what remains** to verify before this can be considered done.

A change with skipped validation is "done with caveats", not "done".

## Forbidden patterns

- Tests that pass by mocking the system under test.
- Tests that depend on machine clock or wall-clock zones.
- Suppressing Sonar issues with comments instead of fixing them.
- Removing or lowering coverage thresholds to pass CI.
- Marking a bug fix as done without a regression test.
