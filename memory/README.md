# /memory — canonical source of truth

This directory is the **single, version-controlled source of truth** for
how coding agents (Claude Code, Codex, Cursor, GitHub Copilot) operate in
this repository. Every other folder (`.claude/`, `.codex/`, `.cursor/`,
`.agents/`, and the Copilot instructions under `.github/`) is a thin
runtime adapter that points back here.

This baseline is **stack-agnostic and reusable**: drop it into any
project (Java, Python, Node, Go, …), activate the relevant `stacks/`
profiles, fill in `policies/06-domain-guardrails.md`, and go.

## Why this layout exists

A typical mistake is to spread instructions across `CLAUDE.md`,
`AGENTS.md`, `.cursor/rules/`, ad hoc prompts and chat history. That
produces drift, contradictions and wasted tokens. `/memory` solves it by:

1. **One canonical file per responsibility.** No instruction is
   duplicated.
2. **Adapters do not own content.** They only forward to canonical files.
3. **Progressive disclosure.** Short index → policies → rules → stacks →
   skills → on-demand references. Heavy content stays out of
   always-loaded files.
4. **SRP per file.** Every file answers exactly one of: *what is
   forbidden*, *how do we work*, *how do we do task X*, *who acts as role
   Y*, *what triggers automation*, *what commands exist*, *how do we
   communicate*, *what are this stack's conventions*.

## Folder contract

| Folder           | Purpose                                                        | Must NOT contain                                |
| ---------------- | -------------------------------------------------------------- | ----------------------------------------------- |
| `policies/`      | Stack-agnostic invariants and governance                       | Task workflows, tone, stack syntax              |
| `rules/`         | How work is executed (flow, DoD, delegation)                   | Long procedures, persona text                   |
| `stacks/`        | Language / framework / datastore conventions                   | Universal invariants (those live in policies)   |
| `skills/`        | Reusable, named workflows with progressive disclosure          | Global policy, persona definition, stack syntax |
| `agents/`        | Specialized personas / delegates                               | General repo rules, project policy text         |
| `hooks/`         | Lifecycle automation contracts (rationale + trigger + scope)   | Implementation code (lives in `scripts/`)       |
| `commands/`      | Explicit user-invoked entrypoints                              | Deep how-to (delegate to a skill)               |
| `output-styles/` | Communication style only                                       | Validation rules, domain policy                 |

## Precedence (when sources conflict)

1. Runtime/platform safety (the harness itself)
2. `memory/policies/*` — non-negotiable invariants
3. `memory/rules/*` — repo operating mode
4. `memory/stacks/*` — the active stack's conventions
5. Active `memory/skills/*` or `memory/agents/*` content for the task
6. Active `memory/output-styles/*` for tone only
7. Ad hoc task prompt
8. Adapter folders — never override canonical content; they may only
   narrow it for a runtime quirk and must reference the canonical file.

## Read path before any non-trivial change

1. `memory/README.md` (this file)
2. `memory/MANIFEST.md`
3. The applicable file in `memory/policies/`
4. The applicable file in `memory/rules/`
5. The active `memory/stacks/<stack>.md` profile(s)
6. The most relevant `memory/skills/*/SKILL.md` (only when activated)
7. The most relevant `memory/agents/*.md` (only if delegating)

## Idempotency guarantee

A file may exist in `/memory` only if it has a **distinct trigger** and a
**distinct responsibility**. If a new instruction mostly restates an
existing file, the existing file is updated instead of adding a second
one. See `MANIFEST.md` for the ownership matrix and anti-duplication
rules.

## Adopting this baseline in a project

1. Copy the whole scaffold into the target repository root.
2. Read `memory/README.md` and `memory/MANIFEST.md`.
3. In `stacks/`, keep the profiles you use; the rest stay as reference.
4. Fill in `policies/06-domain-guardrails.md` with the project's real
   ownership map and critical invariants.
5. Fill in the project idempotency matrix in
   `rules/04-idempotency-and-event-contracts.md`.
6. Adjust the coverage threshold and validation commands in
   `policies/04-*` and `rules/02-*` to the project's toolchain.
7. Merge the generated `AGENTS.md` and `CLAUDE.md` with any existing root
   guides. Keep them short.
8. Verify the hooks run (`.claude/settings.json`, `.codex/hooks.json`)
   and that the CI workflow under `.github/workflows/` matches the stack.

## How to extend

1. Identify the canonical owner using `MANIFEST.md`.
2. If no owner exists, justify a new file (distinct trigger +
   responsibility).
3. Add the file with a clear single-purpose header.
4. Update `MANIFEST.md` so future contributors see it.
5. If a runtime adapter needs to expose it, add a thin reference file —
   never copy the body.
