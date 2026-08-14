# 00 — Governance policy

## Purpose

Define the non-negotiable governance for this `/memory` system. This file
sets the rules that every other file in `/memory` must follow. It is
stack-agnostic: it applies whether the project is Java, Python, Node,
Go, or anything else.

## Canonical-source rules

- `/memory` is the **only** source of truth for agent behavior in this
  repository.
- Adapter folders (`.claude/`, `.codex/`, `.cursor/`, `.agents/`,
  `.github/` Copilot instructions) **must not** become independent
  stores of policy, rules, skills or personas. They reference canonical
  files only.
- `AGENTS.md`, `CLAUDE.md`, and any other root file must stay short. They
  point at `/memory`; they never duplicate it.

## Single-responsibility rules

A new file in `/memory` is justified only if all four are true:

1. It serves a **distinct trigger** (when does it apply?).
2. It owns a **distinct responsibility** (what is it deciding or doing?).
3. It does not mostly restate an existing file.
4. It can answer:
   - When does this apply?
   - When does it explicitly **not** apply?
   - What inputs does it expect?
   - What validation does it require?

If any answer is missing, the content goes inside an existing file.

## Layer vs. stack separation

- **Policies** and **rules** are stack-agnostic. They state invariants
  and execution flow that hold for any language or framework.
- **Stack profiles** (`stacks/*.md`) hold the language-, framework-, and
  datastore-specific conventions (Java/Spring, Python/FastAPI,
  PostgreSQL, MongoDB, …). Activate only the profiles the repository
  actually uses.
- A policy must never hardcode a single stack's syntax as if it were
  universal. When a policy needs a concrete example, it points to the
  relevant stack profile.

## Anti-duplication rules

- When two files appear to overlap, **shrink or merge the weaker one**;
  do not tolerate duplication "just to be explicit".
- Prefer additive local specialization over broad global verbosity.
- Do not restate engineering or architectural rules inside individual
  skills — link to the canonical policy instead.

## Precedence

Already defined in `memory/README.md`. Treat that section as binding.

## Change control

Any structural change to `/memory` (new folder, new file, removal of a
file) requires:

- updating `memory/MANIFEST.md` so the ownership matrix stays correct;
- a one-line rationale in the file itself (`## Why this exists`);
- a verification that no adapter still copies the old content.

## Failure modes to actively prevent

- "Two files saying almost the same thing."
- "Adapter file with original instructions instead of a pointer."
- "Long procedural content embedded inside `policies/` or `rules/`."
- "A stack's syntax hardcoded into a stack-agnostic policy."
- "Domain rules leaking into output styles."
- "Skills that re-explain global engineering rules from scratch."
