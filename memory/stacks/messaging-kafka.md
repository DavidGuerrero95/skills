# Stack — Kafka / event streaming

Concrete conventions for Apache Kafka (or a compatible broker). Universal
async/messaging invariants stay in `policies/03-async-and-messaging.md`
and `rules/04-idempotency-and-event-contracts.md`; this profile adds the
Kafka specifics.

## When to use

The repository produces/consumes events over Kafka (Reactive Kafka,
Spring Kafka, confluent-kafka, kafkajs, etc.).

## Topic & message conventions

- **Topic naming:** `<domain>.<entity>.<event>.v<N>`, e.g.
  `orders.order.placed.v1`. Version in the name; a breaking change is a
  new `v2` topic.
- **Keying:** key by the entity id that must stay ordered
  (`orderId`, `userId`) so a partition preserves per-entity order.
- **Envelope:** every message carries `eventId`, `occurredAt`,
  `schemaVersion`, and a `correlationId` header.
- **Serialization:** a schema registry (Avro/Protobuf/JSON Schema) is
  preferred; otherwise JSON with an explicit, documented schema under
  `docs/contracts/`.

## Producer rules

- Idempotent producer (`enable.idempotence=true`, `acks=all`).
- Set the canonical/idempotency key on every message
  (`rules/04-idempotency-and-event-contracts.md`).
- Declare topic, key strategy, headers, and dead-letter policy in
  module-local docs.
- Use the transactional/outbox pattern when a DB write and a publish must
  be atomic — never dual-write without one.

## Consumer rules

- **Manual commit after successful processing**, not auto-commit before.
- Dedupe on the envelope id (inbox table / cache) for
  effectively-once processing.
- Define behavior for: duplicate, same-key-different-payload
  (dead-letter + alert), poison message (dead-letter + reason header),
  downstream failure (bounded retry + backoff, then dead-letter).
- Bound concurrency; do not fan out unbounded from a partition.
- Keep consumers non-blocking (`policies/03-async-and-messaging.md`).

## Dead-letter & retries

- One dead-letter topic per source topic (`<topic>.dlq.v<N>`) with a
  human-readable `x-dead-letter-reason` header.
- Retries are bounded and backed off; retry storms are prevented with a
  retry topic or delayed retry, not a tight loop.

## Security & ops

- Auth via SASL/TLS; credentials from env vars, never hardcoded.
- Expose metrics: consumer lag, retries, in-flight, DLQ count.
- Integration tests use a real broker via Testcontainers Kafka.

## Forbidden patterns

- Auto-commit before the effect is applied.
- Producing without an idempotency/canonical key.
- Dual-writing to DB and Kafka without outbox/transaction.
- Unbounded fan-out from a consumer.
- Swallowing failures instead of routing to a dead-letter topic.
- Breaking a topic schema in place instead of versioning it.
