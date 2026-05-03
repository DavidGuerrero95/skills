# Testing and quality-gates policy

## Minimum validation

- Compile the changed module or feature path.
- Run targeted unit tests for touched behavior.
- Run integration tests when adapters, persistence, messaging, or contracts change.
- Run smoke or end-to-end scripts when the task crosses service boundaries.

## Quality expectations

- Treat Sonar bugs and vulnerabilities as blockers.
- Keep tests readable and deterministic.
- Prefer focused assertions over overly permissive mocks.
- Avoid Mockito `eq()` unless there is no better option.
- Add regression coverage for every bug fix.
- Update fixtures/builders instead of duplicating setup inline.

## Documentation requirements

When tests or validation are intentionally not run, state:
- what was skipped,
- why,
- and what remains to verify.
