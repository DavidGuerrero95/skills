# Stack — Java + Spring Boot

Concrete conventions for Java + Spring Boot services. Universal
invariants stay in `policies/`; this profile adds the Java specifics.

## When to use

The module is Java 21+ built with Gradle (or Maven) and Spring Boot
(WebFlux for reactive, MVC for blocking).

## Toolchain

- **Language:** Java 21 (LTS). Use modern features when they improve
  clarity: `record`, sealed types, pattern-matching `switch`, text
  blocks.
- **Framework:** Spring Boot 3.2+ / 4.0.x. Reactive (WebFlux + Reactor)
  by default when the service is IO-bound; MVC only for explicitly
  blocking modules.
- **Build:** Gradle multi-module. **All dependency versions in the root
  `build.gradle` or `gradle/libs.versions.toml`.** Child modules inherit.
- **JSON:** one Jackson major version per module. Do not mix Jackson 2
  (`com.fasterxml.jackson`) and Jackson 3 (`tools.jackson`) artifacts.
- **Tests:** JUnit 5 + Mockito + AssertJ; Testcontainers for adapter
  integration tests; `StepVerifier` for Reactor streams.

## Project layout (hexagonal)

```
<service>/
├── domain/                 # entities, value objects, ports, domain events
├── usecase/                # application orchestration
├── infrastructure/
│   ├── entry-points/       # webflux-handler, kafka-consumer, scheduler…
│   └── driven-adapters/    # postgresql, mongo, redis, http-clients…
└── applications/app-service/   # Spring Boot wiring + configuration
```

Module names match folders. Domain stays framework-free.

## Conventions

- **Constructor injection** only. No field injection, no `@Autowired` on
  fields.
- `record` for DTOs, commands, query results, and event payloads.
- Sealed hierarchies for closed variant sets; pattern-matching `switch`
  over them instead of visitors.
- `@ConfigurationProperties` records over scattered `@Value`.
- `application.yaml` over `.properties`; profile overrides in
  `application-<profile>.yaml`; operational values via env vars with a
  YAML default.
- Reactive: `map` for sync, `flatMap` for async, `concatMap` when order
  matters; isolate blocking SDKs on `Schedulers.boundedElastic()`.
- Virtual threads only when the surrounding chain is already synchronous
  and proven blocking. Never wrap a Reactor pipeline in a virtual-thread
  executor.

## Validation commands

```bash
./gradlew :<module>:compileJava
./gradlew :<module>:test
./gradlew spotlessCheck
./gradlew test jacocoTestReport jacocoTestCoverageVerification --no-daemon
```

## Forbidden patterns

- `block()` / `blockFirst()` / `blockLast()` in production code.
- `subscribe()` in domain or use-case code.
- Wildcard imports.
- Field injection.
- Mixing Jackson 2 + Jackson 3 in one module.
- Declaring dependency versions in child-module build files.
- Catching `Throwable` to silence failures.
