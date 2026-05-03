# Reactive and messaging policy

## Reactive rules

- Do not use `block()`, `blockFirst()`, or `blockLast()` in production flows.
- Do not call `subscribe()` inside business code unless the boundary explicitly owns subscription.
- Use `map` for synchronous transforms and `flatMap` for async work.
- Handle empty publishers deliberately.
- Isolate unavoidable blocking work on `Schedulers.boundedElastic()`.
- Use `Mono.defer` when a downstream publisher must remain lazy after a possible short-circuit.

## Messaging and Kafka rules

- Treat event contracts as public APIs.
- Preserve backward compatibility unless there is an explicit migration.
- Make idempotency keys explicit and layer-specific.
- Prefer at-least-once-safe handlers.
- Keep serialization and broker details in adapters.
- Document new topics, schemas, headers, and retry/DLQ behavior.

## Event correctness

- Do not reuse one key as a universal idempotency substitute across layers.
- Separate command intent, broker submission, fill projection, and notification effects.
- When an event becomes the source of truth, update all downstream mappings explicitly.
