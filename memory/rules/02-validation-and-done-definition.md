# 02 — Validation and Definition of Done

## Definition of Done

A task is **done** only when all applicable items are satisfied. Items
that do not apply to a given change should be marked as such in the
summary, never silently dropped.

A task is done when:

- code lives in the **correct layer**;
- no obvious **architecture regression** was introduced;
- touched modules **build / type-check**;
- relevant **tests run** (or the omission is explained with a reason);
- contract-impacting changes are **documented** in `docs/contracts/` and
  the affected module README;
- diagrams and runbooks are updated when behavior or operations changed
  (`rules/05-diagrams-and-docs.md`);
- no secret or destructive command was introduced
  (`policies/05-security-and-secrets.md`);
- merge gates (format, lint/static analysis, coverage threshold) are not
  weakened;
- the change summary states the **exact validation performed** and what
  remains open.

## Validation ladder

Pick the **lowest** rung that still proves correctness. Climb when the
change reaches that scope.

| Scope of change                                                   | Required validation                                                         |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Pure logic in a single unit (domain rule, mapper, value object)   | Unit tests that exercise the new branch + at least one edge case            |
| Use-case orchestration                                            | Unit tests of the use case + tests for the new ports it depends on          |
| Adapter / persistence / messaging                                 | Integration tests with Testcontainers / ephemeral services                  |
| HTTP handler / router                                             | Slice / endpoint test + at least one unhappy path                           |
| Multi-module / multi-service workflow                             | Smoke or E2E across the participating modules                               |
| Contract change (HTTP, event, schema, env var)                    | Tests above + docs update + schema (OpenAPI / AsyncAPI / JSON Schema) review |
| Bug fix                                                           | Failing regression test that reproduces the bug, then the fix               |

## Concrete commands

Use the commands from the active stack profile. Representative examples:

```bash
# Java + Gradle
./gradlew :<module>:test
./gradlew spotlessCheck test jacocoTestCoverageVerification

# Python + FastAPI (see stacks/python-fastapi.md)
ruff check . && mypy . && pytest -q --cov

# Node + TypeScript (see stacks/node-typescript.md)
npm run lint && npm run typecheck && npm test

# Container smoke / local infra (see stacks/docker-compose.md)
docker compose up -d && ./scripts/smoke.sh
```

## Reporting validation

Always end with a structured note in the change summary:

```
Validation:
- [ran]   ./gradlew :payments:test
- [ran]   pytest tests/orders -q
- [skip]  full E2E (no docker on host this session)
Open:     run live E2E in staging; verify webhook delivery
```

If something is skipped, state **why** and **what remains** explicitly.

## Forbidden patterns

- Reporting "tests pass" when only some tests ran.
- Reducing coverage to make CI green.
- Hiding a skipped validation under a vague phrase ("I tested locally").
- Treating a failing flaky test as "infrastructure noise" without filing
  a follow-up.
