# Codex operating guide

`/memory` is the canonical source of truth for agent behavior in this
repository. This file stays short on purpose; deep content lives in
`/memory`.

## Read path

Prefer these sources in order:

1. `/memory/README.md`
2. `/memory/MANIFEST.md`
3. `/memory/policies/*`
4. `/memory/rules/*`
5. The active skill under `/memory/skills/*`
6. The active agent under `/memory/agents/*`

## Working agreements

- Inspect before editing.
- Prefer minimal diffs.
- Keep domain code framework-free.
- Respect hexagonal boundaries.
- Run targeted validation
  (`/memory/rules/02-validation-and-done-definition.md`).
- Update docs when contracts, flows, or operations change.
- Keep secrets out of source.
- Use repo skills and agents instead of repeating long prompts.
- Never duplicate canonical content into adapter folders.

## Project context

INVEXA reactive microservice baseline:

- Five Java 21 reactive microservices (`market-data`,
  `analysis-agent`, `portfolio` / `risk`, `execution`,
  `notification`).
- Spring Boot 4.0.x + Reactor + Kafka 4.2.x + Jackson 3.1.
- PostgreSQL 17.x + MongoDB 8.x + Valkey 9.x.
- Strong idempotency and event-contract discipline
  (`/memory/rules/04-idempotency-and-event-contracts.md`).
- WSL + Docker Compose local workflow.
- Documentation, smoke scripts, and operator runbooks are part of the
  product surface.

## Adapter note

This `AGENTS.md` is intentionally concise. Detailed instructions live
in `/memory`. Codex adapters live under `.codex/`:

- Hooks: `.codex/hooks.json` (delegating to `scripts/agentic/`).
- Agents: `.codex/agents/*.toml` (thin pointers).
- Skills: `.codex/skills/*/SKILL.md` (thin pointers).
- Policies: `.codex/policies/*.md` (thin pointers).
