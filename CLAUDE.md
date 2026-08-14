# Claude operating guide

`/memory` is the canonical source of truth for this repository. This file
stays short on purpose; deep content lives in `/memory`.

## Read path before non-trivial work

1. `/memory/README.md`
2. `/memory/MANIFEST.md`
3. The applicable file in `/memory/policies/`
4. The applicable file in `/memory/rules/`
5. The active stack profile in `/memory/stacks/`
6. The active skill (`/memory/skills/<skill>/SKILL.md`)
7. The active agent (`/memory/agents/<agent>.md`) when delegating

## Working agreements

- Keep domain / core code framework-free.
- Respect hexagonal boundaries (`/memory/policies/02-clean-architecture.md`).
- Prefer minimal diffs.
- Follow the active stack's conventions (`/memory/stacks/*`).
- Run the smallest meaningful validation
  (`/memory/rules/02-validation-and-done-definition.md`).
- Update docs when behavior, contracts, or operations change.
- For repeated workflows, use project skills instead of pasting long
  instructions into chat.
- Never duplicate `/memory` content into adapter folders. They are thin
  pointers.

## What this repository is

A **stack-agnostic, reusable agentic baseline** — skills, agents, hooks,
commands, policies, rules, stack profiles, and output styles — usable
across projects and languages (Java/Spring, Python/FastAPI,
Node/TypeScript, …) and datastores (PostgreSQL, MongoDB, Redis/Valkey,
Kafka). Nothing here is tied to a specific product.

To adapt it to a concrete project, fill in
`/memory/policies/06-domain-guardrails.md`, the idempotency matrix in
`/memory/rules/04-idempotency-and-event-contracts.md`, and activate the
relevant `/memory/stacks/*` profiles.

## Delegation

Specialized agents are listed in `/memory/agents/` and exposed via
`.claude/agents/`. Use the delegation matrix in
`/memory/rules/03-subagent-delegation.md`.

For recurring multi-agent work, run a **pipeline** from
`/memory/pipelines/` — an ordered chain of agents with an artifact and a
gate between each stage (feature delivery, bug fix, refactor, database
change, contract change, review gate). See `/memory/pipelines/README.md`.

## Hooks

The session is wired with hygiene hooks. Their **contracts** live in
`/memory/hooks/`, and their **implementations** live in
`scripts/agentic/`. Configuration:

- `.claude/settings.json` for Claude Code (paths use
  `$CLAUDE_PROJECT_DIR` so they resolve from the project root).
- `.codex/hooks.json` for Codex.

Active hooks: `prompt-memory-reminder` (SessionStart),
`pre-bash-safety-guard` (PreToolUse Bash),
`pre-write-secret-scan` (PreToolUse Edit/Write),
`post-edit-code-quality` (PostToolUse Edit/Write),
`post-task-docs-sync` (Stop),
`session-end-orphan-check` (Stop / SessionEnd / SubagentStop).
