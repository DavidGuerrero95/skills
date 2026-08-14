# Agentic memory foundation

A reusable, idempotent, **stack-agnostic** baseline of skills, agents,
hooks, commands, policies, rules, stack profiles and output styles for
**Claude Code**, **Codex**, **Cursor**, and **GitHub Copilot**. Drop it
into any repository and adapt a few placeholders — it does not assume a
language, framework, or product.

## Design goals

1. **`/memory` is the canonical source of truth.** Adapter folders
   (`.claude/`, `.codex/`, `.cursor/`, `.agents/`, `.github/` Copilot
   instructions) reference it and never duplicate content.
2. **Single responsibility per file.** Every memory file owns exactly one
   trigger and one responsibility (see `memory/MANIFEST.md`).
3. **Idempotency.** Adding new content updates the canonical owner; it
   never creates a parallel file.
4. **Progressive disclosure.** Short index → policies → rules → stacks →
   skills → on-demand references.
5. **Stack-agnostic core + opt-in stack profiles.** Universal invariants
   live in `policies/`; language/datastore specifics live in `stacks/`.
6. **Multi-runtime parity.** Claude Code, Codex, Cursor, and Copilot see
   the same content via thin adapter wrappers.

## Repository layout

```
memory/                     # CANONICAL — single source of truth
  README.md
  MANIFEST.md
  policies/                 # stack-agnostic invariants
  rules/                    # how work is executed
  stacks/                   # language / framework / datastore profiles
  skills/                   # reusable workflows (SKILL.md per skill)
  agents/                   # specialized personas
  hooks/                    # lifecycle automation contracts
  commands/                 # explicit user-invoked entrypoints
  output-styles/            # tone-only

.claude/                    # Claude Code adapter (settings.json + wrappers)
.codex/                     # Codex adapter (hooks.json + wrappers)
.cursor/                    # Cursor adapter (rules/*.mdc)
.agents/                    # tool-neutral skills (anthropics/skills layout)
.github/
  copilot-instructions.md   # GitHub Copilot adapter (root)
  instructions/             # Copilot path-scoped instructions
  workflows/                # CI/CD pipelines
scripts/agentic/            # hook implementations (Python)

CLAUDE.md                   # short Claude operating guide → /memory
AGENTS.md                   # short Codex/Copilot operating guide → /memory
```

## What's inside

### Policies (`memory/policies/`) — stack-agnostic

`00-governance`, `01-engineering-baseline`, `02-clean-architecture`,
`03-async-and-messaging`, `04-testing-and-quality-gates`,
`05-security-and-secrets`, `06-domain-guardrails` (project template),
`07-documentation-and-traceability`.

### Rules (`memory/rules/`)

`00-project-baseline`, `01-task-execution-flow`,
`02-validation-and-done-definition`, `03-subagent-delegation`,
`04-idempotency-and-event-contracts`, `05-diagrams-and-docs`.

### Stack profiles (`memory/stacks/`)

`java-spring`, `python-fastapi`, `node-typescript`, `postgresql`,
`mongodb`, `redis`, `messaging-kafka`, `rest-api-design`,
`docker-compose`.

### Skills (`memory/skills/`)

`feature-implementation`, `async-messaging-engineering`,
`unit-test-crafter`, `e2e-test-crafter`, `code-smell-remediator`,
`implementation-bug-hunter`, `domain-safety-review`, `database-design`,
`mermaid-architecture-diagrams`, `state-of-the-art-research`,
`technical-doc-writer`, `dependency-management`.

### Agents (`memory/agents/`)

`implementation-engineer`, `software-architect`, `unit-test-engineer`,
`e2e-test-engineer`, `code-smell-auditor`, `failure-investigator`,
`database-engineer`, `mermaid-architect`, `technical-writer`,
`security-reviewer`, `code-reviewer`, `dependency-auditor`.

### Pipelines (`memory/pipelines/`)

Ordered multi-agent chains with an artifact and a **gate** between each
stage: `feature-delivery`, `bug-fix`, `refactor`, `database-change`,
`contract-change`, `review-gate`. The main thread runs a pipeline by
delegating to each stage's agent in order and honoring its gate (see
`memory/pipelines/README.md`).

### Commands (`memory/commands/`)

`/implement-feature`, `/review-changes`, `/audit-code-smells`,
`/write-e2e-tests`, `/fix-failing-tests`, `/root-cause-analysis`,
`/generate-diagrams`, `/sync-documentation`, `/refactor-module`,
`/design-database`.

### Hooks (`memory/hooks/`)

`prompt-memory-reminder`, `pre-bash-safety-guard`,
`pre-write-secret-scan`, `post-edit-code-quality`, `post-task-docs-sync`,
`session-end-orphan-check`, `subagent-stop-summary`.

### Output styles (`memory/output-styles/`)

`Terse Caveman`, `Teaching Senior`, `Architect Audit`,
`Incident Responder`.

## Rollout in a new repository

1. Copy this scaffold into the target repository root.
2. Read `memory/README.md` and `memory/MANIFEST.md`.
3. Keep the `stacks/` profiles you use; the rest stay as reference.
4. Fill in `policies/06-domain-guardrails.md` (ownership map + critical
   invariants) and the idempotency matrix in
   `rules/04-idempotency-and-event-contracts.md`.
5. Adjust coverage threshold and validation commands to your toolchain.
6. Merge `AGENTS.md` and `CLAUDE.md` with any existing root guides.
7. Confirm `python3` vs `python` for the hooks in `.claude/settings.json`
   and `.codex/hooks.json`, then smoke-test:

   ```bash
   echo '{}' | python3 scripts/agentic/prompt_memory_reminder.py
   echo '{}' | python3 scripts/agentic/pre_bash_safety_guard.py
   echo '{}' | python3 scripts/agentic/pre_write_secret_scan.py
   ```

8. Point the CI workflow in `.github/workflows/` at your stack's jobs.

## License

MIT — see `LICENSE`.
