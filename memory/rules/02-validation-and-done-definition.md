# 02 — Validation and Definition of Done

## Definition of Done

A task is **done** only when all applicable items are satisfied. Items
that do not apply to a given change should be marked as such in the
summary, never silently dropped.

A task is done when:

- code lives in the **correct layer**;
- no obvious **architecture regression** was introduced;
- touched modules **compile**;
- relevant **tests run** (or the omission is explained with a reason);
- contract-impacting changes are **documented** in
  `docs/contracts/topics.md` and the affected service README;
- diagrams and runbooks are updated when behavior or operations
  changed (`rules/05-diagrams-and-docs.md`);
- no secret or destructive command was introduced
  (`policies/05-security-and-secrets.md`);
- merge gates (Spotless, Sonar bugs/vulns, JaCoCo ≥ 70 %) are not
  weakened;
- the change summary states the **exact validation performed** and
  what remains open.

## Validation ladder

Pick the **lowest** rung that still proves correctness. Climb when the
change reaches that scope.

| Scope of change                                                     | Required validation                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Pure logic in a single class (domain rule, mapper, value object)    | Unit tests that exercise the new branch + at least one edge case                |
| Use case orchestration                                              | Unit tests of the use case + tests for the new ports it depends on              |
| Adapter / persistence / messaging                                   | Integration tests with Testcontainers (broker, DB, cache)                       |
| HTTP handler / WebFlux router                                       | Slice test (`@WebFluxTest`) + at least one unhappy path                         |
| Multi-service workflow                                              | Smoke or E2E (`smoke-paper-trading-e2e.sh`, `smoke-w2-dashboard-e2e.sh`)        |
| Contract change (Kafka, REST, schema, env var)                      | Tests above + docs update + AsyncAPI / JSON schema review                       |
| Bug fix                                                             | Failing regression test that reproduces the bug, then the fix                   |

## Concrete commands

```powershell
# Per service — Windows PowerShell
.\gradlew.bat :<service>:<module>:test

# Full per service with coverage
.\gradlew.bat :<service>:clean :<service>:test :<service>:jacocoMergedReport :<service>:jacocoTestCoverageVerification --no-daemon

# Targeted Kafka integration tests
.\gradlew.bat :portfolio_service_ms:infrastructure:entry-points:kafka-consumer:integrationTest `
              :execution-service-ms:infrastructure:entry-points:kafka-consumer:integrationTest
```

```bash
# WSL — bring up infra, run smoke
bash infrastructure/scripts/start-all.sh
bash infrastructure/scripts/start-services.sh
bash infrastructure/scripts/smoke-all-services.sh
bash infrastructure/scripts/smoke-paper-trading-e2e.sh --dry-run
```

```bash
# Coverage check from repo root, against the merged report
python .github/scripts/check-jacoco-coverage.py --minimum 70
```

## Reporting validation

Always end with a structured note in the change summary:

```
Validation:
- [ran]   ./gradlew :portfolio_service_ms:test
- [ran]   bash infrastructure/scripts/smoke-paper-trading-e2e.sh --dry-run
- [skip]  full smoke-all-services.sh (no docker on host this session)
Open:     run live paper E2E during NYSE hours; verify FILLED on Alpaca
```

If something is skipped, state **why** and **what remains** explicitly.

## Forbidden patterns

- Reporting "tests pass" when only some tests ran.
- Reducing coverage to make CI green.
- Hiding a skipped validation under a vague phrase ("I tested locally").
- Treating a failing flaky test as "infrastructure noise" without
  filing a follow-up.
