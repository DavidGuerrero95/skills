# 05 — Diagrams and docs cadence

## Diagrams

- **Use Mermaid** for context, container, sequence, ownership and flow
  diagrams. Sources live under `docs/diagrams/` as `.mmd` files.
- Keep labels explicit. Show **service ownership** clearly: every box
  belongs to exactly one service.
- Diagrams sit close to the docs that reference them
  (`docs/wiki/architecture-overview.md`, runbooks under
  `docs/wiki/runbooks/`, ADRs under `docs/adr/`).
- Include directionality on edges (events, sync calls, schedulers).
- Prefer **multiple focused diagrams** over one mega-diagram.

## When to update / create a diagram

Update or add a diagram when one of these happens:

- a new service or driven adapter appears,
- an event path changes (new topic, new consumer, new fanout),
- ownership moves between services (e.g. a publisher changes),
- a new scheduler or reconciliation flow appears,
- a previously implicit workflow becomes operationally critical,
- a runbook needs to show a new failure mode.

## Documentation cadence

`policies/07-documentation-and-traceability.md` defines the surfaces
and what triggers an update. This file adds the **how** for diagrams
and the operator-facing voice.

- Start every doc from the **operator or maintainer perspective.** Not
  "the system does X"; "to do X, run Y".
- Include **exact commands** when operationally important.
- Use the repository's actual paths, ports, and script names.
- Keep summaries short; deep detail goes in linked sections.

## Diagram authoring conventions

- File extension: `.mmd`. One diagram per file.
- File name: `<area>-<view>-<n>.mmd`, e.g. `paper-trading-sequence-1.mmd`.
- Header comment in the `.mmd`: title, owner service(s), last
  meaningful change date.
- Whenever practical, the diagram is rendered into a PNG/SVG and
  committed alongside, but the `.mmd` is the source of truth.
- For sequence diagrams, use canonical actor names that match
  `policies/06-investment-domain-guardrails.md`
  (`market-data-service-ms`, `analysis-agent-service-ms`,
  `portfolio_service_ms`, `execution-service-ms`,
  `notification-service-ms`).

## When a diagram must be paired with a doc change

If you are adding/updating a diagram, also update:

- the section in `docs/wiki/architecture-overview.md` that references it,
- the runbook under `docs/wiki/runbooks/` if the operator workflow
  changed,
- the ADR under `docs/adr/` if the change is a decision worth
  preserving.

## Forbidden patterns

- Committing a diagram only as a binary image without `.mmd` source.
- Letting a diagram drift after the implementation changed.
- One mega-diagram that tries to show everything.
- Using ad-hoc service names that disagree with the canonical service
  list.
