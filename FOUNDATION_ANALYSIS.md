# Foundation analysis

## Goal

Provide a single, idempotent baseline of agent guidance (skills,
agents, hooks, commands, policies, rules, output styles) usable by
**Claude Code**, **Codex**, and **Cursor** for the INVEXA family of
Java 21 + Spring Boot 4.0.x reactive microservices.

## Architectural shape

- **`/memory/`** is the canonical, version-controlled source of truth.
- **`.claude/`, `.codex/`, `.cursor/`, `.agents/`** are thin runtime
  adapters. They reference `/memory` and never duplicate content.
- Adapter wrappers are validated against `/memory/MANIFEST.md`, which
  is the ownership matrix and anti-duplication contract.
- Hook contracts live in `/memory/hooks/`; their implementations live
  in `scripts/agentic/`.

## What this baseline guarantees

- **Single responsibility per file.** Every memory file owns exactly
  one trigger and one responsibility.
- **Idempotency.** New responsibilities update the canonical owner
  rather than creating a parallel file.
- **Progressive disclosure.** Short index → policies → rules → active
  skill / agent → on-demand references.
- **Multi-runtime parity.** Claude Code, Codex, and Cursor see the
  same content via thin wrappers.
- **Operational hygiene.** Hooks emit reminders for safety, docs,
  smell, and orphan-process visibility.

## Differences from the prior layout

- The prior `.codex/`-centric layout mixed long-lived policy with
  runtime-discovery artifacts and knowledge-base content. The new
  layout separates: invariants (`policies/`), execution flow
  (`rules/`), workflows (`skills/`), personas (`agents/`),
  automation contracts (`hooks/`), entrypoints (`commands/`), and
  tone (`output-styles/`).
- Adapters were rewritten as thin pointers. They no longer own
  policy.

## How to extend safely

1. Identify the canonical owner using `/memory/MANIFEST.md`.
2. If no owner exists, justify a new file (distinct trigger +
   responsibility).
3. Update only the canonical file.
4. Ensure adapters still point at the canonical file; do not paste
   content into adapter folders.
5. If a new hook is needed, add the contract under
   `/memory/hooks/<name>.md` and the implementation under
   `scripts/agentic/<name>.py`. Wire it in `.claude/settings.json`
   and `.codex/hooks.json`.

## Reuse for new repositories

This scaffold is designed to be copied into a new repository as the
agentic baseline. After copying:

- Adjust the project context blocks in `CLAUDE.md`, `AGENTS.md`, and
  `memory/policies/06-*` to the new domain.
- Keep the rest as-is: it encodes the engineering invariants for any
  Java 21 + Spring Boot 4.0.x reactive microservice baseline.
