---
name: mermaid-architecture-diagrams
description: Produce or update Mermaid architecture, sequence, context, ownership and event-flow diagrams that match the repository's actual behavior, naming and ports. Use when a new service appears, an event path changes, ownership moves between services, a runbook needs a flow diagram, or the architecture overview drifts from reality.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: mermaid-architecture
  version: "1.1"
---

# Mermaid architecture diagrams

## When to use

- A new service or driven adapter appears.
- An event path changes (new topic, new consumer, new fanout).
- Ownership moves between services (e.g. who publishes a notification).
- A scheduler / reconciliation flow appears or changes cadence.
- A runbook needs a sequence or context diagram.
- The architecture overview has drifted from the implementation.

## When NOT to use

- A free-form sketch that the team will throw away. (Use a whiteboard.)
- A diagram that the agent can describe in two sentences instead of
  rendering.

## Read first

- `memory/rules/05-diagrams-and-docs.md`
- `memory/policies/07-documentation-and-traceability.md`
- The relevant service `README.md`(s) and `docs/contracts/topics.md`
  for canonical names.

## Workflow

1. **Pick the view.**
   - Context (system + external actors).
   - Container (services + infra).
   - Sequence (interaction over time).
   - Ownership (which service owns which event/topic).
   - Flow (workflow with conditional branches).

2. **Reuse canonical names.**
   - Service names match the matrix in
     `policies/06-investment-domain-guardrails.md`.
   - Topic names match `docs/contracts/topics.md`.
   - Recipient aliases match `telegram:business` / `telegram:news`.

3. **Author the `.mmd` source** under `docs/diagrams/`.
   - One diagram per file.
   - File name: `<area>-<view>-<n>.mmd`.
   - Header comment: title, owner service(s), last meaningful change.

4. **Pair with documentation.**
   - Update the section in
     `docs/wiki/architecture-overview.md` or the relevant runbook /
     ADR that references the diagram.

5. **Render** to PNG/SVG when practical and commit alongside.
   The `.mmd` is the source of truth.

## Authoring conventions

- Use `flowchart LR` or `flowchart TB` for context/container.
- Use `sequenceDiagram` for interactions over time.
- Use sub-graphs to express service ownership.
- Label every edge with the event/topic name and direction.
- Avoid abbreviations unless they are already canonical
  (e.g. `paper.order.executed.v1`).

## Output expected from this skill

```
Diagram(s):
 - docs/diagrams/<file>.mmd  ← source

Doc surfaces updated:
 - docs/wiki/architecture-overview.md (section: ...)
 - docs/wiki/runbooks/<runbook>.md
 - docs/adr/<adr>.md  (when applicable)

Validation:
 - Mermaid syntax compiled (e.g. via mermaid-cli) — [ran|skipped, reason]
```

## Forbidden patterns

- Committing only a binary image (`.png`, `.svg`) without a `.mmd`
  source.
- Using ad-hoc service names that disagree with the canonical service
  list.
- One mega-diagram that tries to show every flow.
- Inline diagrams in a chat message instead of a committed `.mmd`.
