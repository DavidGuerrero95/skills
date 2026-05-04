# /write-e2e-tests

Design or update smoke / E2E validation for a cross-service or
operator-visible workflow.

## Steps

1. State the workflow: trigger, path, expected observable outcome.
2. Reuse a canonical script when possible:
   - `infrastructure/scripts/smoke-all-services.sh`
   - `infrastructure/scripts/smoke-paper-trading-e2e.sh`
   - `infrastructure/scripts/smoke-paper-trading-sell-e2e.sh`
   - `infrastructure/scripts/smoke-w2-dashboard-e2e.sh`
   - `infrastructure/scripts/test-news-notification.sh`
3. Document prerequisites (`infrastructure/.env.local`, `start-all.sh`,
   `start-services.sh`).
4. Author or extend the script: `[OK]/[FAIL]` lines, summary
   `N/N passed`, exit code reflects success.
5. Document failure signals (DLQ topic, log line, dashboard).
6. Run end-to-end before declaring done; capture the pass count.

## Recommended delegates

- `e2e-test-engineer` (lead)
- `technical-writer` when the runbook is impacted
- `mermaid-architect` when a sequence diagram should accompany the
  smoke
