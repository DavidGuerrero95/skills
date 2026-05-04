---
name: technical-doc-writer
description: Write or update technical documentation, ADRs, runbooks, README sections and operator-facing guidance for this repository. Use whenever behavior, contracts, env vars, scripts or operational workflows change, or when documentation has drifted from the implementation.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: technical-writing
  version: "1.1"
---

# Technical doc writer

## When to use

- README updates after a behavior or contract change.
- ADRs for decisions with lasting architectural impact.
- Runbooks for operator workflows (start, stop, reset, recover).
- Operator guides (paper E2E, kill switch, dashboard alerts).
- Setup docs (local infra, smoke scripts, env vars).
- Contract documentation (`docs/contracts/topics.md`,
  AsyncAPI, JSON schemas).

## When NOT to use

- Diagrams — use `skills/mermaid-architecture-diagrams`.
- Inline javadoc on internal classes (write code that doesn't need it
  instead).

## Read first

- `memory/policies/07-documentation-and-traceability.md`
- `memory/rules/05-diagrams-and-docs.md`

## Workflow

1. **Identify the surface.**
   - Repository overview → root `README.md`.
   - Per-service overview → `<service>-ms/README.md`.
   - Decision → `docs/adr/<NNNN>-<slug>.md`.
   - Operator workflow → `docs/wiki/runbooks/<workflow>.md`.
   - Architecture overview → `docs/wiki/architecture-overview.md`.
   - Contracts → `docs/contracts/topics.md` + AsyncAPI / JSON schema.

2. **Audit the implementation.**
   - Read the actual scripts, ports, env vars, paths.
   - Do not write what "the system should do"; write what it does.

3. **Write from the operator/maintainer perspective.**
   - Use second person where natural.
   - Lead with the outcome, then the steps.
   - Use exact commands and exact file paths.

4. **Keep summaries short.**
   - Push deep detail into linked sections.
   - The `README.md` is a quick start, not a reference manual.

5. **Update neighbors when needed.**
   - A new env var → update `.env.example` + service README +
     contract doc.
   - A new script → update the README script list + relevant runbook.
   - A new topic → update `docs/contracts/topics.md` + AsyncAPI / JSON
     schema.

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
 - [ran]  bash infrastructure/scripts/smoke-...sh   (where the doc claims it works)
```

## ADR conventions

- File name: `NNNN-<slug>.md`.
- Sections: `Status`, `Context`, `Decision`, `Consequences`.
- Status values: `Proposed`, `Accepted`, `Superseded by ADR-NNNN`.
- One decision per file. Cross-reference related ADRs.

## Runbook conventions

- Title is the operator's task, not the system area.
- Each step is numbered and copy-paste runnable.
- Each step ends with the **expected observable outcome**.
- Failure section lists known errors and their remediation.

## Forbidden patterns

- Documenting features that do not yet exist.
- Letting the README drift after a contract change.
- Embedding screenshots of diagrams instead of source-controlled
  Mermaid.
- Documenting credentials in a way that resembles a real secret.
- Splitting one ADR across multiple files.
