# INVEXA agentic memory foundation

Reusable, idempotent baseline of skills, agents, hooks, commands,
policies, rules and output styles for **Claude Code**, **Codex**, and
**Cursor** when building Java 21 + Spring Boot 4.0.x reactive
microservices in the INVEXA family of projects.

## Design goals

1. **`/memory` is the canonical source of truth.** Adapter folders
   (`.claude/`, `.codex/`, `.cursor/`, `.agents/`) reference it and
   never duplicate content.
2. **Single responsibility per file.** Every memory file owns exactly
   one trigger and one responsibility (see
   `memory/MANIFEST.md`).
3. **Idempotency.** Adding new content updates the canonical owner;
   it never creates a parallel file.
4. **Progressive disclosure.** Short index → policies → rules → skills
   → on-demand references.
5. **Multi-runtime parity.** Claude Code, Codex and Cursor see the
   same content via thin adapter wrappers.

## Repository layout

```
memory/                     # CANONICAL — single source of truth
  README.md
  MANIFEST.md
  policies/                 # non-negotiable invariants
  rules/                    # how work is executed
  skills/                   # reusable workflows (SKILL.md per skill)
  agents/                   # specialized personas
  hooks/                    # lifecycle automation contracts
  commands/                 # explicit user-invoked entrypoints
  output-styles/            # tone-only

.claude/                    # Claude Code adapter
  settings.json             # hook wiring
  agents/*.md               # thin wrappers → /memory/agents/*.md
  commands/*.md             # thin wrappers → /memory/commands/*.md
  skills/<skill>/SKILL.md   # thin wrappers → /memory/skills/<skill>/
  output-styles/*.md        # thin wrappers → /memory/output-styles/*.md

.codex/                     # Codex adapter
  config.toml
  hooks.json                # hook wiring
  agents/*.toml             # thin wrappers → /memory/agents/*.md
  skills/<skill>/SKILL.md   # thin wrappers → /memory/skills/<skill>/
  policies/*.md             # thin wrappers → /memory/policies/*.md

.agents/                    # anthropics/skills layout (tool-neutral)
  skills/<skill>/SKILL.md   # thin wrappers → /memory/skills/<skill>/

.cursor/                    # Cursor adapter
  rules/*.mdc               # thin wrappers → /memory/policies|rules/*.md

scripts/agentic/            # hook implementations
  prompt_memory_reminder.py
  pre_bash_safety_guard.py
  pre_write_secret_scan.py
  post_edit_code_quality.py
  post_task_docs_sync.py
  session_end_orphan_check.py

CLAUDE.md                   # short Claude operating guide → /memory
AGENTS.md                   # short Codex operating guide → /memory
```

## Coverage

### Policies (`memory/policies/`)

- `00-governance.md` — memory governance and change control
- `01-engineering-baseline.md` — Java 21 + Spring 4.0.x + Gradle
- `02-clean-architecture.md` — hexagonal layer matrix
- `03-reactive-and-messaging.md` — Reactor + Kafka invariants
- `04-testing-and-quality-gates.md` — Spotless + Sonar + JaCoCo 70 %
- `05-security-and-secrets.md` — secrets, destructive guardrails,
  supply chain
- `06-investment-domain-guardrails.md` — INVEXA trading safety
- `07-documentation-and-traceability.md` — doc surfaces & cadence

### Rules (`memory/rules/`)

- `00-project-baseline.md` — inspect → change → validate → summarize
- `01-task-execution-flow.md` — task sequence + DOR + escalation
- `02-validation-and-done-definition.md` — DoD + validation ladder
- `03-subagent-delegation.md` — when and how to delegate
- `04-idempotency-and-event-contracts.md` — per-layer key matrix
- `05-diagrams-and-docs.md` — Mermaid + docs cadence

### Skills (`memory/skills/`)

- `java-spring-implementation` — implement / refactor Java + Spring
- `reactive-kafka-engineering` — Reactor + Kafka + R2DBC + DLQ
- `unit-test-crafter` — JUnit 5 + Mockito + AssertJ + regression
- `e2e-test-crafter` — smoke + E2E across services
- `code-smell-remediator` — behavior-preserving cleanup
- `implementation-bug-hunter` — root cause + regression
- `investment-domain-review` — trading safety review
- `mermaid-architecture-diagrams` — diagrams that match reality
- `state-of-the-art-research` — pattern selection grounded in repo
- `technical-doc-writer` — README / ADR / runbook authoring
- `dependency-management` — Gradle deps + supply chain

### Agents (`memory/agents/`)

`java-implementation-engineer`, `java-architect`,
`unit-test-engineer`, `e2e-test-engineer`, `code-smell-auditor`,
`failure-investigator`, `mermaid-architect`, `technical-writer`,
`security-reviewer`, `code-reviewer`, `dependency-auditor`.

### Commands (`memory/commands/`)

`/implement-feature`, `/review-changes`, `/audit-code-smells`,
`/write-e2e-tests`, `/fix-failing-tests`, `/root-cause-analysis`,
`/generate-diagrams`, `/sync-documentation`, `/refactor-module`.

### Hooks (`memory/hooks/`)

`prompt-memory-reminder`, `pre-bash-safety-guard`,
`pre-write-secret-scan`, `post-edit-code-quality`,
`post-task-docs-sync`, `session-end-orphan-check`,
`subagent-stop-summary`.

### Output styles (`memory/output-styles/`)

`Terse Caveman`, `Teaching Senior`, `Architect Audit`,
`Incident Responder`.

## Suggested rollout

1. Copy this scaffold into the target repository root.
2. Read `memory/README.md` and `memory/MANIFEST.md`.
3. Merge the generated `AGENTS.md` and `CLAUDE.md` with any existing
   root operating guides.
4. Adjust `python3` vs `python` in `.claude/settings.json` and
   `.codex/hooks.json` to match your environment.
5. Smoke-test the hooks:

   ```bash
   echo '{}' | python3 scripts/agentic/prompt_memory_reminder.py
   echo '{}' | python3 scripts/agentic/pre_bash_safety_guard.py
   echo '{}' | python3 scripts/agentic/pre_write_secret_scan.py
   ```

6. Start small: enable safety + docs-sync hooks first, then expand.
7. When a new responsibility appears, find the canonical owner in
   `memory/MANIFEST.md` and update it. Do not add a parallel file.
