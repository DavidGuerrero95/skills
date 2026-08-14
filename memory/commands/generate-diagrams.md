# /generate-diagrams

Create or update Mermaid diagrams that match the repository's real
behavior, names, and topology.

## Steps

1. Pick the narrowest view (context, container, sequence, ownership,
   flow).
2. Reuse canonical module and topic/endpoint names. See the ownership
   map in `policies/06-domain-guardrails.md` and `docs/contracts/`.
3. Author the `.mmd` source under `docs/diagrams/`. One diagram per
   file. File name `<area>-<view>-<n>.mmd`.
4. Pair with documentation: update the section in `docs/architecture/`,
   the relevant runbook, or an ADR.
5. Render to PNG/SVG when practical and commit alongside.

## Recommended delegates

- `mermaid-architect` (lead)
- `technical-writer` when the surrounding doc must be updated
