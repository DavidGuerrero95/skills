---
name: investment-domain-review
description: Review changes against investment-domain rules, portfolio/risk boundaries, execution responsibilities, notification ownership, idempotency keys per layer, and paper-trading safety constraints. Use whenever order flow, risk logic, alert rules, execution reconciliation, kill-switch behavior or notification ownership is touched.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: investment-domain-safety
  version: "1.1"
---

# Investment-domain review

## When to use

- Order submission path (`paper.order.requested.v1`).
- Risk evaluation and audit events
  (`risk.approved.v1`, `risk.rejected.v1`).
- Execution and reconciliation
  (`paper.order.executed.v1`, kill-switch, broker cancellation).
- Notification ownership (who publishes `trade-fill-summary`,
  `notification.requested.v1`).
- Alert rules and cooldowns (`portfolio.alert.triggered.v1`).
- News dedupe and digest scheduling.
- Any change near the broker boundary (Alpaca paper).

## When NOT to use

- Pure infrastructure or dev tooling changes.
- Changes that do not affect any of the trading topics or services
  listed above.

## Read first

- `memory/policies/06-investment-domain-guardrails.md`
- `memory/rules/04-idempotency-and-event-contracts.md`
- `memory/policies/03-reactive-and-messaging.md`

## Review checklist

Walk this checklist for the diff, in order:

1. **Service boundary preserved?**
   - `market-data → analysis → portfolio/risk → execution → notification`.
   - No service is publishing on behalf of another.
   - `execution-service` only publishes `REJECTED` / `CANCELLED` /
     `FAILED` notifications. `portfolio_service_ms` is the sole
     publisher of `trade-fill-summary`.

2. **Audit-only events stay audit-only?**
   - `risk.approved.v1` carries no executable fields.
   - The executable command is `paper.order.requested.v1`.

3. **Fill projection contract preserved?**
   - Maps `filledQuantity` → executed quantity.
   - Maps `filledPrice` → execution price.
   - Does **not** read `limitPrice`.
   - Preserves `assetClass` and `currency` from the original request.

4. **Idempotency keys match the matrix?**
   - Cross-check with `rules/04-idempotency-and-event-contracts.md`.
   - Each layer declares its own canonical key.

5. **Risk parameters live in PostgreSQL?**
   - New risk knobs are added to `risk.risk_policy_asset_class_rule`
     or `risk.portfolio_alert_rule`, not to env vars.
   - Operational tuning knobs (TTLs, cooldowns) are env vars with
     defaults.

6. **Notification routing is correct?**
   - Trading signals → `telegram:business`.
   - News digests → `telegram:news` (no fallback; missing chat id
     means DLQ).
   - Long messages split into `Part i/N`.

7. **Distributed locks and TTLs preserved?**
   - Schedulers use Valkey `SET NX EX` (`ValkeyReconciliationLockAdapter`
     and similar).
   - Cooldown windows use Valkey keys with a deterministic naming
     pattern.

8. **Documentation updated?**
   - `docs/contracts/topics.md` reflects any topic / schema change.
   - Affected service README is updated.
   - If a runbook is impacted, it is updated in the same change.

## Output expected from this skill

```
Boundary reviewed:
 - <service / topic / layer>

Safety assumptions:
 - <bullet>

Risks of regression:
 - <bullet>

Downstream consumers affected:
 - <service> consumes <topic>

Remediation required:
 - <bullet> (if any)
```

## Forbidden patterns

- Hardcoding a non-paper broker URL.
- Adding executable fields to `risk.approved.v1`.
- Letting `execution-service` publish enriched fill notifications.
- Moving risk parameters out of PostgreSQL into env vars.
- Bypassing Valkey cooldowns or distributed locks "for testing".
- Treating `eventId` as a substitute for layer-specific idempotency
  keys.
