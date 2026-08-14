# 01 — Engineering baseline

## Purpose

Define the engineering invariants that apply to **every** change in this
repository, regardless of language, framework, or which skill is in use.
Language- and framework-specific conventions live in `stacks/*.md`; this
file states what holds everywhere.

## Universal principles

- **Inspect before editing.** Read the impacted module, its manifest
  (`build.gradle` / `pom.xml` / `pyproject.toml` / `package.json` /
  `go.mod`), its immediate neighbors, and recent commits before changing
  anything. Form a hypothesis first.
- **Preserve current behavior** unless the task is an explicit refactor
  or feature change.
- **Prefer minimal diffs.** Three short, similar lines beat a premature
  abstraction. Surrounding cleanup is noise unless it is the task.
- **Single responsibility.** One reason to change per module, class,
  function, or file.
- **Explicit over clever.** A reader should not need to follow three
  levels of indirection to understand a flow. Prefer descriptive names
  over comments that explain confusing code.
- **Immutability by default.** Prefer immutable value types (records,
  frozen dataclasses, readonly types, value objects). Mutate only where
  the design requires it.
- **Dependency injection over globals.** Prefer constructor / parameter
  injection so collaborators can be substituted in tests. Avoid hidden
  singletons and global mutable state.
- **Fail loudly, not silently.** Do not swallow errors. Surface them
  through the return type, an error channel, or a raised exception with
  context.
- **No dead code.** Remove unused imports, dead branches, and
  commented-out leftovers in the files you touch.

## Mandatory behavior per change

- Do not finish with **known compile / type / lint errors** in any
  touched module.
- Build or type-check the touched module first, then validate the
  broader path (see `rules/02-validation-and-done-definition.md`).
- Run the tests that match the change.
- Match the **existing style** of the surrounding code: naming,
  formatting, error handling, and file layout.
- Honor the repository's formatter and linter. Do not hand-format
  against the configured tool.

## Configuration and secrets

- Externalize all operationally-meaningful configuration via environment
  variables with a documented default.
- Never hardcode secrets. See `policies/05-security-and-secrets.md`.
- Every new environment variable is documented in `.env.example` and the
  affected module's README in the same change.

## Dependencies

- **Centralize versions.** Declare dependency versions in the project's
  single source (root `build.gradle` / `libs.versions.toml`,
  `pyproject.toml`, root `package.json` + lockfile, `go.mod`). Child
  modules inherit; they do not re-declare versions.
- Pin to a specific version, never an open range.
- New dependencies require a one-line rationale and a supply-chain check
  (`policies/05-security-and-secrets.md`,
  `skills/dependency-management/SKILL.md`).

## Architecture

- Respect the layer boundaries defined in
  `policies/02-clean-architecture.md`.
- Keep domain / core logic free of framework, transport, and persistence
  imports.
- Keep mapping and serialization at the boundary, never deep inside core
  logic.

## Forbidden patterns (all stacks)

- Committing code with known compile / type / lint errors.
- Wildcard / star imports where the language allows explicit imports.
- Catching the broadest error type only to silence it.
- Global mutable state used as a communication channel.
- Declaring dependency versions per-module instead of centrally.
- Hardcoded secrets, URLs, or credentials.
- Leaving dead code or commented-out blocks in touched files.

## Where stack specifics live

| Stack                         | Profile                          |
| ----------------------------- | -------------------------------- |
| Java + Spring Boot            | `stacks/java-spring.md`          |
| Python + FastAPI              | `stacks/python-fastapi.md`       |
| Node + TypeScript             | `stacks/node-typescript.md`      |
| PostgreSQL                    | `stacks/postgresql.md`           |
| MongoDB                       | `stacks/mongodb.md`              |
| Redis / Valkey                | `stacks/redis.md`                |
| Kafka / event streaming       | `stacks/messaging-kafka.md`      |
| REST / HTTP API design        | `stacks/rest-api-design.md`      |
| Docker / local infra          | `stacks/docker-compose.md`       |

Activate only the profiles the repository actually uses.
