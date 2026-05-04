---
name: e2e-test-crafter
description: Create or refine end-to-end and smoke validation for multi-service flows, operator scripts, messaging pipelines, reconciliation paths and notification fan-out in INVEXA. Use whenever a workflow crosses service boundaries, an operator runbook needs a smoke check, or a Kafka contract change must be validated end-to-end.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: smoke-e2e
  version: "1.1"
---

# E2E + smoke test crafter

## When to use

- Multi-service workflows (paper-trading BUY/SELL, kill-switch, news
  pipeline, dashboard alerts).
- Smoke scripts that operators run to verify a deploy.
- Messaging pipelines where multiple topics participate.
- Reconciliation flows and notification fan-out.

## When NOT to use

- Single-class behavior — use `skills/unit-test-crafter`.
- Adapter-only behavior (Kafka producer ↔ broker, R2DBC repository ↔
  PostgreSQL) — use a Testcontainers integration test inside the
  module.
- Documentation-only changes — use `skills/technical-doc-writer`.

## Read first

- `memory/policies/04-testing-and-quality-gates.md`
- `memory/policies/06-investment-domain-guardrails.md`
- `memory/rules/02-validation-and-done-definition.md`
- `memory/rules/04-idempotency-and-event-contracts.md`

## Workflow

1. **State the workflow under test.**
   - Trigger (HTTP call, scheduler tick, operator command).
   - Path (services, topics, side effects).
   - Expected observable outcome (DB row, Kafka message, Telegram
     notification, log line).

2. **Reuse existing scripts when possible.**
   - `infrastructure/scripts/smoke-all-services.sh`
   - `infrastructure/scripts/smoke-paper-trading-e2e.sh`
   - `infrastructure/scripts/smoke-paper-trading-sell-e2e.sh`
   - `infrastructure/scripts/smoke-w2-dashboard-e2e.sh`
   - `infrastructure/scripts/test-news-notification.sh`

   Add to one of these before introducing a new script.

3. **Document prerequisites.**
   - `infrastructure/.env.local` populated.
   - `start-all.sh` and `start-services.sh` ran successfully.
   - Optional: NYSE hours for live broker fills.

4. **Author or extend the script.**
   - Bash scripts use `set -euo pipefail`.
   - Each assertion writes a `[OK] ...` or `[FAIL] ...` line.
   - Final exit code reflects success/failure.
   - The script summarizes assertion counts (`17/17 passed`).

5. **Make assertions operator-readable.**
   - Use the canonical event names (`paper.order.requested.v1`,
     `paper.order.executed.v1`, `portfolio.alert.triggered.v1`,
     `notification.requested.v1`, `trade-fill-summary`).
   - Use the canonical recipient aliases (`telegram:business`,
     `telegram:news`).

6. **Document failure signals.**
   - Which DLQ topic to inspect (`paper.order.executed.dlq.v1`,
     `notification.requested.dlq.v1`).
   - Which log line to grep for.
   - Which Grafana / Prometheus panel to open.

7. **Run the script** end-to-end before declaring done. Capture the
   final pass count in the change summary.

## Output expected from this skill

```
Workflow: <one-line description>
Trigger:  <HTTP / Kafka / scheduler / operator>
Services involved: <list>
Topics involved:   <list>

Prerequisites:
 - infrastructure/.env.local populated
 - bash infrastructure/scripts/start-all.sh
 - bash infrastructure/scripts/start-services.sh

Commands:
 - bash infrastructure/scripts/smoke-...sh

Assertions performed:
 - <bullet>

Failure signals:
 - DLQ topic   ⇒ <name>
 - Log line    ⇒ <pattern>
 - Dashboard   ⇒ <panel>

Validation run:
 - [ran]  bash infrastructure/scripts/smoke-...sh  (N/N passed)
```

## Forbidden patterns

- A smoke script that exits 0 on partial failure.
- An E2E run that depends on cached fixtures from a previous run
  without explicit reset steps.
- Hardcoding chat ids or broker URLs into the script.
- Writing a brand-new script when one of the canonical scripts could
  be extended.
