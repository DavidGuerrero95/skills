# 07 — Documentation and traceability

## Purpose

Define when documentation must be updated together with the code, and
where each kind of documentation lives. This file is stack-agnostic.

The cadence and trigger lists for diagrams are in
`rules/05-diagrams-and-docs.md`. The technical-writer persona is in
`agents/technical-writer.md`.

## Documentation surfaces

| Surface                     | Location                                              | Purpose                                                        |
| --------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| Repository overview         | `README.md` (root)                                   | Quick start, architecture summary, stack, entry points         |
| Per-module overview         | `<module>/README.md`                                 | Module responsibility, run instructions, key contracts         |
| Architecture decisions      | `docs/adr/`                                          | One file per decision: status + context + decision + consequences |
| Operational runbooks        | `docs/runbooks/`                                     | Step-by-step instructions for operators                        |
| Architecture overview       | `docs/architecture/`                                 | Long-form architecture and infra view                          |
| Diagrams                    | `docs/diagrams/`                                     | Source-controlled `.mmd` (Mermaid) files + rendered output     |
| API / event contracts       | `docs/contracts/`                                    | OpenAPI, AsyncAPI, JSON Schema, topic/endpoint catalog         |
| Plans / progress            | `docs/plans/`                                         | Work-in-progress specs and status                              |
| Env templates               | `.env.example` (root)                                | Operator-visible env var reference                             |

Adjust paths to the repository's real layout, but keep one authoritative
location per surface.

## When to update documentation

Update docs in the same change set that touches:

- module/service boundaries or new modules,
- API endpoints, event topic names, schemas, headers, key strategy,
- environment variables (any addition, rename or removal),
- bootstrap, migration, or smoke scripts,
- idempotency keys or replay behavior,
- scheduler/ownership responsibilities,
- operator workflows,
- ports or local infra topology.

## Style rules

- Keep `README.md` short. Move deep operational detail into
  `docs/` or runbooks.
- Reference **exact file paths** when documenting operational behavior.
  Do not write "the scheduler" — write the path.
- Prefer **concrete commands** over prose. A reader should be able to
  copy-paste.
- Diagrams are **source-controlled and text-based** (Mermaid). Avoid
  binary-only diagrams.
- ADRs: one decision per file. Title format `NNNN-<slug>.md`. Status
  field: `Proposed | Accepted | Superseded`.
- Runbooks: title is the operator's task ("Reset local env and run
  E2E"), not the system area.

## Traceability

- Every change that affects a contract updates the contract catalog and
  the relevant schema in the same commit.
- Every ADR references the commit (or PR) that implemented it.
- The coverage threshold and validation path are documented in
  `04-testing-and-quality-gates.md`; do not duplicate them here.

## Forbidden patterns

- Documenting a feature that does not yet exist as if it were live.
- Letting `README.md` drift after a contract change.
- Embedding screenshots of diagrams instead of source-controlled
  Mermaid.
- Documenting credentials, even fake ones, in a way that resembles a
  real secret.
- Splitting one ADR across multiple files.
