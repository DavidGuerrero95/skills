# 03 — Async and messaging policy

## Purpose

Define the correctness invariants for asynchronous code and for
message/event producers and consumers. This file is stack-agnostic: it
holds whether concurrency is expressed with Reactor `Mono`/`Flux`,
Python `async`/`await`, Node promises, Go goroutines, or Kotlin
coroutines. Concrete broker/runtime detail lives in
`stacks/messaging-kafka.md`; feature workflow lives in
`skills/async-messaging-engineering`.

## Async correctness rules

- **Do not block an async runtime.** Never call a blocking API from
  inside a non-blocking event loop / reactive chain / coroutine
  scheduler (no `.block()` in Reactor production code, no synchronous IO
  inside an `async def`, no blocking calls on a Node event loop). Isolate
  unavoidable blocking work on a dedicated pool
  (`Schedulers.boundedElastic()`, `run_in_executor`, a worker thread) and
  document why.
- **Ownership of subscription/await lives at the boundary.** Core and
  use-case code returns publishers / coroutines / promises; the framework
  boundary (entry point, scheduler, consumer driver) is what subscribes,
  awaits, or drives them.
- **Handle the empty / absent case deliberately.** `switchIfEmpty`,
  `defaultIfEmpty`, an explicit error, `None` handling, or an empty-list
  branch — never assume a stream or optional emits.
- **Bound concurrency and fan-out.** Apply backpressure or a concurrency
  limit on hot paths (`flatMap` with a concurrency arg, a bounded
  semaphore, a worker-pool size). Do not let unbounded fan-out overwhelm
  a downstream.
- **Propagate context explicitly** (request id, tenant id, idempotency
  key) via the runtime's context mechanism (Reactor `Context`,
  `contextvars`, async-local storage) — not via thread-locals or
  globals.
- **Always bound retries and timeouts.** Every remote call has a timeout;
  every retry chain has a maximum attempt count and backoff.

## Messaging rules

- **Treat event contracts as public APIs.** Any change to topic, schema,
  headers, or routing must be backward-compatible by default and
  documented under `docs/contracts/`.
- Producers and consumers are **adapters**. They translate between
  domain events and broker framing; they do not contain business logic.
- Idempotency keys are **layer-specific**. See
  `rules/04-idempotency-and-event-contracts.md` for the matrix and
  template.
- Consumers must define behavior for:
  - duplicate delivery → no-op or explicit delta;
  - same key + different payload → dead-letter + alert (contract
    violation);
  - poison message → dead-letter with a human-readable reason header;
  - downstream failure → bounded retry with backoff, then dead-letter.
- Producers must declare the topic, key strategy, headers, and
  dead-letter policy in module-local docs.
- Never hardcode broker credentials. Resolve them from environment
  variables documented in `.env.example`.

## Schema and contract evolution

- New fields are **additive and optional**. Consumers must tolerate
  unknown fields.
- Removing or renaming a field requires a migration: dual-publish, then
  cut over once consumers are updated.
- Breaking changes require a new versioned topic (`...v2`) and a written
  decision (ADR or `docs/contracts/` entry).
- Machine-readable schemas (JSON Schema, Avro, Protobuf, AsyncAPI) under
  `docs/contracts/` are updated in the same change.

## Operational hygiene

- Producers and consumers expose metrics: lag, retries, in-flight,
  dead-letter count.
- Logs include the canonical key (e.g. `eventId`, `orderId`,
  `correlationId`). Never log credentials or full payloads with PII.
- Long-running schedulers use a distributed lock (e.g. Redis/Valkey
  `SET NX EX`) when more than one replica can run.

## Forbidden patterns

- Blocking calls on an async runtime in production code.
- `subscribe()` / fire-and-forget awaits inside a use case or domain
  class.
- Catching the broadest error type to silence dead-letter routing.
- Thread-locals / globals to propagate request context across async
  hops.
- Producing without setting an idempotency / canonical key.
- Consuming without declaring dead-letter behavior.
