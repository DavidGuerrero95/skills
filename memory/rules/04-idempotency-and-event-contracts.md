# 04 — Idempotency and event contracts

## Principles

- **Every evented workflow declares its canonical effect key.**
- **Replays are either harmless no-ops or intentionally handled deltas.**
- **Event envelope, broker submission, fill projection, alert and
  notification effects use distinct keys.** Do not collapse them.

## Per-layer idempotency matrix

This matrix is the operating contract for trading workflows. Any change
that touches one of these layers must keep the column intact.

| Layer                                | Canonical key                                                                                  | Topic / effect                                              | Required behavior                                                                                                                                                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Kafka envelope                        | `eventId`                                                                                      | All consumers with inbox / dedupe                           | Same `eventId` ⇒ effects applied once. Replay identical ⇒ no-op. Same `eventId` + different payload ⇒ contract violation (DLQ + alert).                          |
| Order to broker                       | `clientOrderId`                                                                                | `paper.order.requested.v1` → `execution-service` → Alpaca   | At most one broker submission per `clientOrderId`. Recovery looks up local DB and broker by client id before resubmitting.                                        |
| Fill projection                       | `clientOrderId` + `cumulativeFilledQuantity`                                                   | `paper.order.executed.v1` → `portfolio_service_ms`          | Apply the **positive delta** vs. last seen cumulative. Same cumulative ⇒ duplicate. Lower cumulative ⇒ inconsistent / stale (DLQ + investigation).               |
| Automated exit (rules)                | `portfolioId` + `symbol` + `exitRule` + `marketSnapshotEventId` (DB-unique on `exit_order_request`) | After `market.snapshot.v1` evaluation                      | At most one exit per rule per snapshot. Additional guard: do not emit a SELL while another SELL is pending for the same symbol (`hasPendingExitOrder`).         |
| Analysis-driven SELL/REDUCE thesis    | Analysis `eventId` + risk dedupe                                                               | `analysis.decision.v1` → risk evaluation                    | Same processed/inbox dedupe as other events. Thesis fraction is read from `thesis_invalidation_sell_fraction`.                                                   |
| Hourly portfolio summary              | `portfolioId` + truncated hour (`epochSecond / 3600`)                                          | `portfolio.summary.v1` + `notification.requested.v1`        | One publication per portfolio per hour. Valkey key: `portfolio-summary:{portfolioId}:{epochSecond/3600}`.                                                        |
| Portfolio alert                       | `portfolioId` + `ruleId` + `cooldownWindow`                                                    | `portfolio.alert.triggered.v1` + `notification.requested.v1` | One alert per rule per cooldown window. Valkey key: `portfolio-alert:{portfolioId}:{ruleId}:{epoch/cooldownSec}`.                                                |
| News digest                           | `contentHash` (SHA-256 of url + headline + window)                                             | MongoDB `news_dedupe_memory` + `notification.requested.v1` | Article with same hash is not republished until TTL expires (default 30 days).                                                                                   |

## Review checklist before merging an event-touching change

- What is the **canonical key** at this layer?
- What **effect** is protected by that key?
- What happens on **duplicate delivery**?
- What happens on **same key + different payload**?
- What **downstream projection or notification** changes?
- Is **DLQ behavior** documented with a human-readable reason header?
- Is the **schema change additive and backward-compatible**? If not,
  is there a versioned topic (`...v2`)?
- Are **AsyncAPI** and **JSON Schema** artifacts updated under
  `docs/contracts/`?

## Documentation requirements

Document, in the same change set:

- topic name(s) and version(s),
- producer and consumer ownership (which service publishes / consumes),
- key fields,
- replay behavior,
- DLQ topic name and routing reason,
- env vars introduced or renamed.

Authoritative locations:

- `docs/contracts/topics.md` — topic catalog.
- `docs/contracts/asyncapi/` — AsyncAPI bundles.
- `docs/contracts/json-schema/` — JSON schemas.

## Forbidden patterns

- Reusing `eventId` as the broker submission key.
- Treating `brokerOrderId` as sufficient for fill projection.
- Skipping cooldown / TTL logic in tests "to make them pass".
- Adding a new evented effect without declaring its key in this matrix.
- Renaming a topic field without a versioned topic and a documented
  migration.
