# Claude operating guide

`/memory` is the canonical source of truth for this repository. This
file stays short on purpose; deep content lives in `/memory`.

## Read path before non-trivial work

1. `/memory/README.md`
2. `/memory/MANIFEST.md`
3. The applicable file in `/memory/policies/`
4. The applicable file in `/memory/rules/`
5. The active skill (`/memory/skills/<skill>/SKILL.md`)
6. The active agent (`/memory/agents/<agent>.md`) when delegating

## Working agreements

- Keep domain code framework-free.
- Respect hexagonal boundaries.
- Prefer minimal diffs.
- Run the smallest meaningful validation
  (`/memory/rules/02-validation-and-done-definition.md`).
- Update docs when behavior, contracts, or operations change.
- For repeated workflows, use project skills instead of pasting long
  instructions into chat.
- Never duplicate `/memory` content into adapter folders. They are
  thin pointers.

## Project context

INVEXA reactive microservice baseline:

- Java 21
- Spring Boot 4.0.x (WebFlux + Reactor)
- Apache Kafka 4.2.x (SASL_PLAINTEXT / SCRAM-SHA-512)
- Jackson 3.1
- PostgreSQL 17.x, MongoDB 8.x, Valkey 9.x
- Hexagonal / clean architecture (`domain`, `usecase`,
  `infrastructure/entry-points/*`, `infrastructure/driven-adapters/*`,
  `applications/app-service/`)
- Quality gates: Spotless + Sonar (Bugs/Vulnerabilities blockers) +
  JaCoCo merged report ≥ 70 % line coverage
- WSL + Docker Compose for local infra and smoke scripts
- Investment-domain safety + per-layer idempotency
  (`/memory/policies/06-investment-domain-guardrails.md`,
  `/memory/rules/04-idempotency-and-event-contracts.md`)

## Delegation

Specialized agents are listed in `/memory/agents/` and exposed via
`.claude/agents/`. Use the delegation matrix in
`/memory/rules/03-subagent-delegation.md`.

## Hooks

The session is wired with hygiene hooks. Their **contracts** live in
`/memory/hooks/`, and their **implementations** live in
`scripts/agentic/`. Configuration:

- `.claude/settings.json` for Claude Code
- `.codex/hooks.json` for Codex

Active hooks:

- `prompt-memory-reminder` (SessionStart)
- `pre-bash-safety-guard` (PreToolUse Bash)
- `pre-write-secret-scan` (PreToolUse Edit/Write)
- `post-edit-code-quality` (PostToolUse Edit/Write)
- `post-task-docs-sync` (Stop)
- `session-end-orphan-check` (Stop / SessionEnd / SubagentStop)
