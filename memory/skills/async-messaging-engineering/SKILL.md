---
name: async-messaging-engineering
description: Implement or review asynchronous code and message/event producers and consumers (Reactor, async/await, coroutines; Kafka, RabbitMQ, SQS) with emphasis on non-blocking behavior, layer-specific idempotency, contract safety, and dead-letter semantics. Use whenever async pipelines, consumers, producers, retries, backpressure, schedulers, or reconciliation flows are touched.
license: MIT
metadata:
  scope: async-and-messaging
  version: "2.0"
---

# Async + messaging engineering

## When to use

- Building or reviewing **async pipelines** (Reactor `Mono`/`Flux`,
  Python `async`/`await`, Node promises, Kotlin coroutines).
- **Message/event** producers, consumers, batch handlers, retries,
  dead-letter routing.
- Streaming handlers (SSE, WebSocket, chunked responses).
- Schedulers and reconciliation flows, including distributed locks.

## When NOT to use

- Pure synchronous logic that never crosses an IO boundary
  (`skills/feature-implementation` is enough).
- Tests-only changes (`skills/unit-test-crafter`,
  `skills/e2e-test-crafter`).

## Read first

- `memory/policies/03-async-and-messaging.md`
- `memory/rules/04-idempotency-and-event-contracts.md`
- `memory/stacks/messaging-kafka.md` (when Kafka is the broker)
- `memory/policies/06-domain-guardrails.md` (for domain-critical flows)

## Workflow

1. **Map the event path end-to-end.**
   - Producer → topic/queue → consumer → side effect → outbound
     notification.
   - Identify the canonical key per layer (envelope id, command id,
     projection counter, cooldown window, content hash).
   - Confirm the dead-letter destination and its reason header.

2. **Confirm non-blocking behavior.**
   - No blocking calls on the async runtime in production.
   - Subscription/await owned at the boundary, not in business code.
   - Explicit empty/absent handling.
   - Bounded concurrency on hot streams.

3. **State the idempotency contract.**
   - Same key + same payload ⇒ no-op.
   - Same key + different payload ⇒ dead-letter + alert.
   - Stale/out-of-order (lower counter) ⇒ dead-letter + investigation.

4. **Document the contract change.**
   - Update the catalog and schema under `docs/contracts/`
     (OpenAPI / AsyncAPI / JSON Schema / Avro).

5. **Add validation.**
   - Unit tests for the use-case logic with mocked ports.
   - Integration tests with a real broker (Testcontainers).
   - Smoke / E2E when multiple modules participate.

6. **Operational hygiene.**
   - Logs include canonical keys; metrics for lag, retries, in-flight,
     dead-letter count. Credentials from env vars.

## Output expected from this skill

```
Event path:
 - producer:  <module> -> topic/queue:<name>:<version>
 - consumer:  <module> -> effect

Canonical keys:
 - envelope:  <id field>
 - <layer>:   <key fields>

Replay behavior:
 - duplicate ⇒ ...
 - same key + different payload ⇒ ...
 - dead-letter destination + reason header ⇒ ...

Validation:
 - [ran]   <unit test command>
 - [ran]   <integration test command>
 - [ran|skip] <smoke/E2E>
```

## Common async smells

- Unbounded fan-out overwhelming a limited downstream.
- A blocking driver call wrapped in an async wrapper without offloading
  to a worker pool.
- A consumer that swallows the error and commits the offset.
- A retry chain without a maximum attempt cap.
- Combining branches that hide timeout differences between them.
- A scheduler running on multiple replicas without a distributed lock.

## Forbidden patterns

- Blocking the async runtime in production.
- Fire-and-forget subscription/await inside a use case or domain class.
- Silent dead-letter swallow (catch + commit without routing).
- Producing without a canonical/idempotency key.
- Consuming without declaring dead-letter behavior.
- Reusing the envelope id as the external-submission or projection key.
