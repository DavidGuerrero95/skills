# Idempotency and event-contract rule

## Principles

- Every evented workflow must define its own canonical effect key.
- Replays must be either harmless no-ops or intentionally handled deltas.
- Event envelopes, broker submission IDs, fill deltas, alerts, and dedupe windows are different responsibilities.

## Review checklist

- What is the canonical key at this layer?
- What effect is protected by that key?
- What happens on duplicate delivery?
- What happens on same key + different payload?
- What downstream projection or notification changes?

## Documentation

Document:
- topic names,
- producer/consumer ownership,
- key fields,
- replay behavior,
- and DLQ expectations.
