---
name: domain-safety-review
description: Review a change against the project's domain guardrails — ownership boundaries, critical invariants, safe-by-default modes, per-layer idempotency, and irreversible-action gating. Use whenever a change touches a domain-critical path (money, auth, data export, external side effects, ownership of an event/effect).
license: MIT
metadata:
  scope: domain-safety
  version: "2.0"
---

# Domain-safety review

## When to use

- A change touches a domain-critical path listed in
  `policies/06-domain-guardrails.md` (money movement, auth, data export,
  irreversible external actions, ownership of an event/effect).
- Ownership of data or an effect may be moving across a boundary.
- Idempotency keys, safe-default modes, or kill-switch behavior are
  involved.

## When NOT to use

- Pure infrastructure or dev-tooling changes with no domain effect.
- Changes that do not touch any domain-critical path.

## Read first

- `memory/policies/06-domain-guardrails.md` (the project's filled-in
  guardrails — the source of truth for this review)
- `memory/rules/04-idempotency-and-event-contracts.md`
- `memory/policies/03-async-and-messaging.md`

## Review checklist

Walk this checklist against the diff, in order. Anchor each finding to
the specific guardrail in `policies/06-domain-guardrails.md`.

1. **Ownership boundary preserved?**
   - No module publishes another module's effects.
   - The ownership map still holds after the change.

2. **Critical invariants intact?**
   - Irreversible actions stay gated and default to the safe mode.
   - Authoritative data stays in its single home (not scattered into env
     vars or duplicate caches).
   - Audit-only events carry no executable fields.
   - Money / exact-quantity math uses decimal types and applies only
     validated deltas.

3. **Safe-by-default mode preserved?**
   - The default environment (sandbox / dry-run) is not silently flipped
     to live/destructive.

4. **Idempotency keys match the matrix?**
   - Each layer declares its own canonical key
     (`rules/04-idempotency-and-event-contracts.md`).

5. **PII handling correct?**
   - PII flows only where allowed; redacted where required; never logged.

6. **Documentation updated?**
   - Contract catalog and affected module README reflect the change.

## Output expected from this skill

```
Guardrail(s) reviewed:
 - <guardrail from policies/06-domain-guardrails.md>

Safety assumptions:
 - <bullet>

Risks of regression:
 - <bullet>

Downstream consumers affected:
 - <module> consumes <topic/endpoint>

Remediation required:
 - <bullet> (if any)
```

## Forbidden patterns

- Approving a change that flips a safe-default to a live/destructive mode.
- Adding executable fields to an audit-only event.
- Moving authoritative parameters out of their datastore into env vars.
- Letting a non-owning module publish another module's effects.
- Bypassing cooldowns / locks / confirmations "for testing".
- Treating the envelope id as a substitute for layer-specific keys.
