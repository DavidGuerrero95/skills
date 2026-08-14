# 06 — Domain guardrails (template)

## Why this exists

Every non-trivial system has a small set of **domain-critical
invariants** whose violation causes real damage: money movement, data
loss, privacy exposure, irreversible external actions. Generic
engineering rules do not capture them. This file is a **template**: each
repository fills it in with its own domain guardrails and keeps them
non-negotiable. The skill `skills/domain-safety-review/SKILL.md`
operationalizes whatever is written here.

> Replace the bracketed sections below with your project's real
> guardrails. Keep the structure. If your project has no critical domain
> (e.g. a static site), this file may state that explicitly and stay
> short.

## 1. Bounded contexts / ownership map

Document the single source of truth for who owns what. A change that
moves ownership across a boundary requires a domain review.

| Context / module / service | Owns (data + effects)                | Publishes / exposes            |
| -------------------------- | ------------------------------------ | ------------------------------ |
| `[context-a]`              | `[what it is authoritative for]`     | `[events / APIs it emits]`     |
| `[context-b]`              | `[…]`                                | `[…]`                          |

## 2. Critical invariants

List the rules that must never break. Examples of the *kind* of rule
(replace with yours):

- **Irreversible actions are gated.** `[payment capture / email send /
  external order]` requires `[explicit confirmation / feature flag /
  double-entry check]` and defaults to the safe mode.
- **Authoritative data has one home.** `[risk parameters / pricing /
  entitlements]` live in `[the datastore]`, never scattered into ad-hoc
  env vars or duplicated caches.
- **Audit vs. command separation.** Events that are audit-only never
  carry executable fields; the executable command is a distinct message.
- **Money / quantity math is exact.** Use decimal types, never binary
  floating point, for `[currency / units]`. Apply only validated deltas.
- **PII handling.** `[which fields are PII]`, where they may flow, and
  where they must be redacted.

## 3. Safe-by-default modes

- Which environment is the default (sandbox / paper / dry-run), and how
  a change proves it did not flip the default to a live/destructive mode.
- Kill-switch / circuit-breaker behavior, if any: what it flushes, what
  it cancels, and how failures are reconciled.

## 4. Idempotency expectations

At policy level (details and matrix in
`rules/04-idempotency-and-event-contracts.md`):

- Every evented or externally-effecting workflow declares its
  **canonical effect key**.
- Replays are either harmless no-ops or intentionally handled deltas.
- Distinct effects (envelope dedupe, external submission, projection,
  notification) use distinct keys.

## 5. Change discipline

Any change that touches a domain-critical path
(`[list them: order submission, billing, auth, data export, …]`) must
include:

- a domain review (`skills/domain-safety-review` or a human reviewer),
- updated contract/documentation for the affected surface,
- a smoke / E2E run that exercises the changed path.

## Forbidden patterns (fill in per project)

- `[Hardcoding a live/destructive endpoint instead of the safe default.]`
- `[Adding executable fields to an audit-only event.]`
- `[Moving authoritative parameters out of their datastore into env
  vars.]`
- `[Letting a non-owning module publish another module's effects.]`
- `[Bypassing cooldowns / locks / confirmations "for testing".]`
