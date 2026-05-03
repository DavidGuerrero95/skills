# Task execution flow

## Default flow

1. Identify the smallest correct scope.
2. Read the applicable policy and rule files.
3. Inspect the impacted codepaths and docs.
4. Decide whether a specialized skill or agent should be used.
5. Make the smallest safe change.
6. Validate at the right level.
7. Update docs if the change affects behavior, contracts, or operations.
8. Report what changed, what was validated, and what remains.

## Escalation

Use specialized agents or skills when the task is:
- test-heavy,
- debugging-heavy,
- cross-service,
- documentation-heavy,
- or architecture-heavy.
