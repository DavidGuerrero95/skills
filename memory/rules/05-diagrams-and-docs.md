# Diagrams and docs rule

## Mermaid expectations

- Prefer Mermaid for context, container, sequence, ownership, and flow diagrams.
- Keep labels explicit.
- Show service ownership clearly.
- Keep diagrams close to the docs they support.

## Update triggers

Update or add diagrams when:
- a new service or adapter appears,
- an event path changes,
- ownership moves between services,
- new scheduler or reconciliation flow appears,
- or a previously implicit workflow becomes critical.

## Documentation style

- Start from the operator or maintainer perspective.
- Include exact commands when operationally important.
- Prefer examples that match the repository’s actual scripts and ports.
