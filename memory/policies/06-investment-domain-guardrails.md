# 06 — Investment-domain guardrails

## Purpose

Define the safety boundaries that protect the **investment domain** in
this repository. The repository is a personal investment platform
(INVEXA), not a generic CRUD system. This policy is non-negotiable.

The skill `skills/investment-domain-review/SKILL.md` operationalizes
these guardrails when reviewing concrete diffs.

## Service responsibilities (single source of truth)

| Service                          | Port  | Owns                                                                                                |
| -------------------------------- | ----- | --------------------------------------------------------------------------------------------------- |
| `market-data-service-ms`         | 8083  | Price, news and calendar ingestion. Publishes `market.snapshot.v1`, `news.batch.v1`, `market.calendar.v1`. |
| `analysis-agent-service-ms`      | 8085  | LLM analysis (Ollama primary, OpenAI fallback). News dedupe + digest scheduler. Publishes `analysis.decision.v1`, `notification.requested.v1`. |
| `portfolio_service_ms`           | 8086  | Portfolio book of record + risk evaluator + alerts. Publishes `risk.approved.v1`, `paper.order.requested.v1`, `kill-switch.activated.v1`, enriched fill notifications. |
| `execution-service-ms`           | 8089  | Paper order submission to Alpaca + reconciliation. Publishes `paper.order.executed.v1`. Notifications limited to `REJECTED` / `CANCELLED` / `FAILED`. |
| `notification-service-ms`        | 8087  | Multi-channel delivery (Telegram + email). Resolves `telegram:business` / `telegram:news` aliases. |

A change that crosses these boundaries (for example moving notification
ownership) requires a domain review.

## Trading safety rules

- **Paper-trading only.** No real-money execution path may be enabled
  by default. Any change near the broker boundary preserves the
  "paper" defaults.
- **Risk parameters live in PostgreSQL.** Tables under `risk.*` (such
  as `risk.risk_policy_asset_class_rule` and
  `risk.portfolio_alert_rule`) are the source of truth for trading
  rules and alerts. Do not move functional parameters into ad-hoc env
  vars.
- **Audit-only events stay audit-only.** `risk.approved.v1` is
  audit-only and **does not** carry executable fields.
  `paper.order.requested.v1` is the executable command.
- **Fill projection** is owned by `portfolio_service_ms`. It uses
  `paper.order.executed.v1` (`filledQuantity`, `filledPrice`,
  `filledNotional`) and applies only positive deltas. It does not
  read `limitPrice` for fill projection.
- **Enriched fill notifications** are published only by
  `portfolio_service_ms` (`trade-fill-summary`, recipient
  `telegram:business`). `execution-service` only notifies for
  `REJECTED`, `CANCELLED`, `FAILED`.
- **Kill-switch** flushes pending orders. Orders without a
  `brokerOrderId` are cancelled locally; orders with one go through
  `BrokerGateway.cancelOrder`. Failures are logged and reconciled by
  the next scheduler tick.
- **Reconciliation** runs every `EXECUTION_RECONCILIATION_FIXED_DELAY`
  (default `PT5M`) under a Valkey distributed lock.

## Notification ownership

- `telegram:business` → trading signals (orders, fills, kill switch).
  Resolved from `NOTIFICATION_TELEGRAM_BUSINESS_CHAT_ID`.
- `telegram:news` → news digests only. Resolved from
  `NOTIFICATION_TELEGRAM_NEWS_CHAT_ID`. **No fallback** — missing value
  routes to DLQ.
- Long messages (> 4096 chars) split into `Part i/N`. Beyond
  `NOTIFICATION_TELEGRAM_MAX_PARTS * 4096` characters, fail fast with
  `TELEGRAM_MESSAGE_TOO_LONG` and route to
  `notification.requested.dlq.v1`.

## Idempotency expectations

Idempotency is per-layer. The detailed matrix is in
`rules/04-idempotency-and-event-contracts.md`. At policy level:

- Every evented workflow declares its **canonical effect key**.
- Replays are either harmless no-ops or intentionally handled deltas.
- Event envelope, broker submission, fill projection and notification
  effects each use their own key.

## Change discipline

Any change that touches:

- order submission,
- reconciliation,
- drawdown / risk logic,
- alert rules,
- kill switch,
- enriched fill notifications,
- or event contracts,

must include:

- a domain review (`agents/investment-domain-review` or human review),
- updated documentation in `docs/contracts/topics.md` and the affected
  service README,
- a smoke / E2E run that exercises the changed path
  (`smoke-paper-trading-e2e.sh`, `smoke-w2-dashboard-e2e.sh`, or
  equivalent).

## Forbidden patterns

- Hardcoding a non-paper broker URL.
- Adding executable fields to `risk.approved.v1`.
- Letting `execution-service` publish enriched fill notifications.
- Moving risk parameters out of PostgreSQL into env vars.
- Bypassing `Valkey` cooldowns or distributed locks "for testing".
- Treating `eventId` as a substitute for layer-specific idempotency
  keys.
