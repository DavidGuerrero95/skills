# Engineering baseline

## Default stack profile

- Java 21
- Spring Boot 3.5+ or 4.x when the repository requires it
- Reactor / WebFlux for reactive services
- Gradle multi-module builds
- JUnit 5, Mockito, Testcontainers where useful
- Hexagonal / clean architecture with explicit boundaries

## Mandatory behavior

- Inspect module layout and naming before editing.
- Preserve existing behavior unless the requested change is explicitly functional.
- Prefer small, targeted diffs.
- Do not finish with known compilation errors in touched areas.
- Compile touched modules first, then verify the broader project path.
- Run the tests relevant to the change.
- Remove unused imports, code, and commented-out leftovers.
- Do not use wildcard imports.
- Keep dependency versions centralized.

## Delivery conventions

- Prefer constructor injection.
- Prefer `record` for DTO-like transport models when appropriate.
- Keep domain code free of framework annotations.
- Keep transport mapping near the boundary.
- Prefer explicit names over clever indirection.
- Add or update test data builders for non-trivial fixtures.
