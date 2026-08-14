# Foundation analysis

## Goal

Provide a single, idempotent, **stack-agnostic** baseline of agent
guidance (skills, agents, hooks, commands, policies, rules, stack
profiles, output styles) usable by **Claude Code**, **Codex**,
**Cursor**, and **GitHub Copilot** across any project and language.

## Architectural shape

- **`/memory/`** is the canonical, version-controlled source of truth.
- **`.claude/`, `.codex/`, `.cursor/`, `.agents/`, `.github/`** (Copilot
  instructions) are thin runtime adapters. They reference `/memory` and
  never duplicate content.
- Adapter wrappers are validated against `/memory/MANIFEST.md`, the
  ownership matrix and anti-duplication contract.
- Hook contracts live in `/memory/hooks/`; their implementations live in
  `scripts/agentic/`.

## Layer separation

- **Invariants** (stack-agnostic): `policies/`.
- **Execution flow**: `rules/`.
- **Language / framework / datastore specifics**: `stacks/`.
- **Reusable workflows**: `skills/`. **Personas**: `agents/`.
- **Automation contracts**: `hooks/`. **Entrypoints**: `commands/`.
- **Tone**: `output-styles/`.

Policies never hardcode a single stack's syntax; they link to the
relevant `stacks/` profile.

## What this baseline guarantees

- **Single responsibility per file.**
- **Idempotency.** New responsibilities update the canonical owner.
- **Progressive disclosure.** Short index → policies → rules → stacks →
  active skill / agent → on-demand references.
- **Multi-runtime parity.** Claude Code, Codex, Cursor, Copilot see the
  same content via thin wrappers.
- **Operational hygiene.** Hooks emit reminders for safety, docs, smell,
  and orphan-process visibility.

## How to extend safely

1. Identify the canonical owner using `/memory/MANIFEST.md`.
2. If no owner exists, justify a new file (distinct trigger +
   responsibility).
3. Update only the canonical file.
4. Ensure adapters still point at the canonical file; do not paste
   content into adapter folders.
5. For a new hook, add the contract under `/memory/hooks/<name>.md` and
   the implementation under `scripts/agentic/<name>.py`. Wire it in
   `.claude/settings.json` and `.codex/hooks.json`.

## Reuse for new repositories

This scaffold is designed to be copied into a new repository as the
agentic baseline. After copying, adapt only the project-specific
placeholders:

- `memory/policies/06-domain-guardrails.md` (ownership + invariants),
- the idempotency matrix in
  `memory/rules/04-idempotency-and-event-contracts.md`,
- the active `memory/stacks/*` profiles,
- coverage threshold and validation commands.

The rest encodes engineering invariants that hold for any well-structured
codebase.
