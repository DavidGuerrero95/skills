---
name: unit-test-crafter
description: Create or improve focused unit tests for Java code in this repository with readable fixtures, deterministic assertions, and regression coverage.
---


# Unit test crafter

## Use for

- domain behavior
- use cases
- pure mappers
- validation logic
- regression tests for bug fixes

## Rules

- Prefer focused assertions.
- Keep fixtures readable.
- Add `[ClassName]TestData` helpers for repeated setup.
- Avoid weak mock assertions.
- Add a regression test for every bug fix.

## Read first

- `/memory/policies/04-testing-and-quality-gates.md`
- `/memory/policies/01-engineering-baseline.md`

## Output

List:
- test scenarios added,
- defect covered,
- edge cases still not covered.
