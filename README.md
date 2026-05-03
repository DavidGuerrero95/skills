# INVEXA Agentic Memory Foundation

This package adds a reusable, source-of-truth agent foundation for **Claude Code**, **Codex**, and optionally **Cursor**.

## Design goals

- Make `/memory` the canonical source of truth.
- Keep concerns separated by single responsibility.
- Avoid repeated instructions across skills, agents, commands, hooks, and policies.
- Preserve compatibility with current INVEXA conventions: Java 21, Spring Boot, Reactor, Kafka, hexagonal architecture, Sonar quality gates, WSL + Docker Compose, and investment-domain guardrails.
- Allow thin runtime adapters for Claude, Codex, and Cursor instead of duplicating all logic in multiple tool-specific folders.

## Ownership model

| Folder | Owns | Must not own |
|---|---|---|
| `memory/policies` | Non-negotiable constraints and governance | Task workflows, tone, command triggers |
| `memory/rules` | Project operating rules and execution flow | Long procedural skills |
| `memory/skills` | Reusable task workflows | Global architecture policy |
| `memory/agents` | Specialized personas / delegates | General repo rules |
| `memory/hooks` | Lifecycle automation contracts | Human-facing commands |
| `memory/commands` | User-invoked entrypoints | Deep implementation detail |
| `memory/output-styles` | Response formatting and brevity | Validation rules |
| `.claude/`, `.codex/`, `.agents/`, `.cursor/` | Runtime adapters only | Canonical source content |

## Runtime mapping

### Claude Code
- Root guidance: `CLAUDE.md`
- Skills: `.claude/skills/`
- Agents: `.claude/agents/`
- Hooks: `.claude/settings.json`
- Commands: `.claude/commands/`
- Output styles: `.claude/output-styles/`

### Codex
- Root guidance: `AGENTS.md`
- Skills (official repo scope): `.agents/skills/`
- Agents: `.codex/agents/`
- Hooks: `.codex/hooks.json`
- Project config: `.codex/config.toml`

### Cursor
- Compatibility rules: `.cursor/rules/`
- These are thin wrappers pointing back to `/memory`.

## Important note about parity

Claude and Codex overlap strongly on **skills**, **hooks**, **repo guidance**, and **subagents/custom agents**. They do **not** have perfect 1:1 parity for every UX concept. In this scaffold:

- Claude native **output styles** stay in `.claude/output-styles/`.
- Codex maps style-like behavior to **custom agents/personality conventions**, because Codex exposes documented personalities and custom agents rather than a documented custom output-style file format.
- Claude custom commands still work in `.claude/commands/`, but Codex treats reusable custom command workflows better as **skills**.

## Suggested rollout

1. Copy this scaffold into the repository root.
2. Review `memory/README.md` and `memory/MANIFEST.md`.
3. Merge the generated `AGENTS.md` and `CLAUDE.md` with any existing root guidance.
4. Update script paths in `.claude/settings.json` and `.codex/hooks.json` if your shell/runtime differs.
5. Start small: enable hooks for safety + docs sync first, then expand.
