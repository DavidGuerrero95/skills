# /generate-diagrams

Create or update Mermaid diagrams that match the repository's real
behavior, names, and ports.

## Steps

1. Pick the narrowest view (context, container, sequence, ownership,
   flow).
2. Reuse canonical service and topic names. See
   `policies/06-investment-domain-guardrails.md` for service names and
   `docs/contracts/topics.md` for topic names.
3. Author the `.mmd` source under `docs/diagrams/`. One diagram per
   file. File name `<area>-<view>-<n>.mmd`.
4. Pair with documentation: update the section in
   `docs/wiki/architecture-overview.md`, the relevant runbook, or an
   ADR.
5. Render to PNG/SVG when practical and commit alongside.

## Recommended delegates

- `mermaid-architect` (lead)
- `technical-writer` when the surrounding doc must be updated
