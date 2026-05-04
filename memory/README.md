# /memory — canonical source of truth

This directory is the **single, version-controlled source of truth** for how
agents (Claude Code, Codex, Cursor) operate in this repository. Every other
folder (`.claude/`, `.codex/`, `.cursor/`, `.agents/`) is a thin runtime
adapter that points back here.

## Why this layout exists

A typical mistake is to spread instructions across `CLAUDE.md`, `AGENTS.md`,
`.cursor/rules/`, ad hoc prompts and chat history. That produces drift,
contradictions and wasted tokens. `/memory` solves it by:

1. **One canonical file per responsibility.** No instruction is duplicated.
2. **Adapters do not own content.** They only forward to canonical files.
3. **Progressive disclosure.** Short index → policies → rules → skills →
   on-demand references. Heavy content stays out of always-loaded files.
4. **SRP per file.** Every file answers exactly one of: *what is forbidden*,
   *how do we work*, *how do we do task X*, *who acts as role Y*, *what
   triggers automation*, *what commands exist*, *how do we communicate*.

## Folder contract

| Folder           | Purpose                                                        | Must NOT contain                                |
| ---------------- | -------------------------------------------------------------- | ----------------------------------------------- |
| `policies/`      | Non-negotiable invariants and governance                       | Task workflows, tone, command triggers          |
| `rules/`         | How work is executed in this repo (flow, DoD, delegation)      | Long procedures, persona text                   |
| `skills/`        | Reusable, named workflows with progressive disclosure          | Global architecture policy, persona definition  |
| `agents/`        | Specialized personas / delegates                               | General repo rules, project policy text         |
| `hooks/`         | Lifecycle automation contracts (rationale + trigger + scope)   | Implementation code (lives in `scripts/`)       |
| `commands/`      | Explicit user-invoked entrypoints                              | Deep how-to (delegate to a skill)               |
| `output-styles/` | Communication style only                                       | Validation rules, domain policy                 |

## Precedence (when sources conflict)

1. Runtime/platform safety (the harness itself)
2. `memory/policies/*` — non-negotiable invariants
3. `memory/rules/*` — repo operating mode
4. Active `memory/skills/*` or `memory/agents/*` content for the task at hand
5. Active `memory/output-styles/*` for tone only
6. Ad hoc task prompt
7. Adapter folders (`.claude/`, `.codex/`, `.cursor/`, `.agents/`) — never
   override canonical content; they may only narrow it for a specific
   runtime quirk and must reference the canonical file.

## Read path before any non-trivial change

1. `memory/README.md` (this file)
2. `memory/MANIFEST.md`
3. The applicable file in `memory/policies/`
4. The applicable file in `memory/rules/`
5. The most relevant `memory/skills/*/SKILL.md` (only when activated)
6. The most relevant `memory/agents/*.md` (only if delegating)

## Idempotency guarantee

A file may exist in `/memory` only if it has a **distinct trigger** and a
**distinct responsibility**. If a new instruction mostly restates an
existing file, the existing file is updated instead of adding a second one.
See `MANIFEST.md` for the ownership matrix and anti-duplication rules.

## Stack assumed by this baseline

This baseline targets the INVEXA reactive microservice stack. Adapt the
specifics in your own repository, but keep the structure identical.

- Java 21
- Spring Boot 4.0.x (WebFlux + Reactor)
- Apache Kafka 4.2.x (SASL_PLAINTEXT / SCRAM-SHA-512)
- Jackson 3.1 (`tools.jackson.databind`)
- PostgreSQL 17.x, MongoDB 8.x, Valkey 9.x
- Gradle multi-module build, central versions in root `build.gradle`
- Hexagonal / clean architecture (`domain`, `usecase` / `application`,
  `infrastructure/entry-points/*`, `infrastructure/driven-adapters/*`,
  `applications/app-service`)
- Quality gates: Spotless + Sonar (Bugs/Vulnerabilities are blockers) +
  JaCoCo merged report ≥ 70 % line coverage
- WSL + Docker Compose for local infra and smoke scripts

## How to extend

When you need to capture new behavior:

1. Identify the canonical owner using `MANIFEST.md`.
2. If no owner exists, justify a new file (distinct trigger + responsibility).
3. Add the file with a clear single-purpose header.
4. Update `MANIFEST.md` so future contributors see it.
5. If a runtime adapter needs to expose it, add a thin reference file —
   never copy the body.
