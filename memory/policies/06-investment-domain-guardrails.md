# Investment domain guardrails

## Context

This repository is an investment platform, not a generic CRUD system.

## Rules

- Preserve paper-trading safety boundaries unless a task explicitly changes them.
- Respect risk-policy ownership and parameter sources.
- Keep idempotency explicit for alerts, orders, fills, and notifications.
- Do not move critical functional parameters into ad hoc environment variables when they belong in data/config tables.
- Distinguish audit-only events from executable events.
- Keep enriched fill notifications owned by the correct service boundary.
- Preserve clear separation between market-data ingestion, analysis, portfolio/risk, execution, and notification responsibilities.

## Change discipline

Any change affecting:
- order submission,
- reconciliation,
- drawdown logic,
- alert rules,
- or event contracts

must include validation of downstream effects and updated documentation.
