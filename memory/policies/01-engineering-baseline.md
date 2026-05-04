# 01 — Engineering baseline

## Purpose

Define the engineering invariants that apply to **every** Java/Spring
change in this repository, regardless of which service or skill is in
use.

## Stack profile

- **Language:** Java 21 (LTS). Use modern language features when they
  improve clarity: `record`, sealed types, pattern matching for `switch`,
  text blocks. Do not retrofit older idioms when a record is a better
  fit.
- **Framework:** Spring Boot 4.0.x with WebFlux + Reactor 3.7+. Reactive
  by default. Avoid the Servlet stack unless the module is explicitly
  blocking.
- **Build:** Gradle multi-module. **All dependency versions are declared
  in the root `build.gradle`.** Child modules inherit; they must not
  declare their own versions.
- **JSON:** Jackson 3.1 (`tools.jackson.databind`). Do not mix with
  Jackson 2 (`com.fasterxml.jackson.databind`) artifacts.
- **Tests:** JUnit 5 + Mockito + AssertJ. Testcontainers when an adapter
  test needs a real broker, database, or cache.
- **Architecture:** hexagonal / clean architecture (see
  `02-clean-architecture.md`).

## Mandatory behavior

- **Inspect before editing.** Read the impacted module's `build.gradle`,
  package structure, and immediate neighbors before making changes.
- **Preserve current behavior** unless the task is an explicit refactor
  or feature change.
- **Prefer minimal diffs.** Three short, similar lines beat a premature
  abstraction.
- Do not finish with **known compilation errors** in any touched module.
- Compile the touched module first, then validate the broader path:

  ```powershell
  # Per service (Windows PowerShell, from repo root)
  .\gradlew.bat :<service>:<module>:compileJava
  .\gradlew.bat :<service>:test
  ```

  ```bash
  # Full smoke after a cross-service change (WSL)
  bash infrastructure/scripts/smoke-all-services.sh
  ```

- Run the tests that match the change (see
  `02-validation-and-done-definition.md` for the validation ladder).
- **Remove unused imports, dead code, and commented-out leftovers.**
- **Do not use wildcard imports.** Configure or honor existing Spotless
  / Checkstyle rules.

## Delivery conventions

- Prefer **constructor injection** for Spring beans. Avoid field
  injection.
- Prefer `record` for DTOs and transport models when immutability is the
  intent.
- Keep **domain code framework-free** — no Spring, persistence, HTTP, or
  messaging SDK imports inside `domain/`.
- Keep transport mapping (REST, Kafka serializers, R2DBC mappers) at the
  boundary, never deep inside use cases.
- Prefer **explicit names** over clever indirection. A reader should not
  need to follow three levels of abstraction to understand a flow.
- Add or update **`[ClassName]TestData` builders** for any non-trivial
  fixture instead of duplicating setup inline.

## Java 21 features in active use

- `record` for value objects, command/query DTOs, event payloads.
- Sealed hierarchies (`sealed`, `non-sealed`, `final`) where the domain
  has a closed set of variants.
- Pattern matching `switch` over sealed types instead of visitor classes
  when readability wins.
- Text blocks for SQL strings, JSON test fixtures, and large prompts.
- Virtual threads only when the surrounding chain is **already
  synchronous** and proven blocking. Never wrap a Reactor pipeline in a
  virtual-thread executor.

## Spring Boot 4.0.x specifics

- `application.yaml` over `application.properties`. Environment-specific
  overrides go in `application-<profile>.yaml`.
- Externalize all operationally-meaningful configuration via env vars
  with a default in YAML.
- Use `@ConfigurationProperties` records over `@Value` constants.
- Use `WebFluxConfigurer` for HTTP, `KafkaListener`/`ReactiveKafka`
  bindings for messaging, and R2DBC repositories for SQL.
- Prefer the constructor form of `WebClient.Builder` injection so test
  doubles can replace it cleanly.

## Package layout convention

Repository base package: `co.com.invexa`.

Per service:

```
<service>-ms/
├── domain/                 # entities, value objects, ports, domain events
├── usecase/                # application orchestration (a.k.a. application/)
├── infrastructure/
│   ├── entry-points/       # webflux-handler, kafka-consumer, scheduler...
│   └── driven-adapters/    # postgresql, mongo, valkey, alpaca, ollama...
└── applications/app-service/   # Spring Boot wiring + configuration
```

Module names match the folders. Test fixtures live next to the production
classes they support.

## Forbidden patterns

- Wildcard imports.
- Static `Logger` field on a class without a clear naming convention.
- Field injection (`@Autowired` on fields).
- Mixing Jackson 2 + Jackson 3 imports in the same module.
- Declaring dependency versions inside child-module `build.gradle` files.
- Calling `block()` / `blockFirst()` / `blockLast()` in production code.
- Catching `Throwable` to silence failures.
