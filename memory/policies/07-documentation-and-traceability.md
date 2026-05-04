# 07 — Documentation and traceability

## Purpose

Define when documentation must be updated together with the code, and
where each kind of documentation lives.

The cadence and trigger lists for diagrams are in
`rules/05-diagrams-and-docs.md`. The technical-doc-writer persona is in
`agents/technical-writer.md`.

## Documentation surfaces

| Surface                              | Location                                                                | Purpose                                                          |
| ------------------------------------ | ----------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Repository overview                  | `README.md` (root)                                                      | Quick start, architecture summary, stack, ports                  |
| Per-service overview                 | `<service>-ms/README.md`                                                | Service responsibility, run instructions, key contracts          |
| Architecture decisions               | `docs/adr/`                                                             | One file per decision, status + context + decision + consequences |
| Operational runbooks                 | `docs/wiki/runbooks/`                                                   | Step-by-step instructions for operators                          |
| Architecture overview                | `docs/wiki/architecture-overview.md`, `docs/wiki/infrastructure.md`    | Long-form architecture and infra view                            |
| Mermaid diagrams                     | `docs/diagrams/`                                                        | Source-controlled `.mmd` files + rendered output                 |
| Kafka topic catalog                  | `docs/contracts/topics.md`                                              | Authoritative topic list, version, ownership, key strategy       |
| Event schemas                        | `docs/contracts/json-schema/`, `docs/contracts/asyncapi/`               | Machine-readable schemas + AsyncAPI spec                         |
| Plans / progress                     | `docs/plans/<workstream>/`                                              | Work-in-progress specs and status                                |
| `.env` templates                     | `.env.example` (root) and `infrastructure/.env.example`                | Operator-visible env var reference                                |

## When to update documentation

Update docs in the same change set that touches:

- service boundaries or new services,
- topic names, schemas, headers, key strategy,
- environment variables (any addition, rename or removal),
- bootstrap or smoke scripts,
- idempotency keys or replay behavior,
- scheduler ownership (who runs the digest, who reconciles),
- operator workflows (kill switch, rollback, paper E2E),
- ports or local infra topology.

## Style rules

- Keep `README.md` short. Move deep operational detail into
  `docs/wiki/` or runbooks.
- Reference **exact file paths** when documenting operational
  behavior. Do not write "the scheduler" — write the path.
- Prefer **concrete commands** over prose. A reader should be able to
  copy-paste.
- Diagrams are **source-controlled and text-based** (Mermaid). Avoid
  binary-only diagrams.
- ADRs: one decision per file. Title format
  `XXXX-<slug>.md`. Status field: `Proposed | Accepted | Superseded`.
- Runbooks: title is the operator's task ("Reset local MVP and run
  paper E2E"), not the system area.

## Traceability

- Every change that affects a contract must update the topic catalog
  and the relevant schema in the same commit.
- Every ADR references the commit (or PR) that implemented it.
- The merged-report JaCoCo verification path is documented in
  `04-testing-and-quality-gates.md`; do not duplicate the threshold
  here.
- The smoke scripts that protect a workstream are listed in the README;
  when a new workstream lands, the smoke script and its expected pass
  count are added there.

## Forbidden patterns

- Documenting a feature that does not yet exist as if it were live.
- Letting `README.md` drift after a contract change.
- Embedding screenshots of diagrams instead of source-controlled
  Mermaid.
- Documenting credentials, even fake ones, in a way that resembles a
  real secret.
- Splitting one ADR across multiple files.
