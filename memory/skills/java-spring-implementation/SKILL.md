---
name: java-spring-implementation
description: Implement or refactor Java 21 + Spring Boot 4.0.x services in this repository while respecting clean architecture, reactive constraints, validation gates, and idempotency. Use whenever Spring controllers, handlers, routers, services, use cases, domain types, DTOs, mappers, or Gradle modules under co.com.invexa are touched.
license: Proprietary. Internal use only.
metadata:
  owner: invexa-platform
  scope: java-spring-boot-4
  version: "1.1"
---

# Java + Spring implementation

## When to use

Activate this skill when the task touches any of:

- Spring controllers / handlers / routers / `@Service` / use cases.
- Java domain or application classes under `co.com.invexa.*`.
- DTOs, mappers, validators, request/response records.
- Gradle modules under `<service>-ms/`.
- WebFlux configuration or `WebClient` adapters.

## When NOT to use

- Pure shell / Docker / CI tasks (use a different workflow).
- Mermaid diagrams (`skills/mermaid-architecture-diagrams`).
- E2E / smoke scripts (`skills/e2e-test-crafter`).
- Documentation-only tasks (`skills/technical-doc-writer`).

## Read first

- `memory/policies/01-engineering-baseline.md`
- `memory/policies/02-clean-architecture.md`
- `memory/policies/03-reactive-and-messaging.md`
- `memory/rules/01-task-execution-flow.md`
- `memory/rules/02-validation-and-done-definition.md`

If the change touches Kafka producers/consumers, also read
`memory/skills/reactive-kafka-engineering/SKILL.md`.

## Workflow

1. **Identify the impacted layer.**
   - `domain/`, `usecase/`, `infrastructure/entry-points/*`,
     `infrastructure/driven-adapters/*`, or `applications/app-service/`.
   - Confirm the change does not pull framework imports into `domain/`.

2. **Read the immediate neighbors.**
   - The class or file you are editing, plus its 2-3 closest
     collaborators (caller, port, mapper).
   - Existing tests for the area. The shape of new tests follows the
     shape of existing tests when consistent.

3. **Match the local style.**
   - Constructor injection. `record` for transport DTOs. No wildcard
     imports. No field injection.
   - Domain code stays free of Spring / persistence / messaging SDK
     imports.

4. **Make the smallest correct change.**
   - One responsibility per class. Mappers at the boundary.
   - Reactive: `map` for sync transforms, `flatMap` for async work,
     no `block()` outside test code.
   - For external blocking SDKs, isolate on
     `Schedulers.boundedElastic()` and document why.

5. **Add or update targeted tests** in the same change.
   - Pure logic ⇒ unit tests with focused assertions.
   - Use cases ⇒ unit tests of orchestration; ports are mocked at the
     port interface, not at the adapter implementation.
   - Adapters ⇒ Testcontainers integration tests for the real protocol
     (Kafka, R2DBC, MongoDB, Valkey).
   - Use `[ClassName]TestData` builders for non-trivial fixtures.

6. **Validate.**
   - `:<service>:<module>:compileJava`
   - `:<service>:test`
   - Spotless if the module enforces it.
   - Coverage if the module ships its own JaCoCo verification.

7. **Update documentation** when behavior or contracts changed
   (`policies/07-documentation-and-traceability.md`).

## Output expected from this skill

The change summary always contains:

```
Files touched:
 - <repo-relative path>

Validation:
 - [ran]   ./gradlew :...
 - [ran]   ./gradlew :...:test
 - [skip]  full smoke (reason)

Risks / open follow-ups:
 - ...
```

## Edge cases worth handling explicitly

- **Empty publisher**: `switchIfEmpty(...)` or
  `Mono.error(...)` instead of letting an empty stream silently win.
- **Backpressure on hot streams**: a bounded `flatMap` concurrency, or
  `limitRate`, when the upstream can fan out.
- **Configuration**: new operational knobs go via env var with a
  default in YAML and an entry in `.env.example` files.
- **Migrations**: SQL changes go under
  `infrastructure/databases/postgresql/migrations/changelog/` (shared)
  or per-service Flyway folders, never inline in code.
- **Recoverable downstream errors**: surface them via the use case's
  return type / event flow, not via swallowed `Throwable`.

## Forbidden patterns

- `block()` in production code.
- Field injection or `@Autowired` constructors with `@Lazy` to mask
  cycles.
- Mixing Jackson 2 + Jackson 3 imports.
- Declaring dependency versions in child-module `build.gradle`.
- Wildcard imports.
- Catching `Throwable` to silence failures.
- Adding new env vars without updating `.env.example` files.
