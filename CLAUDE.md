# Claude operating guide

Use `/memory` as the canonical source of truth for this repository.

## Read path

Before major work, read:
- `/memory/README.md`
- `/memory/MANIFEST.md`
- relevant files in `/memory/policies/`
- relevant files in `/memory/rules/`

## Working agreements

- Keep domain code framework-free.
- Respect hexagonal boundaries.
- Prefer minimal diffs.
- Run the smallest meaningful validation.
- Update docs when behavior, contracts, or operations change.
- For repeated workflows, use project skills instead of copying long instructions into chat.

## Project context

This repository follows the INVEXA baseline:
- Java 21
- Spring Boot 4.0.x
- Reactor / WebFlux
- Kafka
- PostgreSQL, MongoDB, Valkey
- WSL + Docker Compose local runtime
- investment-domain safety and idempotency concerns

## Delegation

Use project agents in `.claude/agents/` for specialized work:
- implementation
- unit tests
- E2E
- smell audit
- architecture
- documentation
- debugging
- security
