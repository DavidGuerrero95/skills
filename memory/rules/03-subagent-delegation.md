# Subagent delegation rule

## Use a specialized agent when

- the task benefits from a distinct role,
- the role can work with narrower context,
- parallel inspection would reduce cognitive load,
- or the output needs independent review.

## Recommended delegates

- `java-architect`
- `java-implementation-engineer`
- `unit-test-engineer`
- `e2e-test-engineer`
- `code-smell-auditor`
- `failure-investigator`
- `mermaid-architect`
- `technical-writer`
- `security-reviewer`

## Boundaries

- Use at most the minimum number of active delegates needed.
- Avoid deep recursive delegation by default.
- Prefer one implementation agent + one reviewer over many overlapping reviewers.
