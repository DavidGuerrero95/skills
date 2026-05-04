---
name: reactive-kafka-engineering
description: Implement or review Reactor, WebFlux, Kafka producers/consumers, R2DBC, and event-driven flows with emphasis on non-blocking behavior, layer-specific idempotency, contract safety and DLQ semantics. Use whenever Reactor chains, WebFlux handlers, KafkaTemplate / Reactive Kafka senders, consumers, retries, backpressure, schedulers or reconciliation flows are touched.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: reactor-kafka
  version: "1.1"
---

# Reactive + Kafka engineering

## When to use

- Building or reviewing **Reactor pipelines** (`Mono` / `Flux`).
- WebFlux **handlers** and **routers**, including SSE and streaming.
- **Kafka** producers, listeners, batch consumers, retries, DLQ.
- **R2DBC** repositories and reactive transactions.
- Schedulers (`@Scheduled`, fixed-delay, distributed locks via Valkey).
- Reconciliation flows (e.g. `ReconciliationScheduler`,
  `ReconcileOrdersUseCase`).

## When NOT to use

- Pure synchronous logic that does not cross any IO boundary
  (`skills/java-spring-implementation` is enough).
- Tests-only changes (`skills/unit-test-crafter` or
  `skills/e2e-test-crafter`).

## Read first

- `memory/policies/03-reactive-and-messaging.md`
- `memory/rules/04-idempotency-and-event-contracts.md`
- `memory/policies/06-investment-domain-guardrails.md` (for trading flows)

## Workflow

1. **Map the event path end-to-end.**
   - Producer → topic → consumer → side effect → outbound notification.
   - Identify all canonical keys per layer (envelope `eventId`,
     `clientOrderId`, fill projection, alert cooldown, news hash).
   - Confirm DLQ topic name and routing reason header.

2. **Confirm non-blocking behavior.**
   - No `block()`, `blockFirst()`, `blockLast()` in production.
   - No `subscribe()` in business code; subscription is owned at the
     entry point.
   - Explicit empty-publisher handling (`switchIfEmpty`,
     `defaultIfEmpty`, `Mono.error`).
   - Bounded `flatMap` concurrency on hot streams.

3. **State the idempotency contract.**
   - Same key + same payload ⇒ no-op.
   - Same key + different payload ⇒ DLQ + alert (contract violation).
   - Lower cumulative quantity than last seen ⇒ DLQ + investigation.

4. **Document the contract change.**
   - Update `docs/contracts/topics.md`.
   - Update or add the JSON Schema in `docs/contracts/json-schema/`.
   - Update or add the AsyncAPI bundle in
     `docs/contracts/asyncapi/`.

5. **Add validation.**
   - Unit tests for the use case logic with mocked ports.
   - Integration tests with Testcontainers Kafka for the listener +
     producer wiring.
   - Smoke / E2E if multiple services participate
     (`smoke-paper-trading-e2e.sh`, `smoke-w2-dashboard-e2e.sh`).

6. **Operational hygiene.**
   - Logs include canonical keys (`eventId`, `clientOrderId`).
   - Metrics: lag, retries, in-flight, DLQ count.
   - SCRAM-SHA-512 against `localhost:9094` locally; credentials read
     from `KAFKA_SASL_USERNAME` / `KAFKA_SASL_PASSWORD`.

## Output expected from this skill

Always state, in the change summary:

```
Event path:
 - producer:  <service>  -> topic:<name>:<version>
 - consumer:  <service>  -> effect

Canonical keys:
 - envelope:        eventId
 - <layer>:         <key fields>

Replay behavior:
 - duplicate ⇒ ...
 - same key + different payload ⇒ ...
 - DLQ topic + reason header ⇒ ...

Validation:
 - [ran]   ./gradlew :<service>:test
 - [ran]   ./gradlew :<service>:integrationTest
 - [ran|skip]  bash infrastructure/scripts/smoke-...
```

## Common reactive smells

- A `flatMap` with no concurrency limit fanning out to a downstream
  with limited capacity.
- A `Mono.fromCallable(...)` wrapping JDBC without
  `.subscribeOn(Schedulers.boundedElastic())`.
- A consumer that catches `Throwable` and acks the offset, swallowing
  the failure.
- A retry chain without a maximum attempts cap.
- A `Mono.zip` that hides timeout differences between branches.
- A scheduler running on multiple replicas without a Valkey distributed
  lock.

## Forbidden patterns

- `block()` outside of test scope.
- `subscribe()` in a use case or domain class.
- Silent DLQ swallow (catching and ack-ing without producing to a DLQ).
- Producing without setting an idempotency / canonical key.
- Consuming without declaring DLQ behavior in module docs.
- Treating `eventId` as substitute for `clientOrderId` or fill
  projection key.
