# /sync-documentation

Bring README, ADRs, runbooks, and contract documentation back into sync
with the codebase.

## Steps

1. Audit the implementation; write what it does, not what it "should
   do".
2. Identify the affected surfaces using
   `policies/07-documentation-and-traceability.md`.
3. Update the narrowest surface that closes the gap. Keep `README.md`
   short; push depth into linked sections.
4. Update `.env.example` if env vars changed.
5. Update `docs/contracts/` (OpenAPI / AsyncAPI / JSON Schema / catalog)
   if endpoints, topics, or schemas changed.
6. Pair runbook updates with smoke-script changes.
7. Validate by running the documented commands when feasible.

## Recommended delegates

- `technical-writer` (lead)
- `mermaid-architect` when flows or ownership changed
