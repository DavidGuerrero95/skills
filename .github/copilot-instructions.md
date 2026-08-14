# GitHub Copilot instructions

`/memory` is the canonical source of truth for how agents operate in this
repository. This file is a thin pointer; it never duplicates canonical
content. Path-scoped rules live in `.github/instructions/*.instructions.md`.

## Read path before non-trivial work

1. `/memory/README.md`
2. `/memory/MANIFEST.md`
3. The applicable file in `/memory/policies/`
4. The applicable file in `/memory/rules/`
5. The active stack profile in `/memory/stacks/`
6. The relevant `/memory/skills/<skill>/SKILL.md`

## Working agreements

- Keep domain / core code framework-free; respect hexagonal boundaries
  (`/memory/policies/02-clean-architecture.md`).
- Prefer minimal diffs; match the surrounding style and the active stack
  profile (`/memory/stacks/*`).
- Never block an async runtime; handle the empty/absent case
  (`/memory/policies/03-async-and-messaging.md`).
- Tests come with the change; run the smallest meaningful validation
  (`/memory/rules/02-validation-and-done-definition.md`).
- Never hardcode secrets; document new env vars in `.env.example`
  (`/memory/policies/05-security-and-secrets.md`).
- Update docs when behavior or contracts change
  (`/memory/policies/07-documentation-and-traceability.md`).

## This repository

A stack-agnostic, reusable agentic baseline. Supported stacks each have a
profile under `/memory/stacks/` (Java/Spring, Python/FastAPI,
Node/TypeScript, PostgreSQL, MongoDB, Redis/Valkey, Kafka, REST, Docker).
Do not add duplicated rules here — update the canonical file under
`/memory` and keep this pointer thin.
