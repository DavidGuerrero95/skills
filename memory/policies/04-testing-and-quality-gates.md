# 04 — Testing and quality gates

## Purpose

Define the minimum validation expected for any change, and the merge
gates that block work from landing. This file is stack-agnostic; the
exact commands for a given stack live in that stack's profile and the
validation ladder lives in
`rules/02-validation-and-done-definition.md`.

## Minimum validation per change

- **Build / type-check** the changed module or feature path.
- **Run targeted unit tests** for touched behavior.
- **Run integration tests** when adapters, persistence, messaging, or
  contracts change (use real dependencies via Testcontainers / ephemeral
  services, not mocks of the protocol surface).
- **Run smoke / E2E** when the task crosses module or service boundaries
  or affects an operator-visible workflow.
- **Re-run the formatter and linter** on touched files.

## Quality expectations

- **Tests are first-class code.** They are reviewed and refactored with
  the production code they cover.
- Tests must be **deterministic**. No `sleep`-based timing, no
  time-of-day assertions, no flaky network calls.
- Prefer **focused assertions** on the observable effect, not on whether
  a method was called. Assert on captured values, not loose matchers.
- Add a **regression test for every bug fix.** A fix without a failing
  test reproducing the bug is incomplete.
- Reuse named **test-data builders / fixtures** instead of duplicating
  setup across files.
- Use **Testcontainers or ephemeral services** for adapter integration
  tests (databases, brokers, caches). Do not mock the protocol surface.

## Merge gates (blocking)

- **Formatter** clean (Spotless / Prettier / Black / gofmt — per stack).
- **Linter / static analysis** clean on the change set; bugs and
  vulnerabilities are blockers (ruff/mypy, ESLint/tsc, Sonar, etc.).
- **Coverage** meets the project threshold (default **≥ 70 % line
  coverage**; adjust per repository in the stack profile). Never lower
  the threshold to make CI pass.
- **CI pipeline** (`.github/workflows/ci.yml`) green for the branch
  before requesting review.

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
- Suppressing static-analysis issues with inline comments instead of
  fixing them.
- Removing or lowering coverage thresholds to pass CI.
- Marking a bug fix as done without a regression test.
