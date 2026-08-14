---
name: mermaid-architecture-diagrams
description: Produce or update Mermaid architecture, sequence, context, ownership, and flow diagrams that match the repository's actual behavior, naming, and topology. Use when a new module appears, an event/request path changes, ownership moves, a runbook needs a flow diagram, or the architecture overview drifts from reality.
license: MIT
metadata:
  scope: mermaid-architecture
  version: "2.0"
---

# Mermaid architecture diagrams

## When to use

- A new module, service, or outbound adapter appears.
- An event/request path changes (new topic, new consumer, new fanout).
- Ownership moves between modules (e.g. who publishes an effect).
- A scheduler / reconciliation flow appears or changes cadence.
- A runbook needs a sequence or context diagram.
- The architecture overview has drifted from the implementation.

## When NOT to use

- A throwaway sketch. (Use a whiteboard.)
- Something describable in two sentences instead of a diagram.

## Read first

- `memory/rules/05-diagrams-and-docs.md`
- `memory/policies/07-documentation-and-traceability.md`
- The relevant module `README.md`(s) and `docs/contracts/` for canonical
  names.

## Workflow

1. **Pick the view.** Context / container / sequence / ownership / flow.
2. **Reuse canonical names.** Module names match the ownership map in
   `policies/06-domain-guardrails.md`; topic/endpoint names match
   `docs/contracts/`.
3. **Author the `.mmd` source** under `docs/diagrams/`. One diagram per
   file; name `<area>-<view>-<n>.mmd`; header comment with title, owner
   module(s), last meaningful change.
4. **Pair with documentation.** Update the referencing section in
   `docs/architecture/` or the relevant runbook / ADR.
5. **Render** to PNG/SVG when practical and commit alongside; the `.mmd`
   is the source of truth.

## Authoring conventions

- `flowchart LR`/`TB` for context/container; `sequenceDiagram` for
  interactions over time; sub-graphs for ownership.
- Label every edge with the event/topic/endpoint name and direction.
- Avoid abbreviations unless already canonical.

## Output expected from this skill

```
Diagram(s):
 - docs/diagrams/<file>.mmd  ← source

Doc surfaces updated:
 - docs/architecture/<file>.md (section: ...)
 - docs/runbooks/<runbook>.md
 - docs/adr/<adr>.md  (when applicable)

Validation:
 - Mermaid syntax compiled (e.g. mermaid-cli) — [ran|skipped, reason]
```

## Forbidden patterns

- Committing only a binary image without a `.mmd` source.
- Ad-hoc module names that disagree with the canonical ownership map.
- One mega-diagram that tries to show every flow.
- Inline diagrams in a chat message instead of a committed `.mmd`.
