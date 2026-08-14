# 04 — Idempotency and event contracts

## Principles

- **Every evented or externally-effecting workflow declares its
  canonical effect key.**
- **Replays are either harmless no-ops or intentionally handled deltas.**
- **Distinct effects use distinct keys.** Do not collapse envelope
  dedupe, external submission, projection, and notification into one key.

## Generic idempotency patterns

Pick the pattern that matches each layer; do not reuse one key across
layers.

| Layer / effect                 | Typical canonical key                              | Required behavior                                                                                       |
| ------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Inbound HTTP write             | client-supplied `Idempotency-Key` header           | Same key ⇒ return the stored response; never apply the effect twice.                                   |
| Message envelope (consumer)    | `eventId` / `messageId` (inbox / dedupe table)     | Same id ⇒ effects applied once. Same id + different payload ⇒ contract violation (dead-letter + alert). |
| External command submission    | domain command id (e.g. `orderId`, `paymentId`)    | At most one external submission per id. Recovery looks up local + remote state before resubmitting.    |
| Projection / running total     | domain id + monotonic counter (e.g. `+ version`)   | Apply the **positive delta** vs. last seen. Same counter ⇒ duplicate. Lower ⇒ stale (dead-letter).      |
| Time-windowed effect           | domain id + truncated window (e.g. `epoch/3600`)   | One effect per entity per window. Store the window key in the cache/DB.                                 |
| Deduplicated content           | content hash (SHA-256 of the identifying fields)   | Same hash ⇒ not reprocessed until TTL expires.                                                          |

> Fill this into a **project-specific matrix** below, replacing the
> generic rows with your real topics/endpoints, keys, and effects.

## Project idempotency matrix (fill in)

| Layer                | Canonical key            | Topic / endpoint / effect     | Required behavior         |
| -------------------- | ------------------------ | ----------------------------- | ------------------------- |
| `[layer]`            | `[key fields]`           | `[topic / endpoint]`          | `[replay behavior]`       |

## Review checklist before merging an event-touching change

- What is the **canonical key** at this layer?
- What **effect** is protected by that key?
- What happens on **duplicate delivery**?
- What happens on **same key + different payload**?
- What **downstream projection or notification** changes?
- Is **dead-letter behavior** documented with a human-readable reason
  header?
- Is the **schema change additive and backward-compatible**? If not, is
  there a versioned topic/endpoint?
- Are the machine-readable schemas (OpenAPI / AsyncAPI / JSON Schema)
  under `docs/contracts/` updated?

## Documentation requirements

Document, in the same change set:

- topic/endpoint name(s) and version(s),
- producer and consumer ownership,
- key fields,
- replay behavior,
- dead-letter topic name and routing reason,
- env vars introduced or renamed.

Authoritative location: `docs/contracts/`.

## Forbidden patterns

- Reusing the envelope id as the external submission key.
- Treating a downstream-generated id as sufficient for projection.
- Skipping cooldown / TTL logic in tests "to make them pass".
- Adding a new evented effect without declaring its key in the matrix.
- Renaming a contract field without a versioned topic/endpoint and a
  documented migration.
