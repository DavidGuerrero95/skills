---
name: feature-implementation
description: Implement or refactor a feature in any stack (Java/Spring, Python/FastAPI, Node/TypeScript, …) while respecting clean architecture, async correctness, validation gates, and idempotency. Use whenever domain logic, use cases, entry points, adapters, DTOs, mappers, or wiring are touched.
license: MIT
metadata:
  scope: cross-stack-implementation
  version: "2.0"
---

# Feature implementation

## When to use

Activate this skill when the task touches any of:

- Domain / core logic, use cases / application services.
- Inbound adapters (controllers, routers, handlers, consumers,
  schedulers) or outbound adapters (repositories, clients, producers).
- DTOs, request/response schemas, mappers, validators.
- Wiring / composition root / dependency injection.

## When NOT to use

- Pure test authoring (`skills/unit-test-crafter`,
  `skills/e2e-test-crafter`).
- Schema / migration design (`skills/database-design`).
- Diagrams (`skills/mermaid-architecture-diagrams`).
- Documentation-only tasks (`skills/technical-doc-writer`).

## Read first

- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`
- `memory/policies/03-async-and-messaging.md` (when async/event-driven)
- The active `memory/stacks/<stack>.md` profile(s).
- `memory/rules/01-task-execution-flow.md`
- `memory/rules/02-validation-and-done-definition.md`

## Workflow

1. **Identify the impacted layer.**
   - domain / application / entry-points / driven-adapters / composition
     root (see `policies/02-clean-architecture.md` and the stack
     profile's layout).
   - Confirm the change does not pull framework/persistence imports into
     the domain.

2. **Read the immediate neighbors.**
   - The unit you are editing plus its 2–3 closest collaborators
     (caller, port, mapper) and the existing tests for the area.

3. **Match the local style and stack profile.**
   - DI over globals; immutable value types; validation at the boundary;
     no dead code. Follow `stacks/<stack>.md` for concrete idioms.

4. **Make the smallest correct change.**
   - One responsibility per unit. Mappers at the boundary.
   - Async: never block the runtime; handle the empty/absent case;
     bound concurrency (`policies/03-async-and-messaging.md`).

5. **Add or update targeted tests** in the same change.
   - Pure logic ⇒ unit tests with focused assertions.
   - Use cases ⇒ mock the ports (not the adapters).
   - Adapters ⇒ Testcontainers / ephemeral-service integration tests.
   - Reuse named test-data builders/fixtures.

6. **Validate.** Build/type-check, run targeted tests, run the
   formatter/linter — using the active stack's commands
   (`rules/02-validation-and-done-definition.md`).

7. **Update documentation** when behavior or contracts changed
   (`policies/07-documentation-and-traceability.md`).

## Output expected from this skill

```
Files touched:
 - <repo-relative path>

Validation:
 - [ran]   <build/type-check command>
 - [ran]   <test command>
 - [skip]  <what> (reason)

Risks / open follow-ups:
 - ...
```

## Edge cases worth handling explicitly

- **Empty / absent value:** explicit branch, not a silent default.
- **Backpressure on hot paths:** bounded concurrency.
- **Configuration:** new knobs via env var with a default and an
  `.env.example` entry.
- **Migrations:** schema changes go through the migration tool
  (`skills/database-design`), never inline auto-sync.
- **Recoverable errors:** surface via the return type / error channel,
  not a swallowed exception.

## Forbidden patterns

- Blocking an async runtime in production code.
- Framework/persistence imports inside the domain.
- Business logic inside controllers/handlers.
- Adding new env vars without updating `.env.example`.
- Catching the broadest error type to silence failures.
- Bundling an unrelated refactor into a feature change.
