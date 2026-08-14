# Agents operating guide

`/memory` is the canonical source of truth for agent behavior in this
repository. This file stays short on purpose; deep content lives in
`/memory`. It applies to Codex, GitHub Copilot, and any other agent that
reads `AGENTS.md`.

## Read path

Prefer these sources in order:

1. `/memory/README.md`
2. `/memory/MANIFEST.md`
3. `/memory/policies/*`
4. `/memory/rules/*`
5. The active stack profile under `/memory/stacks/*`
6. The active skill under `/memory/skills/*`
7. The active agent under `/memory/agents/*`

## Working agreements

- Inspect before editing.
- Prefer minimal diffs.
- Keep domain / core code framework-free.
- Respect hexagonal boundaries.
- Follow the active stack's conventions (`/memory/stacks/*`).
- Run targeted validation
  (`/memory/rules/02-validation-and-done-definition.md`).
- Update docs when contracts, flows, or operations change.
- Keep secrets out of source.
- Use repo skills and agents instead of repeating long prompts.
- Never duplicate canonical content into adapter folders.

## What this repository is

A **stack-agnostic, reusable agentic baseline**. It is not tied to any
product. Supported stacks and datastores each have a profile under
`/memory/stacks/` (Java/Spring, Python/FastAPI, Node/TypeScript,
PostgreSQL, MongoDB, Redis/Valkey, Kafka, REST, Docker). Fill in
`/memory/policies/06-domain-guardrails.md` and the idempotency matrix in
`/memory/rules/04-idempotency-and-event-contracts.md` for a concrete
project.

## Adapter note

This `AGENTS.md` is intentionally concise. Detailed instructions live in
`/memory`. Runtime adapters:

- Codex: `.codex/hooks.json`, `.codex/agents/*.toml`,
  `.codex/skills/*/SKILL.md`, `.codex/policies/*.md` (thin pointers).
- GitHub Copilot: `.github/copilot-instructions.md` and
  `.github/instructions/*.instructions.md` (thin pointers).
- Cursor: `.cursor/rules/*.mdc` (thin pointers).
- Tool-neutral skills: `.agents/skills/*/SKILL.md` (thin pointers).
