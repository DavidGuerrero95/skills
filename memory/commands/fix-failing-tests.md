# /fix-failing-tests

Stabilize failing tests by identifying the root cause, fixing the
smallest safe issue, and keeping or improving coverage.

## Steps

1. Reproduce the failing test deterministically.
2. Distinguish symptom from cause; narrow the boundary.
3. State the root cause in one sentence with file:line.
4. Decide whether the fix belongs in:
   - production code (real bug),
   - test setup (incorrect fixture),
   - test assertion (incorrect expectation).
5. Apply the smallest fix.
6. Re-run the test plus the impacted module's suite.
7. If the test was disabled or quarantined, remove the marker and
   leave a note.

## Recommended delegates

- `failure-investigator` (lead)
- `unit-test-engineer` for fixture / assertion fixes
- `e2e-test-engineer` when the failing path is a smoke / E2E
