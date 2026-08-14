# /root-cause-analysis

Investigate a defect, identify the narrowest credible root cause,
propose the safest fix, and add regression validation.

**Pipeline:** `memory/pipelines/bug-fix.md` (ordered stages + gates).

## Steps

1. Reproduce or restate the failure (one paragraph).
2. Bisect the path: which module, which unit.
3. Inspect logs, dead-letter destinations, and dashboards.
4. State the root cause in one sentence, with file:line.
5. Write the failing regression test first.
6. Apply the smallest safe fix in the right layer.
7. Validate: regression test + impacted module's tests + smoke when the
   bug crosses modules.
8. Summarize cause, fix, validation, follow-ups.

## Recommended delegates

- `failure-investigator` (lead)
- `unit-test-engineer` or `e2e-test-engineer` depending on the bug path
- `database-engineer` when the cause is a schema / query issue
- `code-reviewer` when the fix is non-trivial
