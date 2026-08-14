# 05 — Diagrams and docs cadence

## Diagrams

- **Use Mermaid** for context, container, sequence, ownership and flow
  diagrams. Sources live under `docs/diagrams/` as `.mmd` files.
- Keep labels explicit. Show **ownership** clearly: every box belongs to
  exactly one module/service.
- Diagrams sit close to the docs that reference them
  (`docs/architecture/`, runbooks under `docs/runbooks/`, ADRs under
  `docs/adr/`).
- Include directionality on edges (events, sync calls, schedulers).
- Prefer **multiple focused diagrams** over one mega-diagram.

## When to update / create a diagram

Update or add a diagram when one of these happens:

- a new module, service, or outbound adapter appears,
- an event/request path changes (new topic, new consumer, new fanout),
- ownership moves between modules (e.g. a publisher changes),
- a new scheduler or reconciliation flow appears,
- a previously implicit workflow becomes operationally critical,
- a runbook needs to show a new failure mode.

## Documentation cadence

`policies/07-documentation-and-traceability.md` defines the surfaces and
what triggers an update. This file adds the **how** for diagrams and the
operator-facing voice.

- Start every doc from the **operator or maintainer perspective.** Not
  "the system does X"; "to do X, run Y".
- Include **exact commands** when operationally important.
- Use the repository's actual paths, ports, and script names.
- Keep summaries short; deep detail goes in linked sections.

## Diagram authoring conventions

- File extension: `.mmd`. One diagram per file.
- File name: `<area>-<view>-<n>.mmd`, e.g. `checkout-sequence-1.mmd`.
- Header comment in the `.mmd`: title, owner module(s), last meaningful
  change date.
- Whenever practical, render into a PNG/SVG and commit alongside, but the
  `.mmd` is the source of truth.
- Use canonical module/service names that match the ownership map in
  `policies/06-domain-guardrails.md`.

## When a diagram must be paired with a doc change

If you are adding/updating a diagram, also update:

- the section in `docs/architecture/` that references it,
- the runbook under `docs/runbooks/` if the operator workflow changed,
- the ADR under `docs/adr/` if the change is a decision worth preserving.

## Forbidden patterns

- Committing a diagram only as a binary image without `.mmd` source.
- Letting a diagram drift after the implementation changed.
- One mega-diagram that tries to show everything.
- Using ad-hoc module names that disagree with the canonical ownership
  map.
