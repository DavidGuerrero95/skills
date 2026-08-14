---
name: technical-doc-writer
description: Write or update technical documentation, ADRs, runbooks, README sections, and operator-facing guidance. Use whenever behavior, contracts, env vars, scripts, or operational workflows change, or when documentation has drifted from the implementation.
license: MIT
metadata:
  scope: technical-writing
  version: "2.0"
---

# Technical doc writer

## When to use

- README updates after a behavior or contract change.
- ADRs for decisions with lasting architectural impact.
- Runbooks for operator workflows (start, stop, reset, recover).
- Setup docs (local infra, smoke scripts, env vars).
- Contract documentation (`docs/contracts/`: OpenAPI, AsyncAPI, JSON
  Schema, catalog).

## When NOT to use

- Diagrams — `skills/mermaid-architecture-diagrams`.
- Inline doc-comments on internal units (write self-explanatory code
  instead).

## Read first

- `memory/policies/07-documentation-and-traceability.md`
- `memory/rules/05-diagrams-and-docs.md`

## Workflow

1. **Identify the surface.**
   - Repository overview → root `README.md`.
   - Per-module overview → `<module>/README.md`.
   - Decision → `docs/adr/<NNNN>-<slug>.md`.
   - Operator workflow → `docs/runbooks/<workflow>.md`.
   - Architecture overview → `docs/architecture/`.
   - Contracts → `docs/contracts/`.

2. **Audit the implementation.** Read the actual scripts, ports, env
   vars, paths. Write what it does, not what it "should" do.

3. **Write from the operator/maintainer perspective.** Second person
   where natural; lead with the outcome, then the steps; exact commands
   and exact paths.

4. **Keep summaries short.** Push deep detail into linked sections; the
   root README is a quick start, not a reference manual.

5. **Update neighbors when needed.** A new env var → `.env.example` +
   module README + contract doc. A new script → README list + runbook.
   A new endpoint/topic → `docs/contracts/`.

6. **Validate** by running the documented commands when feasible.

## Output expected from this skill

```
Docs updated:
 - <path>: <what changed>

Behavioral changes documented:
 - <bullet>

Follow-ups still missing:
 - <bullet> (when applicable)

Validation:
 - [ran]  <the command the doc claims works>
```

## ADR conventions

- File name: `NNNN-<slug>.md`.
- Sections: `Status`, `Context`, `Decision`, `Consequences`.
- Status values: `Proposed`, `Accepted`, `Superseded by ADR-NNNN`.
- One decision per file; cross-reference related ADRs.

## Runbook conventions

- Title is the operator's task, not the system area.
- Each step is numbered and copy-paste runnable.
- Each step ends with the **expected observable outcome**.
- A failure section lists known errors and their remediation.

## Forbidden patterns

- Documenting features that do not yet exist.
- Letting the README drift after a contract change.
- Embedding screenshots of diagrams instead of source-controlled
  Mermaid.
- Documenting credentials in a way that resembles a real secret.
- Splitting one ADR across multiple files.
