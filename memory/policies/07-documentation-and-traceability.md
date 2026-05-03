# Documentation and traceability policy

## Rules

- Update docs when architecture, contracts, operational scripts, or workflows change materially.
- Keep diagrams source-controlled and text-based where possible.
- Prefer Mermaid for lightweight architecture and sequence diagrams unless the repository already standardizes another format.
- Reference exact file paths when documenting operational behavior.
- Keep README short; move deep operational detail into docs or runbooks.
- Keep ADRs for decisions with lasting architectural impact.

## Trigger examples

Update documentation when a change affects:
- service boundaries,
- topic names or contracts,
- environment variables,
- smoke commands,
- idempotency keys,
- bootstrap scripts,
- scheduler ownership,
- or operator workflows.
