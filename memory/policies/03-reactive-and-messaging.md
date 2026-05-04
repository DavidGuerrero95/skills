# 03 — Reactive and messaging policy

## Purpose

Define the correctness invariants for Reactor pipelines and Kafka
producers/consumers. This file does **not** prescribe how to build a
specific feature — that lives in `skills/reactive-kafka-engineering`.

## Reactor rules

- **No `block()` / `blockFirst()` / `blockLast()` in production code.**
  Test code may block when stepping through a pipeline; production
  flows must remain non-blocking.
- **No casual `subscribe()` in business code.** A subscription is owned
  by the framework boundary (an entry point, a scheduler, a Kafka
  consumer driver). Use cases and domain code return publishers.
- Use `map` for synchronous transforms, `flatMap` for asynchronous work,
  `concatMap` when ordering matters.
- Handle empty publishers deliberately: `switchIfEmpty(...)`,
  `defaultIfEmpty(...)`, or an explicit `Mono.error(...)`. Never assume
  a publisher emits.
- Isolate unavoidable blocking work on `Schedulers.boundedElastic()` —
  for example, a JDBC driver, a synchronous third-party SDK, or a
  legacy library. Document why blocking is unavoidable.
- Use `Mono.defer(...)` when a downstream publisher must remain lazy
  after a possible short-circuit (e.g. cached results invalidated by
  flag changes).
- Apply backpressure-aware operators (`limitRate`, `flatMap` with
  concurrency parameter) on hot streams. Do not let an unbounded
  `flatMap` fan out without a concurrency limit.
- Propagate context (request id, tenant id, idempotency key) using
  `Context`/`contextWrite`. Do not leak via `ThreadLocal`.

## Kafka and messaging rules

- **Treat event contracts as public APIs.** Any change to topic, schema,
  headers, or routing must be backward-compatible by default and
  documented under `docs/contracts/`.
- Producers and consumers are **adapters**. They translate between
  domain events and broker framing; they do not contain business logic.
- Idempotency keys are **layer-specific**. See
  `rules/04-idempotency-and-event-contracts.md` for the per-layer
  matrix.
- Consumers must handle:
  - duplicate delivery → no-op or explicit delta;
  - same key + different payload → DLQ + alert (contract violation);
  - poison message → DLQ with a human-readable reason header;
  - downstream failure → bounded retry with backoff, then DLQ.
- Producers must declare the topic, key strategy, headers, and DLQ
  policy in module-local docs.
- Use SASL_PLAINTEXT + SCRAM-SHA-512 against the local broker
  (`localhost:9094`). Never hardcode credentials; resolve via
  `KAFKA_SASL_USERNAME` / `KAFKA_SASL_PASSWORD` env vars.
- Never reuse one key as a universal idempotency substitute across
  layers. The Kafka `eventId` is for envelope dedupe; `clientOrderId`
  is for broker submission; fill projection uses `clientOrderId +
  cumulativeFilledQuantity`. See the matrix in
  `rules/04-idempotency-and-event-contracts.md`.

## Schema and contract evolution

- New fields are **additive and optional**. Consumers must tolerate
  unknown fields.
- Removing or renaming a field requires a migration: dual-publish, then
  cut over once consumers are updated.
- Breaking changes require a new topic version (`...v2`) and a written
  decision (ADR or `docs/contracts/topics.md` entry).
- AsyncAPI + JSON Schema artifacts under `docs/contracts/asyncapi/` and
  `docs/contracts/json-schema/` must be updated in the same change.

## Operational hygiene

- Producers and consumers expose Micrometer metrics: lag, retries,
  in-flight, DLQ count.
- Logs include the canonical key (e.g. `eventId`, `clientOrderId`).
  Never log credentials, full payloads with PII, or broker secrets.
- Long-running schedulers must use a distributed lock (Valkey
  `SET NX EX`) when more than one replica can run.

## Forbidden patterns

- `block()` in production.
- `subscribe()` in a use case or domain class.
- Catching `Throwable` to silence DLQ routing.
- Manual `ThreadLocal` to propagate request context.
- Producing without setting an idempotency / canonical key.
- Consuming without declaring DLQ behavior.
