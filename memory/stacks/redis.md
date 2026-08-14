# Stack — Redis / Valkey

Conventions for using Redis or Valkey (Redis-compatible) as a cache,
distributed lock, rate limiter, or ephemeral store.

## When to use

The repository needs fast key-value access for caching, deduplication,
cooldown windows, distributed locks, rate limiting, or transient state.
Redis/Valkey is **not** a system of record — durable data lives in the
primary datastore.

## Key conventions

- **Namespaced keys** with a deterministic scheme:
  `<service>:<entity>:<id>[:<window>]`, e.g.
  `orders:idempotency:{orderId}` or `summary:{userId}:{epoch/3600}`.
- **Always set a TTL** on ephemeral keys (`SET … EX`, `EXPIRE`). A key
  with no expiry is a memory leak unless it is intentionally permanent.
- Choose data structures deliberately: strings for flags/counters,
  hashes for small objects, sorted sets for leaderboards/queues, sets
  for membership.

## Common patterns

- **Cache-aside:** read cache → miss → load from source → populate with
  TTL. Guard against stampedes on hot keys (jittered TTL, single-flight,
  or a short lock).
- **Idempotency / dedupe:** `SET key value NX EX <ttl>` — the `NX`
  guarantees first-writer-wins; the TTL bounds the dedupe window.
- **Distributed lock:** `SET lock token NX EX <ttl>` to acquire; release
  only if the token matches (Lua compare-and-delete). Set the TTL longer
  than the critical section; renew for long tasks. For strong guarantees
  use Redlock or a dedicated coordinator — a single-node lock can be lost
  on failover.
- **Rate limiting:** fixed/sliding window with `INCR` + `EXPIRE`, or a
  token-bucket Lua script for accuracy.

## Operations & safety

- Treat cache as **best-effort**: the app must remain correct when
  Redis/Valkey is unavailable (degrade to source of truth, not fail).
- Bound the connection pool; set command timeouts.
- Never store secrets or large blobs; never use it as the only copy of
  durable data.
- Credentials come from env vars (`policies/05-security-and-secrets.md`).
- Integration tests use a real instance via Testcontainers.

## Forbidden patterns

- Keys without a TTL where the data is ephemeral.
- Treating Redis/Valkey as the system of record.
- A distributed lock without a token check on release (deletes another
  holder's lock).
- Blocking commands (`KEYS *`, unbounded `SMEMBERS`) on hot paths in
  production.
- Cache logic that makes the app fail hard when the cache is down.
