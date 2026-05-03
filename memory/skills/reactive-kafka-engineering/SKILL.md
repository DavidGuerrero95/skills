---
name: reactive-kafka-engineering
description: Implement or review Reactor, WebFlux, Kafka, R2DBC, and event-driven flows with emphasis on non-blocking behavior, idempotency, contract safety, and throughput.
---


# Reactive Kafka engineering

## When to use

Use this skill for:
- Reactor chains
- WebFlux handlers
- Kafka producers/consumers
- async orchestration
- event-driven refactors
- retry, timeout, backpressure, dedupe, and reconciliation concerns

## Read first

- `/memory/policies/03-reactive-and-messaging.md`
- `/memory/rules/04-idempotency-and-event-contracts.md`

## Checks

- No accidental blocking in production flow.
- No casual `subscribe()` in business logic.
- Empty publisher behavior is explicit.
- Idempotency key is stated per layer.
- Contract changes are documented.
- Retry/DLQ semantics are visible.

## Deliverable

Explain:
- the event path,
- canonical keys,
- retry behavior,
- validation performed.
