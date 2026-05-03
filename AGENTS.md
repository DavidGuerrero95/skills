# Codex operating guide

Use `/memory` as the canonical source of truth for agent behavior in this repository.

## Instruction chain

Prefer these sources in order:
1. `/memory/policies/*`
2. `/memory/rules/*`
3. relevant skill under `/memory/skills/*`
4. relevant agent under `/memory/agents/*`

## Working agreements

- Inspect before editing.
- Prefer minimal diffs.
- Keep domain code framework-free.
- Respect hexagonal boundaries.
- Run targeted validation.
- Update docs when contracts, flows, or operations change.
- Keep secrets out of source.
- Use repo skills and agents instead of repeating large prompts.

## Project context

This repository follows the INVEXA baseline:
- five reactive microservice architecture
- Java 21 + Spring + Reactor + Kafka
- strong idempotency and event-contract discipline
- WSL + Docker Compose local workflow
- documentation, smoke scripts, and operator runbooks are part of the product surface

## Adapter note

This `AGENTS.md` is intentionally concise. Detailed instructions live in `/memory`.
