# /audit-code-smells

Run a focused smell and maintainability review over the changed area
only. Behavior-preserving cleanup, not redesign.

## Steps

1. Bound the audit to the diff or named module.
2. Catalog smells before changing anything (file:line + one-sentence
   description).
3. Apply behavior-preserving fixes in safe order: renames → dead-code
   removal → structural moves.
4. Run impacted module tests after each meaningful change.
5. Surface deferred smells with a reason.

## Recommended delegates

- `code-smell-auditor` (lead)
- `java-architect` when a fix would require an architectural decision
